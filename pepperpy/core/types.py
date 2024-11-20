"""Core type definitions"""

from dataclasses import dataclass, field
from typing import Any

JsonDict = dict[str, Any]


@dataclass
class ModuleConfig:
    """Base module configuration"""

    name: str
    enabled: bool = True
    metadata: JsonDict = field(default_factory=dict)


class CoreError(Exception):
    """Base error for core module"""

    def __init__(self, message: str, cause: Exception | None = None) -> None:
        super().__init__(message)
        self.cause = cause
