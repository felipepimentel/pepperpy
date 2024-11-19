"""Core validation module"""

from abc import ABC, abstractmethod
from typing import Any, TypeVar

from .exceptions import ValidationError
from .types import ValidationResult
from .validators import (
    DataValidator,
    NumberValidator,
    StringValidator,
    TypeValidator,
)

T = TypeVar("T")


class Validator(ABC):
    """Base validator interface"""

    @abstractmethod
    async def validate(self, value: Any) -> ValidationResult:
        """Validate a value"""
        pass


__all__ = [
    "Validator",
    "ValidationError",
    "ValidationResult",
    "DataValidator",
    "NumberValidator",
    "StringValidator",
    "TypeValidator",
] 