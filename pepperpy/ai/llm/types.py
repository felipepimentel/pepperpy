"""LLM type definitions"""

from dataclasses import dataclass, field
from datetime import datetime
from typing import Dict, Optional

from pepperpy.core.types import JsonDict


@dataclass
class Message:
    """Chat message representation"""

    role: str
    content: str
    name: Optional[str] = None
    metadata: JsonDict = field(default_factory=dict)
    created_at: datetime = field(default_factory=datetime.utcnow)


@dataclass
class LLMResponse:
    """Response from LLM"""

    content: str
    model: str
    usage: Dict[str, int]
    finish_reason: Optional[str] = None
    metadata: JsonDict = field(default_factory=dict)
    created_at: datetime = field(default_factory=datetime.utcnow)
