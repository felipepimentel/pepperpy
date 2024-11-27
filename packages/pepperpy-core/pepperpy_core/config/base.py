"""Base configuration implementation"""

from typing import Any, Protocol

from pydantic import BaseModel, ConfigDict, Field

from ..base.types import JsonDict


class BaseConfig(BaseModel):
    """Base configuration"""

    metadata: JsonDict = Field(default_factory=dict)
    model_config = ConfigDict(extra="allow", arbitrary_types_allowed=True)


class ConfigProtocol(Protocol):
    """Configuration protocol"""

    def to_dict(self) -> dict[str, Any]:
        """Convert to dictionary"""
        ...

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "ConfigProtocol":
        """Create from dictionary"""
        ...


__all__ = [
    "BaseConfig",
    "ConfigProtocol",
]
