import os
import requests
from typing import Generator, Optional
from app.llm.base import BaseLLM
from app.core.config import settings

class AnthropicClient(BaseLLM):
    def __init__(self, api_key: Optional[str] = None, model: Optional[str] = None):
        self.api_key = api_key or settings.ANTHROPIC_API_KEY
        self.model = model or settings.ANTHROPIC_MODEL

    def is_available(self) -> bool:
        return bool(self.api_key and len(self.api_key) > 10)

    def generate(
        self,
        prompt: str,
        system_prompt: Optional[str] = None,
        temperature: float = 0.7,
        max_tokens: int = 2048
    ) -> str:
        headers = {
            "x-api-key": self.api_key,
            "anthropic-version": "2023-06-01",
            "content-type": "application/json"
        }
        payload = {
            "model": self.model,
            "max_tokens": max_tokens,
            "temperature": temperature,
            "system": system_prompt or "",
            "messages": [{"role": "user", "content": prompt}]
        }
        resp = requests.post("https://api.anthropic.com/v1/messages", headers=headers, json=payload, timeout=60)
        resp.raise_for_status()
        data = resp.json()
        return data["content"][0]["text"]

    def stream(
        self,
        prompt: str,
        system_prompt: Optional[str] = None,
        temperature: float = 0.7,
        max_tokens: int = 2048
    ) -> Generator[str, None, None]:
        # Fallback to single yield if streaming endpoint requires complex SSE parsing
        full_text = self.generate(prompt, system_prompt, temperature, max_tokens)
        words = full_text.split(" ")
        for i, word in enumerate(words):
            yield word + (" " if i < len(words) - 1 else "")

class OpenAIClient(BaseLLM):
    def __init__(self, api_key: Optional[str] = None, model: Optional[str] = None):
        self.api_key = api_key or settings.OPENAI_API_KEY
        self.model = model or settings.OPENAI_MODEL

    def is_available(self) -> bool:
        return bool(self.api_key and len(self.api_key) > 10)

    def generate(
        self,
        prompt: str,
        system_prompt: Optional[str] = None,
        temperature: float = 0.7,
        max_tokens: int = 2048
    ) -> str:
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        messages.append({"role": "user", "content": prompt})

        payload = {
            "model": self.model,
            "messages": messages,
            "temperature": temperature,
            "max_tokens": max_tokens
        }
        resp = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload, timeout=60)
        resp.raise_for_status()
        data = resp.json()
        return data["choices"][0]["message"]["content"]

    def stream(
        self,
        prompt: str,
        system_prompt: Optional[str] = None,
        temperature: float = 0.7,
        max_tokens: int = 2048
    ) -> Generator[str, None, None]:
        full_text = self.generate(prompt, system_prompt, temperature, max_tokens)
        words = full_text.split(" ")
        for i, word in enumerate(words):
            yield word + (" " if i < len(words) - 1 else "")
