import asyncio

from pepperpy.ai import AIModule
from pepperpy.ai.processing import Priority
from pepperpy.core import Application


async def process_with_streaming():
    # Configure AI module
    ai = (
        AIModule.create()
        .configure(
            openrouter={
                "api_key": "your-key",
                "default_model": "anthropic/claude-3-opus",
            },
            embeddings={"local": True, "model": "all-MiniLM-L6-v2"},
            max_concurrent=3,
            batch_size=20,
        )
        .build()
    )

    app = Application()
    app.add_module(ai)

    async with app.run():
        ai_module = app.get_module("ai", AIModule)

        # Process high-priority queries first
        high_priority_queries = [
            "What are the critical security issues?",
            "Are there any immediate risks?",
        ]

        normal_priority_queries = [
            "Summarize the improvements",
            "List potential optimizations",
        ]

        # Process queries with different priorities
        async def process_queries():
            results = await asyncio.gather(
                ai_module.process_document(
                    "document content...", high_priority_queries, priority=Priority.HIGH
                ),
                ai_module.process_document(
                    "document content...",
                    normal_priority_queries,
                    priority=Priority.NORMAL,
                ),
            )
            return results

        # Start processing
        processing_task = asyncio.create_task(process_queries())

        # While processing, stream another response
        print("\nStreaming response:")
        async for token in ai_module.generate_stream(
            "Analyze the overall impact",
            buffer_size=10,  # Larger buffer for faster processing
        ):
            print(token.content, end="", flush=True)
            print(f"\nToken stats: {token.metadata}")  # Show token metadata

        # Get and display processing results
        results = await processing_task
        print("\nProcessing results:", results)

        # Show processor stats
        print("\nProcessor stats:", ai_module._batch_processor.stats)


if __name__ == "__main__":
    asyncio.run(process_with_streaming())
