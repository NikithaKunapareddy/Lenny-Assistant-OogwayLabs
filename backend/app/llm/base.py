from abc import ABC, abstractmethod
from typing import List, Dict, Any, Generator, Optional

class BaseLLM(ABC):
    @abstractmethod
    def generate(
        self,
        prompt: str,
        system_prompt: Optional[str] = None,
        temperature: float = 0.7,
        max_tokens: int = 2048
    ) -> str:
        """Generate full completion text."""
        pass

    @abstractmethod
    def stream(
        self,
        prompt: str,
        system_prompt: Optional[str] = None,
        temperature: float = 0.7,
        max_tokens: int = 2048
    ) -> Generator[str, None, None]:
        """Stream completion text tokens."""
        pass

    @abstractmethod
    def is_available(self) -> bool:
        """Check if the model provider service is reachable."""
        pass
