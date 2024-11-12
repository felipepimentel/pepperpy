"""Example using PepperPy AI module"""

import asyncio

from pepperpy.ai.module import AIModule
from pepperpy.ai.types import Message
from pepperpy.core.logging import LogConfig, LogLevel, get_logger
from pepperpy.core.resources import pepperpy_session

# Configure logger
log_config = LogConfig(
    level=LogLevel.DEBUG,
    console_enabled=True,
    colors_enabled=True,
    format="[{timestamp}] {level:<8} {module}: {message}",
)
logger = get_logger("ai_example", log_config)


async def example_with_context() -> None:
    """Example using context manager"""
    try:
        async with AIModule.session() as ai:
            await logger.info("Sending query to AI...")
            response = await ai.ask("What is the capital of France?")
            await logger.info(f"Response received: {response}")
    except Exception as e:
        await logger.error(f"Error in AI context: {str(e)}")


async def example_with_resource_manager() -> None:
    """Example using resource manager"""
    try:
        async with pepperpy_session() as pepper:
            await logger.info("Initializing AI module...")
            ai = await AIModule.create()
            await pepper.add("ai", ai)

            await logger.info("Sending haiku request...")
            response = await ai.ask("Write a haiku about programming")
            await logger.info(f"Haiku received: {response}")
    except Exception as e:
        await logger.error(f"Error in resource manager: {str(e)}")


async def main() -> None:
    """Main example function"""
    await logger.info("Starting PepperPy AI Example")

    await logger.info("Running context manager example...")
    await example_with_context()

    await logger.info("Running resource manager example...")
    await example_with_resource_manager()

    await logger.info("Running quick usage example...")
    try:
        async with pepperpy_session() as pepper:
            ai = await AIModule.create()
            await pepper.add("ai", ai)

            messages = [
                Message(role="system", content="You are a quantum physics expert"),
                Message(role="user", content="Explain quantum entanglement simply"),
            ]
            await logger.debug("Sending expert query...", messages=len(messages))
            response = await ai.generate(messages)
            await logger.info(f"Expert response: {response.content}")
    except Exception as e:
        await logger.error(f"Error in quick usage: {str(e)}")


if __name__ == "__main__":
    asyncio.run(main())
