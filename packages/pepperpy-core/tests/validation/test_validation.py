"""Test validation functionality"""

from typing import Any

from pepperpy_core.validation import (
    ValidationResult,
    Validator,
)


class TestValidator(Validator[str, Any]):
    """Test validator implementation"""

    async def validate(self, value: Any) -> ValidationResult:
        return ValidationResult(is_valid=True)

    async def validate_many(self, values: list[Any]) -> list[ValidationResult]:
        return [await self.validate(value) for value in values]
