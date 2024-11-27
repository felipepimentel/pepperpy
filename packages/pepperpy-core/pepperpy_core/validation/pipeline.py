"""Validation pipeline implementation"""

from typing import Generic, Optional, Sequence, TypeVar

from .base import ValidationResult, Validator
from .config import ValidationConfig

T = TypeVar("T")
V = TypeVar("V")


class ValidationPipeline(Generic[T, V]):
    """Validation pipeline implementation"""

    def __init__(self, config: Optional[ValidationConfig] = None) -> None:
        self.config = config or ValidationConfig()
        self._validators: list[Validator[T, V]] = []

    def add_validator(self, validator: Validator[T, V]) -> None:
        """Add validator to pipeline"""
        self._validators.append(validator)

    async def validate(self, value: V) -> list[ValidationResult]:
        """Run validation pipeline on single value"""
        results = []

        for validator in self._validators:
            result = await validator.validate(value)
            results.append(result)

            if not result.is_valid and self.config.fail_fast:
                break

            if len(results) >= self.config.max_errors:
                break

        return results

    async def validate_many(self, values: Sequence[V]) -> list[ValidationResult]:
        """Run validation pipeline on multiple values"""
        results = []

        for value in values:
            value_results = await self.validate(value)
            results.extend(value_results)

            if any(not r.is_valid for r in value_results) and self.config.fail_fast:
                break

            if len(results) >= self.config.max_errors:
                break

        return results


__all__ = [
    "ValidationPipeline",
]
