"""Example demonstrating validation functionality"""

import asyncio
from typing import Any, List

from pepperpy_core.validation import (
    LengthValidator,
    SchemaValidator,
    TypeValidator,
    ValidationPipeline,
)
from pydantic import BaseModel, Field


class UserData(BaseModel):
    """User data model for validation"""

    username: str = Field(min_length=3, max_length=20)
    age: int = Field(ge=0, le=120)
    email: str
    scores: List[float] = Field(default_factory=list)


async def demonstrate_validation() -> None:
    """Demonstrate validation functionality"""
    # Create validation pipeline
    pipeline = ValidationPipeline[Any, dict]()

    # Add validators
    pipeline.add_validator(SchemaValidator(UserData))
    pipeline.add_validator(TypeValidator(dict))
    pipeline.add_validator(LengthValidator(min_length=1, max_length=100))

    # Test data
    valid_data = {
        "username": "testuser",
        "age": 25,
        "email": "test@example.com",
        "scores": [85.5, 92.0, 78.5],
    }

    invalid_data = {
        "username": "t",  # Too short
        "age": 150,  # Too high
        "email": "invalid-email",
        "scores": "not-a-list",  # Wrong type
    }

    # Validate data
    print("Validating valid data...")
    results = await pipeline.validate(valid_data)
    for result in results:
        print(f"Valid: {result.valid}, Level: {result.level}, Message: {result.message}")

    print("\nValidating invalid data...")
    results = await pipeline.validate(invalid_data)
    for result in results:
        print(f"Valid: {result.valid}, Level: {result.level}, Message: {result.message}")


if __name__ == "__main__":
    asyncio.run(demonstrate_validation())
