from dataclasses import dataclass, field
from typing import Dict, List, Optional

import requests

from .base import BaseLLM, LLMOptions


@dataclass
class OpenRouterOptions(LLMOptions):
    """Opções específicas para OpenRouter."""

    transforms: List[str] = field(default_factory=list)
    route: Optional[str] = None
    top_p: float = 1.0
    top_k: int = 40
    presence_penalty: float = 0.0
    frequency_penalty: float = 0.0


class OpenRouterLLM(BaseLLM):
    """Implementação do LLM usando OpenRouter."""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.api_base = "https://openrouter.ai/api/v1"
        self.default_model = self.config.get(
            "OPENROUTER_MODEL", "anthropic/claude-3-sonnet"
        )

    def _chat_implementation(
        self, messages: List[Dict[str, str]], options: OpenRouterOptions
    ) -> Dict:
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "HTTP-Referer": self.config.get("APP_URL", "http://localhost"),
            "X-Title": self.config.get("APP_NAME", "Pepperpy Application"),
            "Content-Type": "application/json",
        }

        data = {
            "messages": messages,
            "model": options.model or self.default_model,
            "temperature": options.temperature,
        }

        if options.max_tokens:
            data["max_tokens"] = options.max_tokens
        if options.transforms:
            data["transforms"] = options.transforms
        if options.route:
            data["route"] = options.route
        if options.top_p != 1.0:
            data["top_p"] = options.top_p
        if options.top_k != 40:
            data["top_k"] = options.top_k
        if options.presence_penalty != 0.0:
            data["presence_penalty"] = options.presence_penalty
        if options.frequency_penalty != 0.0:
            data["frequency_penalty"] = options.frequency_penalty

        response = requests.post(
            f"{self.api_base}/chat/completions", headers=headers, json=data
        )
        response.raise_for_status()

        result = response.json()
        return {
            "content": result["choices"][0]["message"]["content"],
            "usage": result.get("usage", {}),
            "metadata": {
                "model": data["model"],
                "route": options.route,
                "transforms": options.transforms,
            },
        }
