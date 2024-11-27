"""Logging example"""

import asyncio
from dataclasses import dataclass
from typing import Optional

from pepperpy_core.logging import LogConfig, get_logger
from pepperpy_core.module import BaseModule
from pepperpy_core.types import JsonDict


@dataclass
class ServiceConfig:
    """Service configuration"""

    name: str
    log_level: str = "INFO"
    metadata: JsonDict = {}


class Service(BaseModule[ServiceConfig]):
    """Example service with logging"""

    def __init__(self, config: ServiceConfig) -> None:
        super().__init__(config)
        self.logger = get_logger(
            f"service.{config.name}", LogConfig(level=config.log_level, metadata=config.metadata)
        )

    async def _initialize(self) -> None:
        """Initialize service"""
        self.logger.info("Initializing service", service=self.config.name)
        self._metadata["start_time"] = "now"

    async def _cleanup(self) -> None:
        """Cleanup service"""
        self.logger.info("Cleaning up service", service=self.config.name)

    async def process(self, data: str, request_id: Optional[str] = None) -> None:
        """Process data"""
        self._ensure_initialized()

        try:
            self.logger.info(
                "Processing data",
                service=self.config.name,
                request_id=request_id,
                data_length=len(data),
            )

            # Simulate processing
            await asyncio.sleep(0.1)

            if "error" in data.lower():
                raise ValueError("Error in data")

            self.logger.info(
                "Data processed successfully", service=self.config.name, request_id=request_id
            )

        except Exception as e:
            self.logger.error(
                "Failed to process data",
                service=self.config.name,
                request_id=request_id,
                error=str(e),
            )
            raise


async def main() -> None:
    """Run example"""
    # Create service
    config = ServiceConfig(
        name="example",
        log_level="DEBUG",
        metadata={"environment": "development", "version": "1.0.0"},
    )
    service = Service(config)

    try:
        # Initialize
        await service.initialize()

        # Process some data
        await service.process("test data", request_id="req-123")

        try:
            await service.process("error data", request_id="req-456")
        except Exception:
            pass  # Ignore error for example

    finally:
        # Cleanup
        await service.cleanup()


if __name__ == "__main__":
    asyncio.run(main())
