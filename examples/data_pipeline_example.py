from pepperpy.data.types import Document, TextFormat, ChunkingStrategy
from pepperpy.data.pipeline import Pipeline, PipelineConfig
from pepperpy.data.embedding import TransformerEmbedding

def demonstrate_pipeline():
    # Configure the pipeline
    config = PipelineConfig(
        chunking_strategy=ChunkingStrategy.SENTENCE,
        chunking_params={"max_sentences": 3},
        embedding_enabled=True,
        chunk_embeddings=True
    )
    
    # Create embedding model
    embedding_model = TransformerEmbedding()
    
    # Create pipeline
    pipeline = Pipeline(config, embedding_model)
    
    # Create a document
    document = Document(
        content="""
        This is a sample document. It contains multiple sentences.
        We will process it through our pipeline. The pipeline will
        chunk the text, preprocess it, and generate embeddings.
        This demonstrates the power of our data processing capabilities.
        """,
        format=TextFormat.PLAIN,
        metadata={"source": "example"}
    )
    
    # Process document
    processed_doc = pipeline.process(document)
    
    # Print results
    print(f"Number of chunks: {len(processed_doc.chunks)}")
    for i, chunk in enumerate(processed_doc.chunks):
        print(f"\nChunk {i+1}:")
        print(f"Content: {chunk.content}")
        print(f"Embedding shape: {chunk.embedding.shape}")
        print(f"Start index: {chunk.start_index}")
        print(f"End index: {chunk.end_index}")

if __name__ == "__main__":
    demonstrate_pipeline() 