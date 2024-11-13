"""AI module examples demonstrating LLM integrations"""

import asyncio

from pepperpy.ai import AIClient, ask
from pepperpy.ai.chat import Conversation
from pepperpy.console import Console

console = Console()


async def simple_chat_example() -> None:
    """Simple chat completion example using environment configuration"""
    try:
        # Método 1: Usando a função de conveniência ask()
        response = await ask(
            "What are the key features that make Python popular for AI development?",
            system_prompt="You are a helpful AI assistant with expertise in Python programming.",
        )
        console.success(title="Quick Ask Response", content=response)

        # Método 2: Usando o cliente completo para mais controle
        async with AIClient.create() as client:
            # Criar uma conversa de forma fluente e legível
            response = await (
                Conversation()
                .system("You are a helpful AI assistant with expertise in Python programming.")
                .user("What are the key features that make Python popular for AI development?")
                .complete(client)
            )

            console.success(
                title=f"AI Response using {response.model}",
                subtitle=f"Usage: {response.usage}",
                content=response.content,
            )

            # Exemplo de conversa mais complexa
            response = await (
                Conversation()
                .system("You are a Python expert and mentor.")
                .user("I want to learn Python for AI development.")
                .assistant("That's a great choice! What's your current programming experience?")
                .user("I have some experience with JavaScript.")
                .complete(client)
            )

            console.success(
                title="Extended Conversation",
                subtitle=f"Model: {response.model} | Tokens: {response.usage.get('total_tokens', 0)}",
                content=response.content,
            )

    except Exception as e:
        console.error("Error occurred:", e)


if __name__ == "__main__":
    try:
        asyncio.run(simple_chat_example())
    except KeyboardInterrupt:
        console.info("Example finished! 👋")
