"""Example demonstrating core module functionality"""

import asyncio

from pepperpy_core.base.module import BaseModule
from pepperpy_core.base.types import JsonDict
from pydantic import BaseModel, ConfigDict, Field


class ExampleConfig(BaseModel):
    """Example configuration"""

    name: str = "example"
    enabled: bool = True
    metadata: JsonDict = Field(default_factory=dict)
    model_config = ConfigDict(frozen=True)


class ExampleModule(BaseModule[ExampleConfig]):
    """Example module implementation"""

    async def _initialize(self) -> None:
        """Initialize module"""
        print(f"Initializing {self.config.name}...")
        self._metadata["initialized_at"] = "now"

    async def _cleanup(self) -> None:
        """Cleanup module"""
        print(f"Cleaning up {self.config.name}...")
        self._metadata["cleaned_at"] = "now"

    async def process(self, data: str) -> str:
        """Process data"""
        self._ensure_initialized()
        return f"Processed: {data}"


async def main() -> None:
    """Run example"""
    # Create module
    config = ExampleConfig(name="test_module")
    module = ExampleModule(config)

    try:
        # Initialize
        await module.initialize()
        assert module.is_initialized
        assert "initialized_at" in module.metadata

        # Process data
        result = await module.process("test data")
        print(f"Result: {result}")

    finally:
        # Cleanup
        await module.cleanup()
        assert not module.is_initialized
        assert "cleaned_at" in module.metadata


if __name__ == "__main__":
    asyncio.run(main())
