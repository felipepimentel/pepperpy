"""Plugin configuration."""

from dataclasses import dataclass, field
from typing import Any

from ..base import BaseConfigData


@dataclass
class PluginConfig(BaseConfigData):
    """Plugin configuration."""

    # Required fields (herdado de BaseConfigData)
    name: str

    # Optional fields
    enabled: bool = True
    auto_load: bool = True
    search_paths: list[str] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)

    def validate(self) -> None:
        """Validate configuration."""
        if not isinstance(self.search_paths, list):
            raise ValueError("search_paths must be a list")

    def get_stats(self) -> dict[str, Any]:
        """Get configuration statistics."""
        return {
            "name": self.name,
            "enabled": self.enabled,
            "auto_load": self.auto_load,
            "search_paths_count": len(self.search_paths),
            "metadata": self.metadata,
        }


__all__ = ["PluginConfig"]
