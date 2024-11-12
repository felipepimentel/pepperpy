"""AI type definitions"""

from dataclasses import dataclass, field
from typing import Any, Dict, Literal, Optional, TypedDict


class UsageInfo(TypedDict):
    prompt_tokens: int
    completion_tokens: int
    total_tokens: int


@dataclass
class Message:
    role: Literal["user", "assistant", "system"]
    content: str
    usage: UsageInfo


@dataclass
class LLMResponse:
    content: str
    model: str
    usage: UsageInfo


@dataclass
class AIConfig:
    """Configuration for AI modules"""

    model: str
    api_key: str
    organization: Optional[str] = None
    extra_params: Dict[str, Any] = field(default_factory=dict)


@dataclass
class AIResponse:
    """Response from AI modules"""

    content: str
    raw_response: Dict[str, Any]
    model: str
    usage: Dict[str, int]
