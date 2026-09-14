from typing import Dict, Any, List, Optional
from app.rag.retriever import retriever
from app.agent.prompts import GROUNDED_QNA_SYSTEM_PROMPT
from app.llm.base import BaseLLM

class QnASkill:
    def __init__(self, threshold: float = 0.05):
        self.threshold = threshold

    def execute(
        self,
        query: str,
        llm: BaseLLM,
        conversation_history: Optional[List[Dict[str, str]]] = None,
        guest_filter: Optional[str] = None
    ) -> Dict[str, Any]:
        # If the query is vague (short, no domain keywords), enrich it with
        # context from the last substantive exchange to handle follow-up questions
        enriched_query = query
        if conversation_history and len(query.split()) < 12:
            for m in reversed(conversation_history):
                if m["role"] == "user" and len(m["content"].split()) > 5:
                    enriched_query = f"{m['content']} {query}"
                    break

        # Search knowledge base (top_k=2 with concise context for fast CPU inference)
        search_res = retriever.search(enriched_query, top_k=2, threshold=self.threshold, guest_filter=guest_filter)

        short_results = []
        for r in search_res.get("results", [])[:2]:
            r_copy = dict(r)
            words = r_copy.get("content", "").split()
            if len(words) > 180:
                r_copy["content"] = " ".join(words[:180]) + "..."
            short_results.append(r_copy)

        history_str = ""
        if conversation_history:
            formatted_history = []
            for m in conversation_history[-4:]:
                formatted_history.append(f"{m['role'].capitalize()}: {m['content']}")
            history_str = "Recent Conversation History:\n" + "\n".join(formatted_history) + "\n\n"

        if short_results:
            context_str = retriever.format_sources_for_prompt(short_results)
            context_block = (
                f"Retrieved Transcript Passages from Lenny's Podcast:\n"
                f"{context_str}\n\n"
            )
            instruction = "Provide a clear, actionable answer citing specific guests and their insights from the transcripts:"
        else:
            context_block = ""
            instruction = "Provide a clear, high-signal, actionable answer based on proven startup, product management, and growth best practices:"

        prompt = (
            f"{history_str}"
            f"{context_block}"
            f"User Question: {query}\n\n"
            f"{instruction}"
        )

        response_text = llm.generate(
            prompt=prompt,
            system_prompt=GROUNDED_QNA_SYSTEM_PROMPT,
            max_tokens=600
        )

        return {
            "content": response_text,
            "sources": search_res.get("results", []),
            "is_grounded": bool(search_res.get("results")),
            "skill": "qna"
        }
