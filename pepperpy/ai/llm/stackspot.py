from typing import Dict, List, Optional, AsyncGenerator
import httpx
import json
from dataclasses import dataclass, field

from .base import BaseLLM, LLMResponse, LLMException, ModelInfo
from .types import Message

@dataclass
class StackspotConfig:
    """Stackspot-specific configuration."""
    workspace_id: Optional[str] = None
    knowledge_source_ids: List[str] = field(default_factory=list)
    stack_id: Optional[str] = None
    conversation_id: Optional[str] = None
    quick_command: Optional[str] = None

class StackspotLLM(BaseLLM):
    """Stackspot AI LLM implementation."""

    def _initialize(self) -> None:
        """Initialize Stackspot-specific configurations."""
        super()._initialize()
        self.api_base = self.config.get(
            "STACKSPOT_API_BASE", 
            "https://api.stackspot.com/ai"
        )
        self.workspace_id = self.config.get("STACKSPOT_WORKSPACE_ID")
        self._client = httpx.AsyncClient(timeout=30.0)

    @property
    def available_models(self) -> Dict[str, ModelInfo]:
        """Available models in Stackspot AI."""
        return {
            "gpt-4": ModelInfo(
                name="gpt-4",
                provider="stackspot",
                context_window=8192,
                input_cost_per_1k=0.03,
                output_cost_per_1k=0.06,
                supports_functions=True
            ),
            "gpt-3.5-turbo": ModelInfo(
                name="gpt-3.5-turbo",
                provider="stackspot",
                context_window=4096,
                input_cost_per_1k=0.001,
                output_cost_per_1k=0.002
            )
        }

    async def _make_request(
        self, 
        endpoint: str, 
        data: Dict, 
        config: Optional[StackspotConfig] = None
    ) -> Dict:
        """Make an async request to Stackspot AI."""
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
            "X-Workspace-ID": (
                config.workspace_id or 
                self.workspace_id or 
                ""
            ),
        }

        try:
            response = await self._client.post(
                f"{self.api_base}/{endpoint}",
                headers=headers,
                json=data
            )
            response.raise_for_status()
            return response.json()
        except httpx.HTTPError as e:
            raise LLMException(f"Stackspot AI request failed: {str(e)}")

    async def achat(
        self, 
        messages: List[Message], 
        **kwargs
    ) -> LLMResponse[str]:
        """Async chat implementation."""
        config = StackspotConfig(**kwargs)
        
        data = {
            "messages": messages,
            "model": kwargs.get("model", "gpt-4"),
            "temperature": kwargs.get("temperature", 0.7),
        }

        if config.quick_command:
            endpoint = "quick-commands"
            data["quick_command"] = config.quick_command
        else:
            endpoint = "chat/completions"

        if config.knowledge_source_ids:
            data["knowledge_source_ids"] = config.knowledge_source_ids
        if config.stack_id:
            data["stack_id"] = config.stack_id
        if config.conversation_id:
            data["conversation_id"] = config.conversation_id
        if "max_tokens" in kwargs:
            data["max_tokens"] = kwargs["max_tokens"]

        result = await self._make_request(endpoint, data, config)

        return LLMResponse(
            content=result["choices"][0]["message"]["content"],
            usage=result["usage"],
            metadata={
                "conversation_id": result.get("conversation_id"),
                "model": data["model"],
                "quick_command": config.quick_command
            }
        )

    async def acomplete(self, prompt: str, **kwargs) -> LLMResponse[str]:
        """Async completion implementation."""
        return await self.achat(
            [{"role": "user", "content": prompt}],
            **kwargs
        )

    async def stream_chat(
        self, 
        messages: List[Message], 
        **kwargs
    ) -> AsyncGenerator[str, None]:
        """Stream chat responses."""
        config = StackspotConfig(**kwargs)
        data = {
            "messages": messages,
            "model": kwargs.get("model", "gpt-4"),
            "temperature": kwargs.get("temperature", 0.7),
            "stream": True
        }

        async with httpx.AsyncClient() as client:
            async with client.stream(
                "POST",
                f"{self.api_base}/chat/completions",
                headers=self._get_headers(config),
                json=data
            ) as response:
                async for line in response.aiter_lines():
                    if line.startswith("data: "):
                        chunk = json.loads(line[6:])
                        if chunk["choices"][0]["finish_reason"] is None:
                            yield chunk["choices"][0]["delta"]["content"]
