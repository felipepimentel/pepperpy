import asyncio

from pepperpy.ai import AIModule
from pepperpy.ai.pipeline.templates import AIPipelines
from pepperpy.ai.visualization import AIVisualizer
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
        visualizer = AIVisualizer()

        # Create and use RAG pipeline
        rag_pipeline = AIPipelines.create_rag_pipeline(ai)

        document = """
        Long document with multiple paragraphs...
        """

        query = "What are the main points?"

        async for result in rag_pipeline.execute(
            {"document": document, "query": query}
        ):
            print(f"Pipeline step result: {result}")

        # Get metrics and create visualizations
        metrics = ai.get_metrics()

        # Plot performance metrics
        performance_fig = visualizer.plot_performance_metrics(metrics)
        performance_fig.show()

        # Plot token distribution
        responses = [...]  # List of responses
        token_fig = visualizer.plot_token_distribution(responses)
        token_fig.show()

        # Plot similarity matrix
        texts = [...]  # List of texts
        similarity_matrix = await ai.analyze_similarities(texts)
        similarity_fig = visualizer.plot_similarity_matrix(
            similarity_matrix, labels=[f"Text {i}" for i in range(len(texts))]
        )
        similarity_fig.show()


if __name__ == "__main__":
    asyncio.run(main())
