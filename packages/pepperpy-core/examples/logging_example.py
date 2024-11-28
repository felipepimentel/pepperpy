"""Example demonstrating logging functionality"""

import asyncio

from pepperpy_core.logging import LogConfig, LogManager


async def demonstrate_logging() -> None:
    """Demonstrate logging functionality"""
    # Create log config
    config = LogConfig(level="DEBUG", handlers=["console"])

    # Create log manager
    log_manager = LogManager(config)

    try:
        # Initialize
        await log_manager.initialize()

        # Log messages with different levels
        log_manager.debug("This is a debug message", component="example")
        log_manager.info("This is an info message", user="test_user")
        log_manager.warning("This is a warning message", action="test_action")
        log_manager.error("This is an error message", error_code=500)

        # Log with structured data
        log_manager.info(
            "Processing request",
            request_id="123",
            user="test_user",
            action="login",
            metadata={"ip": "127.0.0.1", "browser": "Chrome"},
        )

        # Get logger for specific module
        module_logger = log_manager.get_logger("module.submodule")
        module_logger.info("Module specific log", component="submodule")

    finally:
        await log_manager.cleanup()


if __name__ == "__main__":
    asyncio.run(demonstrate_logging())
