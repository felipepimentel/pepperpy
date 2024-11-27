"""Metrics example"""

import asyncio
import random
from dataclasses import dataclass

from pepperpy_core.metrics import MetricsCollector, MetricsConfig, timing
from pepperpy_core.module import BaseModule
from pepperpy_core.types import JsonDict


@dataclass
class WorkerConfig:
    """Worker configuration"""

    name: str
    settings: JsonDict = {}


class Worker(BaseModule[WorkerConfig]):
    """Example worker with metrics"""

    def __init__(self, config: WorkerConfig) -> None:
        super().__init__(config)
        self.metrics = MetricsCollector(
            MetricsConfig(prefix=f"{config.name}_", default_labels={"worker": config.name})
        )
        self._processed = 0
        self._errors = 0

    async def _initialize(self) -> None:
        """Initialize worker"""
        print(f"Initializing worker {self.config.name}...")
        self.metrics.counter("initialized")

    async def _cleanup(self) -> None:
        """Cleanup worker"""
        print(f"Cleaning up worker {self.config.name}...")
        self.metrics.counter("cleaned_up")

    @timing("process")
    async def process_item(self, item: str) -> None:
        """Process item with metrics"""
        self._ensure_initialized()

        try:
            # Record start
            self.metrics.counter("items_processed_total", labels={"type": "start"})

            # Simulate processing
            await asyncio.sleep(random.uniform(0.1, 0.3))

            # Simulate random errors
            if random.random() < 0.3:
                raise ValueError("Random error")

            # Record success
            self._processed += 1
            self.metrics.counter("items_processed_total", labels={"type": "success"})
            self.metrics.gauge("items_processed", self._processed)

        except Exception:
            # Record error
            self._errors += 1
            self.metrics.counter("items_processed_total", labels={"type": "error"})
            self.metrics.gauge("errors_total", self._errors)
            raise


async def main() -> None:
    """Run example"""
    # Create worker
    config = WorkerConfig(name="example")
    worker = Worker(config)

    try:
        # Initialize
        await worker.initialize()

        # Process items
        items = [f"item_{i}" for i in range(10)]
        for item in items:
            try:
                await worker.process_item(item)
                print(f"Processed {item}")
            except Exception as e:
                print(f"Error processing {item}: {e}")

        # Print metrics
        print("\nMetrics:")
        for metric in worker.metrics.collect():
            print(f"{metric.name} " f"({metric.type}): " f"{metric.value} " f"{metric.labels}")

    finally:
        # Cleanup
        await worker.cleanup()


if __name__ == "__main__":
    asyncio.run(main())
