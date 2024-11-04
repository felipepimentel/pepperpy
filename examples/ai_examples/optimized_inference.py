from pepperpy.ai import AIModule
from pepperpy.ai.core.ggml import GGMLConfig
from pepperpy.ai.optimization.compression import ModelCompressor
from pepperpy.core import Application


async def main():
    # Configure AI module with optimizations
    ai = (
        AIModule.create()
        .configure(
            ggml=GGMLConfig(
                model_path="models/llama-7b.gguf",
                n_threads=8,
                n_gpu_layers=0,  # CPU only
            ),
            compression={"pruning_amount": 0.3, "quantization": "int8"},
        )
        .build()
    )

    app = Application()
    app.add_module(ai)

    async with app.run():
        # Load and optimize model
        model = await ModelCompressor.prune_model(ai.model, amount=0.3)
        model = await ModelCompressor.quantize_dynamic(model, dtype="int8")

        # Export optimized model
        await ModelCompressor.export_onnx(
            model, "optimized_model.onnx", {"input_ids": [1, 128]}
        )

        # Run efficient inference
        response = await ai.generate(
            "Explain quantum computing", max_length=1000, temperature=0.7
        )
        print(f"Response: {response}")


if __name__ == "__main__":
    import asyncio

    asyncio.run(main())
