from typing import Dict, Any, Optional
from app.llm.base import BaseLLM
from app.llm.ollama_client import OllamaClient
from app.llm.cloud_client import AnthropicClient, OpenAIClient
from app.llm.mock_client import MockGroundedClient
from app.core.config import settings

class LLMManager:
    def __init__(self):
        self.active_provider = settings.DEFAULT_MODEL_PROVIDER.lower()
        self._providers: Dict[str, BaseLLM] = {
            "ollama": OllamaClient(),
            "anthropic": AnthropicClient(),
            "openai": OpenAIClient(),
            "mock": MockGroundedClient()
        }

    def get_client(self, provider_override: Optional[str] = None) -> BaseLLM:
        provider = (provider_override or self.active_provider).lower()
        client = self._providers.get(provider)
        if not client:
            client = self._providers["mock"]

        # If requested client is unavailable (e.g. Ollama is down or no cloud key), fall back gracefully
        if not client.is_available():
            if provider == "ollama":
                print(f"[!] Ollama is currently unavailable on {settings.OLLAMA_BASE_URL}. Falling back to internal Grounded Engine.")
            elif provider in ["anthropic", "openai"]:
                print(f"[!] Cloud provider '{provider}' missing API key or offline. Falling back to internal Grounded Engine.")
            return self._providers["mock"]

        return client

    def set_active_provider(self, provider: str) -> bool:
        provider = provider.lower()
        if provider in self._providers:
            self.active_provider = provider
            return True
        return False

    def list_providers(self) -> Dict[str, Any]:
        return {
            "active_provider": self.active_provider,
            "providers": [
                {
                    "id": "ollama",
                    "name": f"Ollama Local ({settings.OLLAMA_MODEL})",
                    "type": "local",
                    "available": self._providers["ollama"].is_available(),
                    "recommended_for": "Local privacy & zero API cost (Mandatory demo requirement)"
                },
                {
                    "id": "anthropic",
                    "name": f"Anthropic Claude ({settings.ANTHROPIC_MODEL})",
                    "type": "cloud",
                    "available": self._providers["anthropic"].is_available(),
                    "recommended_for": "High-reasoning cloud intelligence"
                },
                {
                    "id": "openai",
                    "name": f"OpenAI ({settings.OPENAI_MODEL})",
                    "type": "cloud",
                    "available": self._providers["openai"].is_available(),
                    "recommended_for": "Cloud production deployment"
                },
                {
                    "id": "mock",
                    "name": "Lenny High-Fidelity Grounded Engine (Offline Fallback)",
                    "type": "internal",
                    "available": True,
                    "recommended_for": "Deterministic zero-dependency testing"
                }
            ]
        }

llm_manager = LLMManager()
