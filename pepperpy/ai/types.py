"""AI type definitions"""

from dataclasses import dataclass, field
from typing import Any

from pepperpy.core.types import JsonDict

from .config import AIConfig


@dataclass
class AIResponse:
    """AI response"""

    content: str
    model: str | None = None
    usage: dict[str, int] | None = None
    metadata: JsonDict = field(default_factory=dict)


@dataclass
class AIMessage:
    """AI message"""

    role: str
    content: str
    name: str | None = None
    metadata: JsonDict = field(default_factory=dict)


@dataclass
class AgentConfig:
    """Agent configuration"""

    name: str
    role: str
    ai_config: AIConfig  # Usando AIConfig do módulo config
    metadata: JsonDict = field(default_factory=dict)
    params: dict[str, Any] = field(default_factory=dict)
