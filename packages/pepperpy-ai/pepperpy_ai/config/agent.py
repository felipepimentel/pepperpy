"""Agent configuration"""

from bko.ai.roles import AgentRole
from bko.core.types import JsonDict
from pydantic import BaseModel, Field


class AgentConfig(BaseModel):
    """Agent configuration"""

    name: str
    role: AgentRole
    metadata: JsonDict = Field(default_factory=dict)

    class Config:
        """Pydantic config"""

        frozen = True
