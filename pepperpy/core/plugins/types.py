"""Plugin type definitions"""

from dataclasses import dataclass, field
from typing import Any, Protocol

from pepperpy.core.types import JsonDict


@dataclass
class PluginConfig:
    """Plugin configuration"""

    name: str
    enabled: bool = True
    auto_load: bool = True
    metadata: JsonDict = field(default_factory=dict)


class Plugin(Protocol):
    """Plugin protocol"""

    async def initialize(self) -> None:
        """Initialize plugin"""
        ...

    async def execute(self, **kwargs: Any) -> Any:
        """Execute plugin"""
        ...

    async def cleanup(self) -> None:
        """Cleanup plugin resources"""
        ...
