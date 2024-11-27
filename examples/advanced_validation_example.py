"""Advanced validation example"""

import asyncio
from dataclasses import dataclass
from typing import Any

from pepperpy_core.module import BaseModule
from pepperpy_core.types import JsonDict
from pepperpy_core.validation import ValidationLevel, ValidationPipeline, ValidationResult
from pepperpy_core.validation.validators import (
    LengthValidator,
    RegexValidator,
    SchemaValidator,
    TypeValidator,
)
from pydantic import BaseModel


class UserSchema(BaseModel):
    """User data schema"""

    username: str
    email: str
    age: int
    tags: list[str] = []
    metadata: dict[str, Any] = {}


@dataclass
class ValidatorConfig:
    """Validator configuration"""

    name: str
    settings: JsonDict = {}


class UserValidator(BaseModule[ValidatorConfig]):
    """User data validator"""

    def __init__(self, config: ValidatorConfig) -> None:
        super().__init__(config)
        self._pipeline = ValidationPipeline[Any, dict[str, Any]]()

    async def _initialize(self) -> None:
        """Initialize validator"""
        print(f"Initializing validator {self.config.name}...")

        # Add validators to pipeline
        self._pipeline.add_validator(SchemaValidator(UserSchema))

        # Username validation
        self._pipeline.add_validator(
            RegexValidator(
                r"^[a-zA-Z0-9_]{3,20}$",
                message="Username must be 3-20 characters, alphanumeric and underscore only",
            )
        )

        # Email validation
        self._pipeline.add_validator(
            RegexValidator(
                r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$", message="Invalid email format"
            )
        )

        # Age validation
        self._pipeline.add_validator(TypeValidator(int, level=ValidationLevel.ERROR))

        # Tags validation
        self._pipeline.add_validator(
            LengthValidator(
                max_length=5, message="Maximum 5 tags allowed", level=ValidationLevel.WARNING
            )
        )

    async def _cleanup(self) -> None:
        """Cleanup validator"""
        print(f"Cleaning up validator {self.config.name}...")

    def _format_results(self, results: list[ValidationResult]) -> None:
        """Format and print validation results"""
        for result in results:
            status = "✓" if result.valid else "✗"
            level_symbol = {
                ValidationLevel.INFO: "ℹ",
                ValidationLevel.WARNING: "⚠",
                ValidationLevel.ERROR: "✖",
            }[result.level]

            print(f"{status} {level_symbol} [{result.level}] {result.message}")
            if result.metadata:
                print(f"  Metadata: {result.metadata}")

    async def validate(self, data: dict[str, Any]) -> bool:
        """Validate user data"""
        self._ensure_initialized()

        print(f"\nValidating user data: {data}")
        results = await self._pipeline.validate(data)
        self._format_results(results)

        return all(r.valid for r in results)


async def main() -> None:
    """Run example"""
    # Create validator
    config = ValidatorConfig(name="user_validator")
    validator = UserValidator(config)

    try:
        # Initialize
        await validator.initialize()

        # Test data
        test_users = [
            {
                # Valid user
                "username": "john_doe",
                "email": "john@example.com",
                "age": 30,
                "tags": ["user", "premium"],
                "metadata": {"joined": "2024-01-01"},
            },
            {
                # Invalid username
                "username": "j@hn",
                "email": "john@example.com",
                "age": 30,
            },
            {
                # Invalid email
                "username": "jane_doe",
                "email": "not-an-email",
                "age": 25,
            },
            {
                # Too many tags
                "username": "tag_master",
                "email": "tags@example.com",
                "age": 28,
                "tags": ["tag1", "tag2", "tag3", "tag4", "tag5", "tag6"],
            },
        ]

        # Validate each user
        for user in test_users:
            is_valid = await validator.validate(user)
            print(f"Validation {'passed' if is_valid else 'failed'}\n")

    finally:
        # Cleanup
        await validator.cleanup()


if __name__ == "__main__":
    asyncio.run(main())
