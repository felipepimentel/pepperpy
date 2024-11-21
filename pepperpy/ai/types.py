"""AI type definitions"""

from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any, Sequence

from pepperpy.core.types import JsonDict


class MessageRole(str, Enum):
    """Message role types"""

    SYSTEM = "system"
    USER = "user"
    ASSISTANT = "assistant"
    FUNCTION = "function"


@dataclass
class AIMessage:
    """AI message"""

    role: MessageRole
    content: str
    timestamp: datetime = field(default_factory=datetime.now)
    metadata: JsonDict = field(default_factory=dict)


@dataclass
class AIResponse:
    """AI response"""

    content: str
    messages: Sequence[AIMessage]
    usage: JsonDict = field(default_factory=dict)
    metadata: JsonDict = field(default_factory=dict)


@dataclass
class AIFunction:
    """AI function definition"""

    name: str
    description: str
    parameters: dict[str, Any]
    is_required: bool = False
    metadata: JsonDict = field(default_factory=dict)
