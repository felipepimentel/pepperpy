"""Team configuration module"""

from enum import Enum

from pydantic import BaseModel, Field

from pepperpy.core.types import JsonDict


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
