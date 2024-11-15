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
        )
        console.success(title="Quick Ask Response", content=response.content)

        # Método 2: Usando o cliente completo para mais controle
        client = await AIClient.create()
        async with client:
            conversation = Conversation(client)
            conversation.add_message(
                "system", "You are a helpful AI assistant with expertise in Python programming.",
            )

            response = await conversation.send_message(
                "What are the key features that make Python popular for AI development?",
            )

            console.success(
                title=f"AI Response using {response.model}",
                subtitle=f"Usage: {response.usage}",
                content=response.content,
            )

            # Exemplo de conversa mais complexa
            conversation.clear_history()
            conversation.add_message("system", "You are a Python expert and mentor.")

            response = await conversation.send_message("I want to learn Python for AI development.")
            console.print("Assistant:", response.content)

            response = await conversation.send_message("I have some experience with JavaScript.")
            console.success(
                title="Extended Conversation",
                subtitle=f"Model: {response.model} | Usage: {response.usage}",
                content=response.content,
            )

    except Exception as e:
        console.error("❌ Error during chat:", str(e))


if __name__ == "__main__":
    try:
        asyncio.run(simple_chat_example())
    except KeyboardInterrupt:
        console.info("\n👋 Chat finished!")
