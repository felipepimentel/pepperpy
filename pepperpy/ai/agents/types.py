"""Agent type definitions"""

from dataclasses import dataclass, field
from typing import Any

from pepperpy.core.types import JsonDict


@dataclass
class AgentResponse:
    """Agent response"""
    content: str
    metadata: JsonDict = field(default_factory=dict)


@dataclass
class AgentContext:
    """Agent execution context"""
    task: str
    metadata: JsonDict = field(default_factory=dict)
    parameters: dict[str, Any] = field(default_factory=dict)
