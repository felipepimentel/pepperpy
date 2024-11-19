"""Autogen type definitions"""

from dataclasses import dataclass, field
from typing import Any, TypedDict

from ..types import AIMessage


class AutogenMessage(TypedDict):
    """Autogen message type"""

    role: str
    content: str
    metadata: dict[str, Any]


@dataclass
class AutogenConfig:
    """Autogen configuration"""

    model: str
    temperature: float = 0.7
    max_tokens: int = 1000
    stop_sequences: list[str] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass
class AutogenResponse:
    """Autogen response"""

    content: str
    messages: list[AIMessage] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)
