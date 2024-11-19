"""AI types and constants"""

from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Literal

Role = Literal["user", "assistant", "system"]


@dataclass
class AIMessage:
    """AI message"""
    role: Role
    content: str
    metadata: dict[str, Any] = field(default_factory=dict)
    created_at: datetime = field(default_factory=datetime.now)


@dataclass
class AIResponse:
    """AI response"""
    content: str
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass
class AIConfig:
    """AI configuration"""
    model: str
    temperature: float = 0.7
    max_tokens: int = 1000
    stop_sequences: list[str] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)
