"""Example of advanced integration features."""
from pepperpy.llm import get_llm
from pepperpy.data.embedding import TransformerEmbedding
from pepperpy.integrations.llm_data import RAGPipeline, RAGConfig
from pepperpy.data.types import Document, TextFormat
from pepperpy.telemetry import metrics
from pepperpy.streaming import StreamProcessor
import asyncio

async def demonstrate_integration():
    # Initialize components
    llm = get_llm("openrouter")
    embedding_model = TransformerEmbedding()
    
    # Configure RAG
    rag = RAGPipeline(
        llm,
        embedding_model,
        RAGConfig(
            chunk_size=500,
            chunk_overlap=50,
            similarity_threshold=0.7
        )
    )
    
    # Create sample documents
    documents = [
        Document(
            content="""
            Python is a high-level programming language known for its simplicity
            and readability. It supports multiple programming paradigms including
            procedural, object-oriented, and functional programming.
            """,
            format=TextFormat.PLAIN,
            metadata={"source": "python_docs", "section": "introduction"}
        ),
        Document(
            content="""
            Python's design philosophy emphasizes code readability with its notable
            use of significant whitespace. Its language constructs and object-oriented
            approach aim to help programmers write clear, logical code.
            """,
            format=TextFormat.PLAIN,
            metadata={"source": "python_docs", "section": "philosophy"}
        )
    ]
    
    # Process documents
    with metrics.timer("document_processing"):
        processed_docs = await rag.process_documents(documents)
    
    # Query using RAG
    query = "What are the main characteristics of Python?"
    
    with metrics.timer("rag_query"):
        response = await rag.query(query, processed_docs)
    
    print(f"Answer: {response['answer']}\n")
    print("Sources:")
    for source in response['sources']:
        print(f"- {source['content']}")
        print(f"  Similarity: {source['similarity']:.2f}")
        print(f"  Metadata: {source['metadata']}\n")
    
    # Print metrics
    print("\nMetrics:")
    for name, points in metrics.get_metrics().items():
        for point in points:
            print(f"{name}: {point['value']:.3f}s")

if __name__ == "__main__":
    asyncio.run(demonstrate_integration()) 