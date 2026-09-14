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
    "onboarding", "metric", "saas", "customer", "customers", "team", "engineer", "designer",
    "roadmap", "user", "reforge", "funnel", "loop", "experiment", "b2b", "plg",
    "interview", "interviews", "podcast", "lenny", "monetization", "acquisition", "distribution",
    "strategy", "culture", "leadership", "feedback", "okr", "market", "hiring",
    "marketplace", "liquidity", "discovery", "prioritization", "design", "north", "star",
    "cac", "ltv", "margin", "dhm", "lno", "survey", "disappointed",
    "amplitude", "miro", "dropbox", "figma", "pinterest", "netflix", "slack", "stripe",
    "startup", "startups", "founder", "founders", "icp", "ideal", "persona", "segmentation",
    "sales", "gtm", "audience", "positioning", "scale", "launch", "mvp", "validation"
}

class LennyRetriever:
    def __init__(self, kb_path: str = KB_JSON_PATH, index_path: str = INDEX_PATH):
        self.kb_path = kb_path
        self.index_path = index_path
        self.chunks: List[Dict[str, Any]] = []
        self.chunks_by_id: Dict[str, Dict[str, Any]] = {}
        self.all_guests: set = set()
        self.guest_last_names: set = set()
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
            self.all_guests = {c["guest"].lower() for c in self.chunks if c.get("guest")}
            self.guest_last_names = {g.split()[-1] for g in self.all_guests if len(g.split()) > 1}

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
        threshold: float = 0.05,
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
        has_guest_name = any(g in query_lower for g in self.all_guests) or any(ln in query_words for ln in self.guest_last_names)

        # Vector search
        q_vec = self.vectorizer.transform([query])
        cos_sims = cosine_similarity(q_vec, self.tfidf_matrix)[0]

        key_acronyms = [
            "plg", "pmf", "retention", "activation", "cac", "ltv", "pricing", "dhm", "lno", "reforge",
            "icp", "ideal customer", "target customer", "target persona", "mvp", "gtm",
            "product strategy", "strategy stack", "roadmap", "vision", "strategy",
            "40%", "40 percent", "sean ellis", "pmf survey", "product-market fit", "product market fit",
            "first mile", "aha moment", "willingness to pay"
        ]

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
                        boost += 0.04

            # High-signal phrase boosting for specific PM/growth concepts
            if any(k in query_lower for k in ["plg", "product-led", "product led", "self-serve"]):
                if "plg" in chunk_content_lower or "product-led" in chunk_content_lower or "self-serve" in chunk_content_lower:
                    boost += 0.15
                if "hila qu" in chunk_content_lower or "elena verna" in chunk_content_lower:
                    boost += 0.12

            if any(k in query_lower for k in ["team", "teams", "hire", "hiring", "growth team", "product team"]):
                if "growth team" in chunk_content_lower or "adam fishman" in chunk_content_lower or "high-performing" in chunk_content_lower:
                    boost += 0.14

            if any(k in query_lower for k in ["40%", "40 percent", "pmf", "product-market fit", "product market fit", "sean ellis", "survey"]):
                if "very disappointed" in chunk_content_lower or "40%" in chunk_content_lower or "no longer use this product" in chunk_content_lower:
                    boost += 0.12
                if "sean ellis test" in chunk_content_lower or "leading indicator of product market fit" in chunk_content_lower:
                    boost += 0.10

            if any(k in query_lower for k in ["pricing", "monetization", "price", "packaging"]):
                if "willingness to pay" in chunk_content_lower or "monetizing innovation" in chunk_content_lower:
                    boost += 0.10

            if any(k in query_lower for k in ["onboarding", "first mile", "activation"]):
                if "first mile" in chunk_content_lower or "aha moment" in chunk_content_lower or "first 30 seconds" in chunk_content_lower:
                    boost += 0.10

            if (any(k in query_lower for k in ["strategy stack", "ravi mehta"])) or ("product strategy" in query_lower and not any(x in query_lower for x in ["product-led", "product led", "plg"])):
                if "strategy stack" in chunk_content_lower or "roadmap is not strategy" in chunk_content_lower:
                    boost += 0.10

            if any(k in query_lower for k in ["dhm", "biddle", "delight"]):
                if "dhm" in chunk_content_lower or "delight customers in hard-to-copy" in chunk_content_lower:
                    boost += 0.12

            if any(k in query_lower for k in ["lno", "shreyas"]):
                if "lno" in chunk_content_lower or "leverage, neutral" in chunk_content_lower:
                    boost += 0.12

            # Boost if chunk title directly matches key topic in query
            chunk_title_lower = chunk["title"].lower()
            for topic_kw in ["product strategy", "strategy stack", "retention", "pricing", "onboarding", "plg", "activation", "pmf", "product-market fit", "survey", "sean ellis"]:
                if topic_kw in query_lower and topic_kw in chunk_title_lower:
                    boost += 0.06
                    break

            # Boost if chunk guest directly matches query
            chunk_guest_lower = chunk["guest"].lower()
            if chunk_guest_lower in query_lower or (len(chunk_guest_lower.split()) > 1 and chunk_guest_lower.split()[-1] in query_words):
                boost += 0.12

            total_score = base_score + boost

            if total_score > 0.02:
                # Convert timestamp like 00:18:43 into seconds for YouTube deep linking
                raw_url = chunk.get("youtube_url", "")
                ts_str = chunk.get("timestamp", "00:00:00")
                ts_secs = 0
                try:
                    parts = [int(p) for p in ts_str.strip().split(":")]
                    if len(parts) == 3:
                        ts_secs = parts[0] * 3600 + parts[1] * 60 + parts[2]
                    elif len(parts) == 2:
                        ts_secs = parts[0] * 60 + parts[1]
                except Exception:
                    ts_secs = 0

                timestamped_url = f"{raw_url}&t={ts_secs}s" if (raw_url and ts_secs > 0) else raw_url

                scored_results.append({
                    "id": chunk["id"],
                    "guest": chunk["guest"],
                    "title": chunk["title"],
                    "timestamp": ts_str,
                    "youtube_url": timestamped_url,
                    "speaker": chunk.get("primary_speaker", chunk["guest"]),
                    "content": chunk["content"],
                    "score": round(total_score, 4),
                    "base_score": round(base_score, 4)
                })

        scored_results.sort(key=lambda x: x["score"], reverse=True)

        # Select top results with guest/episode diversity (strictly 1 per guest) so each source is a different video & guest
        top_results = []
        guest_counts = {}
        max_per_guest = 1

        for r in scored_results:
            g = r["guest"]
            if guest_counts.get(g, 0) < max_per_guest:
                top_results.append(r)
                guest_counts[g] = guest_counts.get(g, 0) + 1
                if len(top_results) == top_k:
                    break

        # If not enough diverse candidates, fill remaining slots
        if len(top_results) < top_k:
            for r in scored_results:
                if r not in top_results:
                    top_results.append(r)
                    if len(top_results) == top_k:
                        break

        top_score = top_results[0]["score"] if top_results else 0.0
        is_grounded = (top_score >= threshold) and (has_domain_term or has_guest_name)

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
