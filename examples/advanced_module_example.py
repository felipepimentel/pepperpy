"""Advanced module example demonstrating error handling and events"""

import asyncio
from dataclasses import dataclass
from typing import Any, Callable

from pepperpy_core.exceptions import ModuleError
from pepperpy_core.module import BaseModule
from pepperpy_core.types import JsonDict


@dataclass
class AdvancedConfig:
    """Advanced module configuration"""

    name: str
    settings: JsonDict
    max_retries: int = 3
    retry_delay: float = 1.0


class AdvancedModule(BaseModule[AdvancedConfig]):
    """Advanced module implementation with error handling and events"""

    def __init__(self, config: AdvancedConfig) -> None:
        super().__init__(config)
        self._handlers: dict[str, list[Callable[..., Any]]] = {
            "initialized": [],
            "cleanup": [],
            "error": [],
        }

    def on(self, event: str, handler: Callable[..., Any]) -> None:
        """Register event handler"""
        if event not in self._handlers:
            raise ValueError(f"Unknown event: {event}")
        self._handlers[event].append(handler)

    def _emit(self, event: str, *args: Any, **kwargs: Any) -> None:
        """Emit event to handlers"""
        for handler in self._handlers[event]:
            try:
                handler(*args, **kwargs)
            except Exception as e:
                print(f"Error in event handler: {e}")

    async def _initialize(self) -> None:
        """Initialize module with retry logic"""
        retries = 0
        while True:
            try:
                print(f"Initializing {self.config.name}...")
                # Simulate initialization
                await asyncio.sleep(0.1)
                self._metadata["start_time"] = asyncio.get_event_loop().time()
                self._emit("initialized", self)
                break
            except Exception as e:
                retries += 1
                if retries >= self.config.max_retries:
                    self._emit("error", e)
                    raise ModuleError("Failed to initialize after retries", cause=e)
                print(f"Retry {retries} after error: {e}")
                await asyncio.sleep(self.config.retry_delay)

    async def _cleanup(self) -> None:
        """Cleanup module"""
        print(f"Cleaning up {self.config.name}...")
        end_time = asyncio.get_event_loop().time()
        start_time = self._metadata.get("start_time", 0)
        duration = end_time - start_time
        self._metadata["duration"] = duration
        self._emit("cleanup", self)

    async def process(self, data: Any) -> Any:
        """Process data with error handling"""
        self._ensure_initialized()
        try:
            print(f"Processing data with {self.config.name}...")
            # Simulate processing
            await asyncio.sleep(0.1)
            return data
        except Exception as e:
            self._emit("error", e)
            raise ModuleError("Failed to process data", cause=e)


async def main() -> None:
    """Run advanced example"""
    # Create module
    config = AdvancedConfig(
        name="advanced", settings={"debug": True}, max_retries=3, retry_delay=0.5
    )
    module = AdvancedModule(config)

    # Register event handlers
    module.on("initialized", lambda m: print(f"Module {m.config.name} initialized"))
    module.on(
        "cleanup",
        lambda m: print(f"Module {m.config.name} ran for {m.metadata['duration']:.2f} seconds"),
    )
    module.on("error", lambda e: print(f"Error occurred: {e}"))

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
