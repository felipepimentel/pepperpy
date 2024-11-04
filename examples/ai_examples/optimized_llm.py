import asyncio

import torch

from pepperpy.ai import AIModule
from pepperpy.ai.cache.vector import VectorCacheConfig
from pepperpy.ai.core.llm import LLMConfig
from pepperpy.core import Application


async def main():
    # Configure AI module with optimizations
    ai = (
        AIModule.create()
        .configure(
            llm=LLMConfig(
                model_id="mistralai/Mistral-7B-v0.1",
                device_map="auto",
                torch_dtype=torch.float16,
                load_in_8bit=True,
                use_better_transformer=True,
                max_memory={0: "24GB"},
            ),
            cache=VectorCacheConfig(engine="faiss", dimension=768),
        )
        .build()
    )

    app = Application()
    app.add_module(ai)

    async with app.run():
        # Generate text with optimized model
        response = await ai.generate(
            "Explain quantum computing", max_length=1000, temperature=0.7
        )
        print(f"Response: {response}")

        # Generate and cache embeddings
        embeddings = await ai.embed_batch(
            ["First text to embed", "Second text to embed", "Third text to embed"]
        )

        # Search similar texts
        results = await ai.search_similar("Query text", k=2)
        print(f"Similar texts: {results}")


if __name__ == "__main__":
    asyncio.run(main())
