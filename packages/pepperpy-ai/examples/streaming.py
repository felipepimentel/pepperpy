"""Example demonstrating AI streaming functionality"""

import asyncio

from pepperpy_ai import AIClient, AIConfig
from pepperpy_ai.types import AIResponse


async def demonstrate_streaming() -> None:
    """Demonstrate streaming functionality"""
    # Create AI configuration
    config = AIConfig.model_validate({})
    client = AIClient(config=config)

    try:
        # Initialize client
        await client.initialize()

        # Stream completion
        prompt = "Write a short story about a programmer who discovers AI"
        print("\nStreaming response:")
        print(f"Prompt: {prompt}\n")

        async for chunk in client.stream(prompt):
            if isinstance(chunk, AIResponse):
                print(chunk.content, end="", flush=True)
            else:
                print(chunk, end="", flush=True)
        print("\n")

        # Stream chat completion
        messages = [
            {"role": "system", "content": "You are a creative writer."},
            {"role": "user", "content": "Tell me a story about space exploration"},
        ]

        print("\nStreaming chat response:")
        async for chunk in client.stream(messages=messages):
            if isinstance(chunk, AIResponse):
                print(chunk.content, end="", flush=True)
            else:
                print(chunk, end="", flush=True)
        print("\n")

    finally:
        await client.cleanup()


if __name__ == "__main__":
    asyncio.run(demonstrate_streaming())
