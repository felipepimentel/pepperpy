"""Provider type definitions"""

from dataclasses import dataclass
from datetime import datetime
from typing import Any


@dataclass
class Message:
    """Chat message"""
    role: str
    content: str
    name: str | None = None
    metadata: dict[str, Any] | None = None


@dataclass
class ProviderResponse:
    """Provider response"""
    content: str
    model: str
    created_at: datetime
    metadata: dict[str, Any] 