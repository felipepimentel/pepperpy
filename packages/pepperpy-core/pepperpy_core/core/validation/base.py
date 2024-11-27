"""Base validation implementations"""

from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Generic, Sequence, TypeVar

from ..exceptions import PepperPyError

T = TypeVar("T")
V = TypeVar("V")


class ValidationError(PepperPyError):
    """Validation error"""

    pass


@dataclass
class ValidationResult(Generic[T]):
    """Validation result"""

    is_valid: bool
    value: T | None = None
    errors: Sequence[str] = ()


class Validator(ABC, Generic[T, V]):
    """Base validator interface"""

    @abstractmethod
    async def validate(self, value: V) -> ValidationResult[T]:
        """Validate a value"""
        pass

    @abstractmethod
    async def validate_many(self, values: Sequence[V]) -> Sequence[ValidationResult[T]]:
        """Validate multiple values"""
        pass
