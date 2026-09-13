from typing import Dict, Any, List, Optional
from app.rag.retriever import retriever
from app.agent.prompts import SHIP30_ESSAY_SYSTEM_PROMPT
from app.llm.base import BaseLLM

class Ship30Skill:
    def __init__(self):
        pass

    def execute(
        self,
        query: str,
        llm: BaseLLM,
        conversation_history: Optional[List[Dict[str, str]]] = None
    ) -> Dict[str, Any]:
        # For essay requests, expand the query to retrieve comprehensive coverage
        cleaned_query = query.replace("turn this into an essay", "").replace("write an essay", "").replace("ship 30", "").strip()
        if not cleaned_query and conversation_history:
            # Infer topic from the previous user message
            for m in reversed(conversation_history):
                if m["role"] == "user":
                    cleaned_query = m["content"]
                    break

        if not cleaned_query:
            cleaned_query = "product retention and growth frameworks"

        search_res = retriever.search(cleaned_query, top_k=5, threshold=0.05)
        short_results = []
        for r in search_res["results"][:5]:
            r_copy = dict(r)
            words = r_copy.get("content", "").split()
            if len(words) > 300:
                r_copy["content"] = " ".join(words[:300]) + "..."
            short_results.append(r_copy)

        context_str = retriever.format_sources_for_prompt(short_results)

        prompt = (
            f"Retrieved Transcript Passages from Lenny's Podcast:\n"
            f"{context_str}\n\n"
            f"Assignment: Write a comprehensive, high-impact Ship 30 for 30 style essay based strictly on the above knowledge.\n"
            f"Topic / Prompt: {query}\n\n"
            f"Generate the complete essay following all Ship 30 for 30 principles:"
        )

        essay_text = llm.generate(
            prompt=prompt,
            system_prompt=SHIP30_ESSAY_SYSTEM_PROMPT,
            temperature=0.7,
            max_tokens=1800
        )

        return {
            "content": essay_text,
            "sources": search_res["results"],
            "is_grounded": True,
            "skill": "ship30",
            "word_count": len(essay_text.split())
        }
