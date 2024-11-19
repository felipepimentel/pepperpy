"""Configuration module"""

from dataclasses import asdict
from typing import Any, Protocol


class ModuleConfig(Protocol):
    """Module configuration protocol"""

    def to_dict(self) -> dict[str, Any]:
        """Convert configuration to dictionary"""
        ...


def config_to_dict(config: Any) -> dict[str, Any]:
    """Convert configuration to dictionary"""
    if hasattr(config, "to_dict"):
        return config.to_dict()
    if hasattr(config, "__dataclass_fields__"):
        return asdict(config)
    if isinstance(config, dict):
        return config
    return {} 