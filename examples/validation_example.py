"""Validation example"""

import asyncio
from dataclasses import dataclass
from typing import Any

from pepperpy_core.module import BaseModule
from pepperpy_core.types import JsonDict
from pepperpy_core.validation import (
    RangeValidator,
    SchemaValidator,
    ValidationPipeline,
    ValidationResult,
)
from pydantic import BaseModel


class DataSchema(BaseModel):
    """Data validation schema"""

    id: str
    value: float
    metadata: dict[str, Any] = {}


@dataclass
class ValidatorConfig:
    """Validator configuration"""

    name: str
    settings: JsonDict = {}


class DataValidator(BaseModule[ValidatorConfig]):
    """Example data validator"""

    def __init__(self, config: ValidatorConfig) -> None:
        super().__init__(config)
        self._pipeline = ValidationPipeline[Any, dict[str, Any]]()

    async def _initialize(self) -> None:
        """Initialize validator"""
        print(f"Initializing validator {self.config.name}...")

        # Add validators to pipeline
        self._pipeline.add_validator(SchemaValidator(DataSchema))
        self._pipeline.add_validator(RangeValidator(min_value=0, max_value=100))

    async def _cleanup(self) -> None:
        """Cleanup validator"""
        print(f"Cleaning up validator {self.config.name}...")

    def _format_results(self, results: list[ValidationResult]) -> None:
        """Format and print validation results"""
        for result in results:
            status = "✓" if result.valid else "✗"
            print(f"{status} [{result.level}] {result.message}")
            if result.metadata:
                print(f"  Metadata: {result.metadata}")

    async def validate(self, data: dict[str, Any]) -> None:
        """Validate data"""
        self._ensure_initialized()

        print(f"\nValidating data: {data}")
        results = await self._pipeline.validate(data)
        self._format_results(results)


async def main() -> None:
    """Run example"""
    # Create validator
    config = ValidatorConfig(name="example")
    validator = DataValidator(config)

    try:
        # Initialize
        await validator.initialize()

        # Validate some data
        test_data = [
            {
                # Valid data
                "id": "test1",
                "value": 42.0,
                "metadata": {"source": "test"},
            },
            {
                # Invalid schema (missing value)
                "id": "test2",
                "metadata": {},
            },
            {
                # Invalid range
                "id": "test3",
                "value": 999.9,
                "metadata": {},
            },
            {
                # Invalid types
                "id": 123,
                "value": "not a number",
            },
        ]

        for data in test_data:
            await validator.validate(data)

    finally:
        # Cleanup
        await validator.cleanup()


if __name__ == "__main__":
    asyncio.run(main())
