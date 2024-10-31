"""Example of workflow and pipeline usage."""
import asyncio
from pepperpy.workflow.engine import Workflow
from pepperpy.pipeline.processor import create_pipeline
from pepperpy.logging import get_logger

logger = get_logger()

async def demonstrate_workflow_pipeline():
    # Workflow example
    workflow = Workflow("data_processing")
    
    # Define workflow tasks
    async def fetch_data(context):
        return {"users": [{"id": 1, "name": "John"}, {"id": 2, "name": "Jane"}]}
    
    async def process_data(context):
        users = context["fetch_data"]["users"]
        return [user["name"].upper() for user in users]
    
    async def save_results(context):
        processed = context["process_data"]
        return {"saved": True, "count": len(processed)}
    
    # Configure workflow
    workflow.add_task("fetch_data", fetch_data)
    workflow.add_task("process_data", process_data, depends_on=["fetch_data"])
    workflow.add_task("save_results", save_results, depends_on=["process_data"])
    
    # Execute workflow
    results = await workflow.execute()
    logger.info(f"Workflow results: {results}")
    
    # Pipeline example
    pipeline = create_pipeline("text_processing")
    
    # Define pipeline stages
    def normalize_text(text: str) -> str:
        return text.lower().strip()
    
    def tokenize(text: str) -> list:
        return text.split()
    
    def count_words(tokens: list) -> dict:
        return {"word_count": len(tokens)}
    
    # Configure pipeline
    pipeline.add_stage("normalize", normalize_text)
    pipeline.add_stage("tokenize", tokenize)
    pipeline.add_stage("count", count_words)
    
    # Process data
    text = "  Hello World from Pepperpy!  "
    result = await pipeline.process(text)
    logger.info(f"Pipeline result: {result}")

if __name__ == "__main__":
    asyncio.run(demonstrate_workflow_pipeline()) 