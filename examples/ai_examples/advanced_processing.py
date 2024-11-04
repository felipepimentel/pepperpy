import asyncio

from pepperpy.ai import AIModule
from pepperpy.core import Application


async def process_large_document():
    # Configure AI module
    ai = (
        AIModule.create()
        .configure(
            openrouter={
                "api_key": "your-key",
                "default_model": "anthropic/claude-3-opus",
            },
            embeddings={"local": True, "model": "all-MiniLM-L6-v2"},
            max_concurrent=3,  # Limit concurrent operations
            batch_size=20,  # Optimize batch size
        )
        .build()
    )

    app = Application()
    app.add_module(ai)

    async with app.run():
        ai_module = app.get_module("ai", AIModule)

        # Process document with multiple queries
        document = """
        [Large document content...]
        """

        queries = [
            "Summarize the main points",
            "What are the key findings?",
            "List the recommendations",
            "Identify potential issues",
        ]

        # Process all queries efficiently
        results = await ai_module.process_document(document, queries, temperature=0.7)

        for query, response in results.items():
            print(f"\nQuery: {query}")
            print(f"Response: {response.content}")

        # Demonstrate streaming
        print("\nStreaming response:")
        async for token in ai_module.generate_stream(
            "Explain the document's significance"
        ):
            print(token.content, end="", flush=True)

        # Analyze text similarities
        texts = [
            "First important point",
            "Second related concept",
            "Third different topic",
            # ... more texts
        ]

        similarity_matrix = await ai_module.analyze_similarities(texts)
        print("\n\nSimilarity Matrix:")
        print(similarity_matrix)


if __name__ == "__main__":
    asyncio.run(process_large_document())
