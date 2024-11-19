"""Validation implementations"""

from typing import Any, Type, TypeVar

from .exceptions import ValidationError
from .types import ValidationResult

T = TypeVar("T")


class DataValidator:
    """Generic data validator"""

    async def validate_type(self, value: Any, expected_type: Type[T]) -> ValidationResult:
        """Validate value type"""
        if not isinstance(value, expected_type):
            raise ValidationError(
                f"Expected type {expected_type.__name__}, got {type(value).__name__}"
            )
        return ValidationResult(valid=True)


class NumberValidator:
    """Number validation utilities"""

    async def validate_range(
        self, value: float, min_value: float | None = None, max_value: float | None = None
    ) -> ValidationResult:
        """Validate number range"""
        if min_value is not None and value < min_value:
            raise ValidationError(f"Value {value} is less than minimum {min_value}")
        if max_value is not None and value > max_value:
            raise ValidationError(f"Value {value} is greater than maximum {max_value}")
        return ValidationResult(valid=True)


class StringValidator:
    """String validation utilities"""

    async def validate_length(
        self, value: str, min_length: int | None = None, max_length: int | None = None
    ) -> ValidationResult:
        """Validate string length"""
        if min_length is not None and len(value) < min_length:
            raise ValidationError(f"String length {len(value)} is less than minimum {min_length}")
        if max_length is not None and len(value) > max_length:
            raise ValidationError(f"String length {len(value)} is greater than maximum {max_length}")
        return ValidationResult(valid=True)


class TypeValidator:
    """Type validation utilities"""

    async def validate_instance(self, value: Any, expected_type: Type[T]) -> ValidationResult:
        """Validate type instance"""
        if not isinstance(value, expected_type):
            raise ValidationError(
                f"Expected instance of {expected_type.__name__}, got {type(value).__name__}"
            )
        return ValidationResult(valid=True) 