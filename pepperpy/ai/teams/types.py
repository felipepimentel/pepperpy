"""Team type definitions"""

from dataclasses import dataclass, field
from enum import Enum

from pepperpy.core.types import JsonDict


class TeamFramework(str, Enum):
    """Team framework types"""

    AUTOGEN = "autogen"
    CREW = "crew"
    LANGCHAIN = "langchain"


@dataclass
class TeamConfig:
    """Team configuration"""

    name: str
    framework: TeamFramework
    metadata: JsonDict = field(default_factory=dict)


@dataclass
class TeamResult:
    """Team execution result"""

    success: bool
    output: str | None
    metadata: JsonDict = field(default_factory=dict)
