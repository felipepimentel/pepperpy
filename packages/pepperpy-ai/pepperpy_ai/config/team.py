"""Team configuration module"""

from enum import Enum

from bko.core.types import JsonDict
from pydantic import BaseModel, Field


class TeamFramework(str, Enum):
    """Enumeration for team frameworks"""

    AUTOGEN = "autogen"
    CREW = "crew"
    LANGCHAIN = "langchain"


class TeamConfig(BaseModel):
    """Configuration for AI Teams"""

    name: str
    framework: TeamFramework
    metadata: JsonDict = Field(default_factory=dict)
    enabled: bool = Field(default=True)

    class Config:
        """Pydantic configuration"""

        frozen = True
