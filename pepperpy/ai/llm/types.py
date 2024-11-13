"""LLM type definitions"""

from dataclasses import dataclass, field
from typing import Any, Dict, Optional


@dataclass
class Message:
    """Chat message representation"""

    role: str
    content: str
    name: Optional[str] = None
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class LLMResponse:
    """Response from LLM"""

    content: str
    model: str
    usage: Dict[str, int]
    metadata: Dict[str, Any] = field(default_factory=dict)
