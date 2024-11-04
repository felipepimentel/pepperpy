from pepperpy.ai import AIModule
from pepperpy.ai.text.chunking import MarkdownChunker
from pepperpy.core import Application


async def main():
    # Configure AI module with optimizations
    ai = (
        AIModule.create()
        .configure(
            openrouter={
                "api_key": "your-key",
                "default_model": "anthropic/claude-3-opus",
            },
            embeddings={
                "local": True,
                "model": "all-MiniLM-L6-v2",  # Small, efficient model
            },
            cache={
                "backend": "file",  # Persistent cache
                "ttl": 3600 * 24,  # 24 hour cache
            },
        )
        .build()
    )

    app = Application()
    app.add_module(ai)

    async with app.run():
        ai_module = app.get_module("ai", AIModule)

        # Process large document efficiently
        with open("large_document.md", "r") as f:
            document = f.read()

        # Split into optimal chunks
        chunker = MarkdownChunker()
        chunks = chunker.split(document, max_chunk_size=1000)

        # Generate embeddings in batches
        embeddings = await ai_module.embed_batch(
            [chunk.content for chunk in chunks],
            batch_size=20,  # Adjust based on memory
        )

        # Process multiple queries efficiently
        questions = [
            "What are the main topics?",
            "Summarize the key points",
            "What are the conclusions?",
        ]

        responses = await ai_module.generate_batch(
            questions, batch_size=3, context=document
        )

        for question, response in zip(questions, responses):
            print(f"Q: {question}")
            print(f"A: {response.content}\n")


if __name__ == "__main__":
    import asyncio

    asyncio.run(main())
