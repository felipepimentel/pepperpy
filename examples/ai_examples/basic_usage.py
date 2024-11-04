from pepperpy.ai import AIModule
from pepperpy.core import Application


async def main():
    # Create application
    app = Application()

    # Configure AI module
    ai = (
        AIModule.create()
        .configure(
            openrouter={
                "api_key": "your-openrouter-key",
                "default_model": "anthropic/claude-3-opus",
            },
            stackspot={
                "api_key": "your-stackspot-key",
                "workspace_id": "your-workspace",
            },
            default_provider="openrouter",
        )
        .build()
    )

    # Add module to application
    app.add_module(ai)

    # Use the module
    async with app.run():
        # Get AI module
        ai_module = app.get_module("ai", AIModule)

        # Generate with default provider (OpenRouter)
        response = await ai_module.generate("Explain quantum computing in simple terms")
        print(f"Response from {response.model}: {response.content}")

        # Generate with specific provider and model
        response = await ai_module.generate(
            "What are the best practices for Python development?", provider="stackspot"
        )
        print(f"Response from StackSpot: {response.content}")

        # List available models
        models = await ai_module.list_models()
        print("Available models:", models)


if __name__ == "__main__":
    import asyncio

    asyncio.run(main())
