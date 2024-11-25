"""AI types module"""

from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Dict, List, Optional


class Role(str, Enum):
    """Message role types"""

    SYSTEM = "system"
    USER = "user"
    ASSISTANT = "assistant"


@dataclass
class Message:
    """AI message"""

    role: Role
    content: str


@dataclass
class AIResponse:
    """AI response"""

    content: str
    role: Role = Role.ASSISTANT
    model: str = "default"
    usage: Dict[str, int] = field(default_factory=lambda: {"total_tokens": 0})
    messages: Optional[List[Message]] = None
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class AIContext:
    """AI context"""

    messages: List[Message]
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class AIResult:
    """AI result"""

    response: AIResponse
    context: AIContext
    metadata: Dict[str, Any] = field(default_factory=dict)


class ProviderType(str, Enum):
    """Provider types"""

    OPENAI = "openai"
    ANTHROPIC = "anthropic"
    OPENROUTER = "openrouter"
    STACKSPOT = "stackspot"


# Aliases for backward compatibility
MessageRole = Role
AIMessage = Message
