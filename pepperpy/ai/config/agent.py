"""Agent configuration"""

from pydantic import BaseModel, Field

from pepperpy.ai.roles import AgentRole
from pepperpy.core.types import JsonDict


class AgentConfig(BaseModel):
    """Agent configuration"""

    name: str
    role: AgentRole
    enabled: bool = Field(default=True)
    max_retries: int = Field(default=3, ge=0)
    timeout: float = Field(default=60.0, gt=0)
    metadata: JsonDict = Field(default_factory=dict)

    class Config:
        """Pydantic config"""

        frozen = True
