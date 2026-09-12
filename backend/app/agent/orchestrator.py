import time
import re
from typing import Dict, Any, List, Optional
from app.agent.skills.qna_skill import QnASkill
from app.agent.skills.ship30_skill import Ship30Skill
from app.agent.skills.artifact_skill import ArtifactSkill
from app.llm.factory import llm_manager
from app.core.config import settings

class AgentOrchestrator:
    def __init__(self):
        self.qna_skill = QnASkill(threshold=settings.RAG_GROUNDING_THRESHOLD)
        self.ship30_skill = Ship30Skill()
        self.artifact_skill = ArtifactSkill()

    def route_intent(self, query: str) -> str:
        """
        Classifies incoming query intent into:
        - 'ship30': requests to write an essay/article/deep dive
        - 'artifact': requests to create/generate an interactive framework/html/checklist/matrix
        - 'qna': default grounded conversational question answering
        """
        q = query.lower().strip()

        # Check essay / Ship 30 triggers
        if any(term in q for term in [
            "essay", "article", "ship 30", "write a piece", "turn this into an essay",
            "deep dive post", "1250 words", "write an article"
        ]):
            return "ship30"

        # Questions asking to "explain", "what is", "tell me about" a framework should be QnA!
        is_explanation_query = any(q.startswith(prefix) for prefix in [
            "explain", "what is", "what are", "tell me about", "describe", "how does", "how do"
        ])

        # Action-oriented creation triggers using regex (handles intermediate words)
        is_artifact_request = bool(re.search(
            r'\b(create|generate|build|make|design)\b.*\b(framework|checklist|artifact|matrix|template|canvas|visual model|html)\b',
            q
        ))

        if is_artifact_request and not is_explanation_query:
            return "artifact"

        if "html" in q and any(w in q for w in ["generate", "create", "build", "code"]):
            return "artifact"

        return "qna"

    def execute(
        self,
        query: str,
        conversation_history: Optional[List[Dict[str, str]]] = None,
        model_provider_override: Optional[str] = None
    ) -> Dict[str, Any]:
        start_time = time.time()
        intent = self.route_intent(query)
        llm = llm_manager.get_client(model_provider_override)

        if intent == "ship30":
            result = self.ship30_skill.execute(query, llm, conversation_history)
        elif intent == "artifact":
            result = self.artifact_skill.execute(query, llm, conversation_history)
        else:
            result = self.qna_skill.execute(query, llm, conversation_history)

        latency_ms = int((time.time() - start_time) * 1000)
        result["latency_ms"] = latency_ms
        result["routed_intent"] = intent
        result["model_provider"] = model_provider_override or llm_manager.active_provider

        return result

# Singleton orchestrator
agent_orchestrator = AgentOrchestrator()
