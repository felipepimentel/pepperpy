"""AI module examples demonstrating LLM integrations"""

import asyncio
from typing import Dict, Optional

from pepperpy.ai import AIClient, AIConfig
from pepperpy.console import Console
from pepperpy.core.config import load_config

console = Console()


def get_ai_config() -> Optional[Dict[str, str]]:
    """Get AI configuration from environment"""
    config = load_config(
        {
            "OPENROUTER_API_KEY": {
                "required": True,
                "validator": lambda x: x.startswith("sk-"),
                "error": "API key must start with 'sk-'",
            },
            "OPENROUTER_MODEL": {"default": "openai/gpt-4o-mini", "description": "AI model to use"},
            "SITE_URL": {"default": "https://github.com/felipepimentel/pepperpy"},
            "SITE_NAME": {"default": "PepperPy Demo"},
        }
    )

    if not config.is_valid():
        console.error("Configuration Error:", config.get_errors())
        return None

    return config.as_dict()


async def simple_chat_example() -> None:
    """Simple chat completion example using OpenRouter"""
    config = get_ai_config()
    if not config:
        return

    async with AIClient.from_config(AIConfig(**config)) as client:
        try:
            response = await client.complete(
                [
                    {
                        "role": "system",
                        "content": "You are a helpful AI assistant with expertise in Python programming.",
                    },
                    {
                        "role": "user",
                        "content": "What are the key features that make Python popular for AI development?",
                    },
                ]
            )

            console.success(
                title=f"AI Response using {response.model}",
                subtitle=f"Usage: {response.usage}",
                content=response.content,
            )

        except Exception as e:
            console.error("Error occurred:", e)


if __name__ == "__main__":
    try:
        asyncio.run(simple_chat_example())
    except KeyboardInterrupt:
        console.info("Example finished! 👋")
