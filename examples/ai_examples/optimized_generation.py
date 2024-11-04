from pepperpy.ai import AIModule
from pepperpy.ai.optimization.afn import AFNConfig, AFNOptimizer
from pepperpy.ai.optimization.attention import ContinuousBatcher
from pepperpy.ai.optimization.speculative import SpeculativeConfig, SpeculativeDecoder
from pepperpy.core import Application


async def main():
    # Configure AI module with all optimizations
    ai = (
        AIModule.create()
        .configure(
            model="mistralai/Mistral-7B-v0.1",
            optimizations={
                "afn": AFNConfig(hidden_size=768, chunk_size=128),
                "batch_size": 32,
                "speculative": SpeculativeConfig(
                    draft_model_name="mistralai/Mistral-7B-v0.1-int4"
                ),
            },
        )
        .build()
    )

    app = Application()
    app.add_module(ai)

    async with app.run():
        # Initialize optimized components
        model = await AFNOptimizer.convert_to_afn(
            ai.model, ai.config.optimizations["afn"]
        )
        model = await AFNOptimizer.optimize_memory_access(
            model, ai.config.optimizations["afn"]
        )

        # Setup continuous batching
        batcher = ContinuousBatcher(batch_size=ai.config.optimizations["batch_size"])

        # Setup speculative decoding
        decoder = SpeculativeDecoder(
            target_model=model,
            draft_model=ai.draft_model,
            config=ai.config.optimizations["speculative"],
        )

        # Generate optimized responses
        prompts = [
            "Explain quantum computing",
            "What is machine learning?",
            "How do neural networks work?",
        ]

        for prompt in prompts:
            # Add to batch
            inputs = ai.tokenizer(prompt, return_tensors="pt", padding=True)
            await batcher.add_request(inputs["input_ids"], inputs["attention_mask"])

        # Process all requests
        responses = await ai.generate_batch(prompts, decoder=decoder, batcher=batcher)

        for prompt, response in zip(prompts, responses):
            print(f"Q: {prompt}")
            print(f"A: {response.content}\n")


if __name__ == "__main__":
    import asyncio

    asyncio.run(main())
