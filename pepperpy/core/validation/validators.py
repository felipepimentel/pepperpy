"""Common validator implementations"""

from typing import Any, Sequence, Type, TypeVar

from pydantic import BaseModel, ValidationError

from .base import ValidationResult, Validator

T = TypeVar("T", bound=BaseModel)


class PydanticValidator(Validator[T, dict[str, Any]]):
    """Validator using Pydantic models"""

    def __init__(self, model: Type[T]):
        self.model = model

    async def validate(self, value: dict[str, Any]) -> ValidationResult[T]:
        """Validate single value"""
        try:
            instance = self.model(**value)
            return ValidationResult(is_valid=True, value=instance)
        except ValidationError as e:
            return ValidationResult(is_valid=False, errors=[str(err) for err in e.errors()])

    async def validate_many(
        self, values: Sequence[dict[str, Any]]
    ) -> Sequence[ValidationResult[T]]:
        """Validate multiple values"""
        return [await self.validate(value) for value in values]


class TypeValidator(Validator[Any, Any]):
    """Type validator"""

    def __init__(self, expected_type: Type[Any]):
        self.expected_type = expected_type

    async def validate(self, value: Any) -> ValidationResult[Any]:
        """Validate value type"""
        if isinstance(value, self.expected_type):
            return ValidationResult(is_valid=True, value=value)
        return ValidationResult(
            is_valid=False,
            errors=[f"Expected type {self.expected_type.__name__}, got {type(value).__name__}"],
        )

    async def validate_many(self, values: Sequence[Any]) -> Sequence[ValidationResult[Any]]:
        """Validate multiple values"""
        return [await self.validate(value) for value in values]
