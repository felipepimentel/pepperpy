"""Configuration types."""

from dataclasses import dataclass, field
from typing import Any

from pydantic import BaseModel

from ..base import BaseData
from ..types import JsonDict


@dataclass
class ConfigData(BaseData):
    """Base configuration data."""

    enabled: bool = True
    settings: JsonDict = field(default_factory=dict)
    defaults: JsonDict = field(default_factory=dict)
    overrides: JsonDict = field(default_factory=dict)


@dataclass
class ConfigSource:
    """Configuration source."""

    name: str
    path: str
    format: str = "json"
    required: bool = True
    metadata: JsonDict = field(default_factory=dict)


@dataclass
class ConfigState:
    """Configuration state."""

    loaded: bool = False
    validated: bool = False
    sources: list[ConfigSource] = field(default_factory=list)
    errors: list[str] = field(default_factory=list)

    def get_stats(self) -> dict[str, Any]:
        """Get state statistics."""
        return {
            "loaded": self.loaded,
            "validated": self.validated,
            "sources": len(self.sources),
            "errors": len(self.errors),
        }


class ConfigManagerConfig(BaseModel):
    """Configuration manager configuration."""

    name: str
    config_path: str
    enabled: bool = True


__all__ = [
    "ConfigData",
    "ConfigSource",
    "ConfigState",
    "ConfigManagerConfig",
]
