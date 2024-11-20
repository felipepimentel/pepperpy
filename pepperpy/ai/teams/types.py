"""Team type definitions"""

from dataclasses import dataclass, field
from enum import Enum
from typing import Any

from pepperpy.core.types import JsonDict


class TeamFramework(str, Enum):
    """Supported team frameworks"""

    AUTOGEN = "autogen"
    CREW = "crew"
    LANGCHAIN = "langchain"


@dataclass
class TeamConfig:
    """Team configuration"""

    framework: TeamFramework
    name: str
    description: str | None = None
    max_iterations: int = 10
    timeout: float = 300.0
    parallel_execution: bool = True
    review_required: bool = True
    metadata: JsonDict = field(default_factory=dict)


@dataclass
class TeamResult:
    """Team execution result"""

    success: bool
    output: Any
    metadata: JsonDict = field(default_factory=dict) 