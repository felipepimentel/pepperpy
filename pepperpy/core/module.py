"""Base module implementation"""

from dataclasses import asdict, dataclass, field
from typing import Any


@dataclass
class ModuleMetadata:
    """Module metadata"""

    name: str
    version: str
    description: str | None = None
    dependencies: list[str] | None = None
    config: dict[str, Any] | None = None


@dataclass
class BaseModule:
    """Base module implementation"""

    metadata: ModuleMetadata = field(init=False)
    config: Any = field(default=None)

    def __post_init__(self) -> None:
        """Post initialization"""
        self.metadata = ModuleMetadata(
            name=self.__class__.__name__,
            version="0.1.0",
            config=asdict(self.config) if self.config else None,
        )

    async def initialize(self) -> None:
        """Initialize module resources"""
        pass

    async def cleanup(self) -> None:
        """Cleanup module resources"""
        pass

    def get_config(self) -> dict[str, Any]:
        """Get module configuration"""
        if hasattr(self, "config"):
            return asdict(self.config)
        return {}
