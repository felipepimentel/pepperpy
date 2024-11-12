"""Example usage of logging functionality"""

import asyncio

from pepperpy.core.logging import get_logger
from pepperpy.core.logging.config import LogConfig, LogLevel


async def basic_logging_example() -> None:
    """Basic logging example"""
    config = LogConfig(
        name="basic_example",
        level=LogLevel.DEBUG,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        console_enabled=True,
        async_enabled=True,
    )

    logger = get_logger(config.name, config)
    await logger.initialize()

    await logger.debug("Debug message")
    await logger.info("Info message")
    await logger.warning("Warning message")
    await logger.error("Error message")
    await logger.critical("Critical message")

    await logger.cleanup()


async def file_logging_example() -> None:
    """File logging example"""
    config = LogConfig(
        name="file_example",
        level=LogLevel.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        console_enabled=True,
        file_enabled=True,
        file_path="example.log",
        async_enabled=True,
    )

    logger = get_logger(config.name, config)
    await logger.initialize()

    await logger.info("This message goes to both console and file")
    await logger.error("Error messages are also logged")

    await logger.cleanup()


async def main() -> None:
    """Run logging examples"""
    await basic_logging_example()
    await file_logging_example()


if __name__ == "__main__":
    asyncio.run(main())
