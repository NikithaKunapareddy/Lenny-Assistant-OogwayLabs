import os
import json
import pickle
import re
from typing import List, Dict, Any, Optional
from sklearn.metrics.pairwise import cosine_similarity

RAG_DIR = os.path.dirname(os.path.abspath(__file__))
KB_JSON_PATH = os.path.join(RAG_DIR, "lenny_knowledge_base.json")
INDEX_PATH = os.path.join(RAG_DIR, "tfidf_index.pkl")

# Core product & growth domain lexicon for Lenny's Podcast
DOMAIN_KEYWORDS = {
    "growth", "product", "retention", "activation", "pmf", "churn", "pricing",
    "onboarding", "metric", "saas", "customer", "team", "engineer", "designer",
    "roadmap", "user", "reforge", "funnel", "loop", "experiment", "b2b", "plg",
    "interview", "podcast", "lenny", "monetization", "acquisition", "distribution",
    "strategy", "culture", "leadership", "feedback", "okr", "market", "hiring",
    "amplitude", "miro", "dropbox", "figma", "pinterest", "netflix", "slack", "stripe"
}

class LennyRetriever:
    def __init__(self, kb_path: str = KB_JSON_PATH, index_path: str = INDEX_PATH):
        self.kb_path = kb_path
        self.index_path = index_path
        self.chunks: List[Dict[str, Any]] = []
        self.chunks_by_id: Dict[str, Dict[str, Any]] = {}
        self.vectorizer = None
        self.tfidf_matrix = None
        self.chunk_ids: List[str] = []
        self.is_loaded = False
        self._load()

    def _load(self):
        if not os.path.exists(self.kb_path) or not os.path.exists(self.index_path):
            print(f"[!] Warning: Knowledge base files missing at {self.kb_path} or {self.index_path}")
            return

        with open(self.kb_path, "r", encoding="utf-8") as f:
            self.chunks = json.load(f)
            self.chunks_by_id = {c["id"]: c for c in self.chunks}

        with open(self.index_path, "rb") as f:
            idx = pickle.load(f)
            self.vectorizer = idx["vectorizer"]
            self.tfidf_matrix = idx["matrix"]
            self.chunk_ids = idx["chunk_ids"]

        self.is_loaded = True
        print(f"[+] LennyRetriever loaded {len(self.chunks)} chunks successfully.")

    def search(
        self,
        query: str,
        top_k: int = 5,
        threshold: float = 0.085,
        guest_filter: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Searches the knowledge base using hybrid TF-IDF + Keyword boosting + Domain verification.
        Returns top matching chunks, relevance scores, and grounding confidence.
        """
        if not self.is_loaded or not query.strip():
            return {
                "results": [],
                "is_grounded": False,
                "top_score": 0.0,
                "message": "Retriever not initialized or query is empty."
            }

        query_lower = query.lower()
        query_words = set(re.findall(r'\b[a-z]{3,}\b', query_lower))

        # Check domain relevance: does query contain at least one PM/growth term or known guest name?
        has_domain_term = bool(query_words.intersection(DOMAIN_KEYWORDS))
        has_guest_name = any(c["guest"].lower() in query_lower for c in self.chunks[:50])

        if not has_domain_term and not has_guest_name:
            # Out-of-domain query (e.g. nuclear reactor, cooking recipes)
            return {
                "query": query,
                "top_score": 0.0,
                "is_grounded": False,
                "total_candidates": 0,
                "results": []
            }

        # Vector search
        q_vec = self.vectorizer.transform([query])
        cos_sims = cosine_similarity(q_vec, self.tfidf_matrix)[0]

        key_acronyms = ["plg", "pmf", "retention", "activation", "cac", "ltv", "pricing", "dhm", "lno", "reforge"]

        scored_results = []
        for i, chunk_id in enumerate(self.chunk_ids):
            chunk = self.chunks_by_id.get(chunk_id)
            if not chunk:
                continue

            if guest_filter and guest_filter.lower() not in chunk["guest"].lower():
                continue

            base_score = float(cos_sims[i])

            # Apply boosting for keyword matches
            chunk_content_lower = chunk["content"].lower()
            boost = 0.0
            for acr in key_acronyms:
                if re.search(r'\b' + re.escape(acr) + r'\b', query_lower):
                    if re.search(r'\b' + re.escape(acr) + r'\b', chunk_content_lower):
                        boost += 0.03

            if chunk["guest"].lower() in query_lower:
                boost += 0.08

            total_score = base_score + boost

            if total_score > 0.02:
                scored_results.append({
                    "id": chunk["id"],
                    "guest": chunk["guest"],
                    "title": chunk["title"],
                    "timestamp": chunk["timestamp"],
                    "youtube_url": chunk.get("youtube_url", ""),
                    "speaker": chunk.get("primary_speaker", chunk["guest"]),
                    "content": chunk["content"],
                    "score": round(total_score, 4),
                    "base_score": round(base_score, 4)
                })

        scored_results.sort(key=lambda x: x["score"], reverse=True)
        top_results = scored_results[:top_k]

        top_score = top_results[0]["score"] if top_results else 0.0
        is_grounded = top_score >= threshold

        return {
            "query": query,
            "top_score": top_score,
            "is_grounded": is_grounded,
            "total_candidates": len(scored_results),
            "results": top_results
        }

    def format_sources_for_prompt(self, results: List[Dict[str, Any]]) -> str:
        """Formats retrieved chunks as context for the LLM prompt."""
        formatted_blocks = []
        for idx, r in enumerate(results, 1):
            block = (
                f"[Source {idx}]:\n"
                f"Guest: {r['guest']}\n"
                f"Episode: {r['title']}\n"
                f"Timestamp: {r['timestamp']}\n"
                f"Dialogue:\n{r['content']}\n"
            )
            formatted_blocks.append(block)
        return "\n----------------------------------------\n".join(formatted_blocks)

# Singleton instance
retriever = LennyRetriever()
