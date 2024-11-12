"""Test logging functionality"""

import pytest

from pepperpy.core.logging import get_logger
from pepperpy.core.logging.config import LogConfig, LogLevel


@pytest.mark.asyncio
async def test_logger_config():
    """Test logger configuration"""
    config = LogConfig(
        name="test_logger",
        level=LogLevel.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        console_enabled=True,
        async_enabled=True,
    )

    # Get configured logger
    logger = get_logger(config.name, config)
    await logger.initialize()

    assert logger.metadata is not None
    assert logger.metadata.name == "logger"
    assert logger._name == "test_logger"

    # Test logging
    await logger.info("Test message")
    await logger.debug("Debug message")  # Shouldn't be logged

    # Get existing logger
    same_logger = get_logger("test_logger")
    assert same_logger == logger

    # Cleanup
    await logger.cleanup()


@pytest.mark.asyncio
async def test_logger_levels():
    """Test different logging levels"""
    config = LogConfig(
        name="test_levels",
        level=LogLevel.DEBUG,
        format="%(message)s",
        console_enabled=True,
        async_enabled=False,  # Synchronous for testing
    )

    logger = get_logger(config.name, config)
    await logger.initialize()

    # Test all log levels
    await logger.debug("Debug message")
    await logger.info("Info message")
    await logger.warning("Warning message")
    await logger.error("Error message")
    await logger.critical("Critical message")

    await logger.cleanup()
