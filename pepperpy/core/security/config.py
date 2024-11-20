"""Security configuration"""

from dataclasses import dataclass, field

from pepperpy.core.types import JsonDict


@dataclass
class SecurityConfig:
    """Security configuration"""

    name: str
    enabled: bool = True
    metadata: JsonDict = field(default_factory=dict)
