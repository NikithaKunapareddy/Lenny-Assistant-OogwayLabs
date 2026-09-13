from typing import Dict, Any, List, Optional
from app.rag.retriever import retriever
from app.agent.prompts import GROUNDED_QNA_SYSTEM_PROMPT
from app.llm.base import BaseLLM

class QnASkill:
    def __init__(self, threshold: float = 0.085):
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

        if not search_res["is_grounded"]:
            return {
                "content": (
                    "I couldn't find sufficient information about this topic in the available Lenny's Podcast transcripts.\n\n"
                    "My knowledge base contains transcripts from Lenny's interviews on Product Management, Growth Strategy, "
                    "Retention, Activation, Product-Led Growth (PLG), Pricing, and Org design. "
                    "Please try asking a question related to these growth and product topics!"
                ),
                "sources": [],
                "is_grounded": False,
                "skill": "qna"
            }

        short_results = []
        for r in search_res["results"][:2]:
            r_copy = dict(r)
            words = r_copy.get("content", "").split()
            if len(words) > 180:
                r_copy["content"] = " ".join(words[:180]) + "..."
            short_results.append(r_copy)

        context_str = retriever.format_sources_for_prompt(short_results)

        history_str = ""
        if conversation_history:
            formatted_history = []
            for m in conversation_history[-4:]:
                formatted_history.append(f"{m['role'].capitalize()}: {m['content']}")
            history_str = "Recent Conversation History:\n" + "\n".join(formatted_history) + "\n\n"

        prompt = (
            f"{history_str}"
            f"Retrieved Transcript Passages from Lenny's Podcast:\n"
            f"{context_str}\n\n"
            f"User Question: {query}\n\n"
            f"Provide a clear, grounded answer citing specific guests and their insights:"
        )

        response_text = llm.generate(
            prompt=prompt,
            system_prompt=GROUNDED_QNA_SYSTEM_PROMPT,
            max_tokens=600
        )

        return {
            "content": response_text,
            "sources": search_res["results"],
            "is_grounded": True,
            "skill": "qna"
        }
