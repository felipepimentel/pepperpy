"""Base validation types and interfaces"""

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Generic, Sequence, TypeVar

from ..base.types import JsonDict
from ..utils.datetime import utc_now


class ValidationLevel(str, Enum):
    """Validation severity levels"""

    INFO = "info"
    WARNING = "warning"
    ERROR = "error"


@dataclass
class ValidationResult:
    """Validation result"""

    is_valid: bool
    level: ValidationLevel = ValidationLevel.INFO
    message: str = ""
    path: str = ""
    timestamp: datetime = field(default_factory=utc_now)
    metadata: JsonDict = field(default_factory=dict)

    @property
    def valid(self) -> bool:
        """Alias for is_valid"""
        return self.is_valid


T = TypeVar("T")
V = TypeVar("V")


class Validator(ABC, Generic[T, V]):
    """Base validator interface"""

    @abstractmethod
    async def validate(self, value: V) -> ValidationResult:
        """Validate single value"""
        ...

    @abstractmethod
    async def validate_many(self, values: Sequence[V]) -> Sequence[ValidationResult]:
        """Validate multiple values"""
        ...


__all__ = [
    "ValidationLevel",
    "ValidationResult",
    "Validator",
]
