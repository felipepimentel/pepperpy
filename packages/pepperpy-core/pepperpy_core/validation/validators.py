"""Common validator implementations"""

import re
from typing import Any, Optional, Pattern, Sequence, Type, TypeVar

from pydantic import BaseModel, ValidationError

from .base import ValidationLevel, ValidationResult, Validator

T = TypeVar("T", bound=BaseModel)


class SchemaValidator(Validator[T, dict[str, Any]]):
    """Schema validation implementation"""

    def __init__(self, schema: Type[T]) -> None:
        """Initialize validator"""
        self.schema = schema

    async def validate(self, value: dict[str, Any]) -> ValidationResult:
        """Validate against schema"""
        try:
            self.schema.model_validate(value)
            return ValidationResult(
                is_valid=True, level=ValidationLevel.INFO, message="Schema validation passed"
            )
        except ValidationError as e:
            return ValidationResult(
                is_valid=False,
                level=ValidationLevel.ERROR,
                message=f"Schema validation failed: {e}",
                metadata={"error": str(e)},
            )

    async def validate_many(self, values: Sequence[dict[str, Any]]) -> Sequence[ValidationResult]:
        """Validate multiple values against schema"""
        return [await self.validate(value) for value in values]


class RegexValidator(Validator[str, str]):
    """Regex validation implementation"""

    def __init__(
        self,
        pattern: str | Pattern[str],
        message: Optional[str] = None,
        level: ValidationLevel = ValidationLevel.ERROR,
    ) -> None:
        """Initialize validator"""
        self.pattern = re.compile(pattern) if isinstance(pattern, str) else pattern
        self.message = message
        self.level = level

    async def validate(self, value: str) -> ValidationResult:
        """Validate value matches pattern"""
        if self.pattern.match(value):
            return ValidationResult(
                is_valid=True, level=ValidationLevel.INFO, message="Pattern validation passed"
            )

        return ValidationResult(
            is_valid=False,
            level=self.level,
            message=self.message or f"Value does not match pattern {self.pattern.pattern}",
            metadata={"pattern": self.pattern.pattern},
        )

    async def validate_many(self, values: Sequence[str]) -> Sequence[ValidationResult]:
        """Validate multiple values match pattern"""
        return [await self.validate(value) for value in values]


class LengthValidator(Validator[Any, Any]):
    """Length validation implementation"""

    def __init__(
        self,
        min_length: Optional[int] = None,
        max_length: Optional[int] = None,
        level: ValidationLevel = ValidationLevel.ERROR,
    ) -> None:
        """Initialize validator"""
        self.min_length = min_length
        self.max_length = max_length
        self.level = level

    async def validate(self, value: Any) -> ValidationResult:
        """Validate value length"""
        try:
            length = len(value)  # type: ignore
        except TypeError:
            return ValidationResult(
                is_valid=False,
                level=self.level,
                message="Value does not support length check",
                metadata={"type": str(type(value))},
            )

        if self.min_length is not None and length < self.min_length:
            return ValidationResult(
                is_valid=False,
                level=self.level,
                message=f"Length {length} is below minimum {self.min_length}",
                metadata={"length": length, "min_length": self.min_length},
            )

        if self.max_length is not None and length > self.max_length:
            return ValidationResult(
                is_valid=False,
                level=self.level,
                message=f"Length {length} is above maximum {self.max_length}",
                metadata={"length": length, "max_length": self.max_length},
            )

        return ValidationResult(
            is_valid=True,
            level=ValidationLevel.INFO,
            message="Length validation passed",
            metadata={"length": length},
        )

    async def validate_many(self, values: Sequence[Any]) -> Sequence[ValidationResult]:
        """Validate multiple value lengths"""
        return [await self.validate(value) for value in values]


class TypeValidator(Validator[Any, Any]):
    """Type validation implementation"""

    def __init__(
        self, expected_type: type | tuple[type, ...], level: ValidationLevel = ValidationLevel.ERROR
    ) -> None:
        """Initialize validator"""
        self.expected_type = expected_type
        self.level = level

    async def validate(self, value: Any) -> ValidationResult:
        """Validate value type"""
        if isinstance(value, self.expected_type):
            return ValidationResult(
                is_valid=True,
                level=ValidationLevel.INFO,
                message="Type validation passed",
                metadata={"type": str(type(value))},
            )

        return ValidationResult(
            is_valid=False,
            level=self.level,
            message=f"Expected type {self.expected_type}, got {type(value)}",
            metadata={"expected_type": str(self.expected_type), "actual_type": str(type(value))},
        )

    async def validate_many(self, values: Sequence[Any]) -> Sequence[ValidationResult]:
        """Validate multiple value types"""
        return [await self.validate(value) for value in values]


class RangeValidator(Validator[T, float]):
    """Range validation implementation"""

    def __init__(
        self,
        min_value: Optional[float] = None,
        max_value: Optional[float] = None,
        level: ValidationLevel = ValidationLevel.ERROR,
    ) -> None:
        """Initialize validator"""
        self.min_value = min_value
        self.max_value = max_value
        self.level = level

    async def validate(self, value: T) -> ValidationResult:
        """Validate value range"""
        if self.min_value is not None and value < self.min_value:
            return ValidationResult(
                is_valid=False,
                level=self.level,
                message=f"Value {value} is below minimum {self.min_value}",
                metadata={"value": value, "min_value": self.min_value},
            )

        if self.max_value is not None and value > self.max_value:
            return ValidationResult(
                is_valid=False,
                level=self.level,
                message=f"Value {value} is above maximum {self.max_value}",
                metadata={"value": value, "max_value": self.max_value},
            )

        return ValidationResult(
            is_valid=True,
            level=ValidationLevel.INFO,
            message="Range validation passed",
            metadata={"value": value},
        )

    async def validate_many(self, values: Sequence[T]) -> Sequence[ValidationResult]:
        """Validate multiple value ranges"""
        return [await self.validate(value) for value in values]


__all__ = [
    "LengthValidator",
    "RegexValidator",
    "SchemaValidator",
    "TypeValidator",
    "RangeValidator",
]
