"""Example demonstrating basic AI chat functionality"""

import asyncio

from pepperpy_ai import AIClient, AIConfig


async def demonstrate_chat() -> None:
    """Demonstrate basic chat functionality"""
    # Create AI configuration
    config = AIConfig.model_validate({})
    client = AIClient(config=config)

    try:
        # Initialize client
        await client.initialize()

        # Simple completion
        response = await client.complete("Explain what is dependency injection in Python")
        print("\nBasic completion:")
        print(response.content)

        # Chat with context
        messages = [
            {"role": "system", "content": "You are a Python expert."},
            {"role": "user", "content": "What are Python decorators?"},
            {"role": "assistant", "content": "Decorators are a way to modify functions."},
            {"role": "user", "content": "Can you show an example?"},
        ]

        response = await client.complete(messages=messages)
        print("\nChat completion:")
        print(response.content)

    finally:
        await client.cleanup()


if __name__ == "__main__":
    asyncio.run(demonstrate_chat())
