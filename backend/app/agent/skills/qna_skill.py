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
        # Search knowledge base
        search_res = retriever.search(query, top_k=4, threshold=self.threshold, guest_filter=guest_filter)

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

        context_str = retriever.format_sources_for_prompt(search_res["results"])

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

        response_text = llm.generate(prompt=prompt, system_prompt=GROUNDED_QNA_SYSTEM_PROMPT)

        return {
            "content": response_text,
            "sources": search_res["results"],
            "is_grounded": True,
            "skill": "qna"
        }
