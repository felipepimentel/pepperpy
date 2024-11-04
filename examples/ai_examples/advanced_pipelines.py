import asyncio

from pepperpy.ai import AIModule
from pepperpy.ai.pipeline.advanced import AdvancedPipelines
from pepperpy.ai.visualization.advanced import AdvancedVisualizer
from pepperpy.core import Application


async def main():
    # Configure AI module
    ai = (
        AIModule.create()
        .configure(
            openrouter={
                "api_key": "your-key",
                "default_model": "anthropic/claude-3-opus",
            },
            embeddings={"local": True, "model": "all-MiniLM-L6-v2"},
        )
        .build()
    )

    app = Application()
    app.add_module(ai)

    async with app.run():
        # Create visualizer
        visualizer = AdvancedVisualizer()

        # Create and use fine-tuning pipeline
        fine_tuning_pipeline = AdvancedPipelines.create_fine_tuning_pipeline(ai)

        training_data = {
            "texts": ["text 1", "text 2", ...],
            "labels": ["label 1", "label 2", ...],
        }

        async for result in fine_tuning_pipeline.execute(training_data):
            print(f"Fine-tuning step result: {result}")

        # Create and use data augmentation pipeline
        augmentation_pipeline = AdvancedPipelines.create_data_augmentation_pipeline(
            ai, num_variations=3
        )

        texts = ["original text 1", "original text 2"]

        async for result in augmentation_pipeline.execute(texts):
            print(f"Augmentation step result: {result}")

        # Visualize pipeline flow
        pipeline_viz = visualizer.plot_pipeline_flow(
            fine_tuning_pipeline.steps, ai.get_metrics()
        )
        pipeline_viz.show("pipeline_flow.html")

        # Visualize embeddings
        embeddings = await ai.embed_batch(texts)
        cluster_fig = visualizer.plot_embedding_clusters(
            embeddings, labels=texts, n_components=3
        )
        cluster_fig.show()


if __name__ == "__main__":
    asyncio.run(main())
