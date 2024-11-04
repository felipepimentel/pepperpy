from pepperpy.ai import AIModule
from pepperpy.core import Application


async def main():
    # Create application
    app = Application()

    # Configure AI module with advanced features
    ai = (
        AIModule.create()
        .configure(
            openrouter={
                "api_key": "your-key",
                "default_model": "anthropic/claude-3-opus",
            },
            embeddings={"local": True, "model": "all-MiniLM-L6-v2"},
            cache={"ttl": 3600},
        )
        .build()
    )

    # Add module to application
    app.add_module(ai)

    async with app.run():
        ai_module = app.get_module("ai", AIModule)

        # Generate with context
        context = """
        Python is a high-level programming language known for its simplicity.
        It emphasizes code readability with its notable use of significant whitespace.
        Python features a dynamic type system and automatic memory management.
        """

        response = await ai_module.generate_with_context(
            "What are Python's main features?", context=context
        )
        print(f"Response: {response.content}")

        # Calculate text similarity
        text1 = "Python is great for data science"
        text2 = "Python is excellent for scientific computing"
        similarity = await ai_module.calculate_similarity(text1, text2)
        print(f"Similarity: {similarity}")


if __name__ == "__main__":
    import asyncio

    asyncio.run(main())
