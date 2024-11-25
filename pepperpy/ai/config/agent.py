"""Agent configuration"""

from pydantic import BaseModel, Field

from pepperpy.ai.roles import AgentRole
from pepperpy.core.types import JsonDict


class AgentConfig(BaseModel):
    """Agent configuration"""

    name: str
    role: AgentRole
    metadata: JsonDict = Field(default_factory=dict)

    class Config:
        """Pydantic config"""

        frozen = True
