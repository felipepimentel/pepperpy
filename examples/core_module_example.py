"""Core module example"""

import asyncio
from dataclasses import dataclass
from typing import Any

from pepperpy_core.module import BaseModule
from pepperpy_core.types import JsonDict


@dataclass
class ExampleConfig:
    """Example configuration"""

    name: str
    settings: JsonDict


class ExampleModule(BaseModule[ExampleConfig]):
    """Example module implementation"""

    async def _initialize(self) -> None:
        """Initialize module"""
        print(f"Initializing {self.config.name}...")
        self._metadata["start_time"] = asyncio.get_event_loop().time()

    async def _cleanup(self) -> None:
        """Cleanup module"""
        print(f"Cleaning up {self.config.name}...")
        end_time = asyncio.get_event_loop().time()
        start_time = self._metadata.get("start_time", 0)
        print(f"Module ran for {end_time - start_time:.2f} seconds")

    async def process(self, data: Any) -> Any:
        """Process data"""
        self._ensure_initialized()
        print(f"Processing data with {self.config.name}...")
        return data


async def main() -> None:
    """Run example"""
    # Create module
    config = ExampleConfig(name="example", settings={"debug": True})
    module = ExampleModule(config)

    try:
        # Initialize
        await module.initialize()

        # Process data
        result = await module.process("test data")
        print(f"Result: {result}")

    finally:
        # Cleanup
        await module.cleanup()


if __name__ == "__main__":
    asyncio.run(main())
