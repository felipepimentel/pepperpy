"""Team type definitions"""

from dataclasses import dataclass, field

from pepperpy.core.types import JsonDict

from .types import AgentConfig


@dataclass
class TeamConfig:
    """Team configuration"""

    name: str
    description: str | None = None
    agent_configs: dict[str, AgentConfig] = field(default_factory=dict)
    metadata: JsonDict = field(default_factory=dict)
