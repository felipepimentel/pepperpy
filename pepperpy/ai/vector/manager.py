"""Vector operations manager"""

from typing import Any, Sequence, TypeVar, cast

from pepperpy.core.module import BaseModule
from pepperpy.db.engines import BaseEngine, get_engine

from ..client import AIClient
from .config import VectorConfig
from .exceptions import VectorError
from .types import VectorResult

# Type variable for row dictionary keys
K = TypeVar('K', bound=str)

class VectorManager(BaseModule):
    """Manages vector operations and storage"""

    def __init__(self, config: VectorConfig, ai_client: AIClient | None = None) -> None:
        self.config = config
        self.ai_client = ai_client
        self._engine: BaseEngine | None = None
        self._initialized = False

    async def initialize(self) -> None:
        """Initialize vector operations"""
        if self._initialized:
            return

        if self.config.backend == "pgvector":
            if not self.config.db_config:
                raise VectorError("Database configuration required")
            
            self._engine = get_engine(self.config.db_config.__dict__)
            await self._engine.initialize()
            
            # Enable pgvector extension
            if self._engine:
                await self._engine.execute("CREATE EXTENSION IF NOT EXISTS vector;")
                
                # Create vector table if not exists
                await self._create_vector_table()

        self._initialized = True

    async def _create_vector_table(self) -> None:
        """Create vector storage table"""
        if not self._engine:
            raise VectorError("Database engine not initialized")

        query = f"""
        CREATE TABLE IF NOT EXISTS ai_vectors (
            id SERIAL PRIMARY KEY,
            collection TEXT NOT NULL,
            vector vector({self.config.dimension}),
            metadata JSONB,
            created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
        );
        CREATE INDEX IF NOT EXISTS ai_vectors_collection_idx ON ai_vectors(collection);
        CREATE INDEX IF NOT EXISTS ai_vectors_vector_idx ON ai_vectors 
        USING ivfflat (vector vector_cosine_ops)
        WITH (lists = 100);
        """
        await self._engine.execute(query)

    async def store_vectors(
        self, 
        collection: str,
        vectors: Sequence[list[float]], 
        metadata: list[dict[str, Any]] | None = None
    ) -> list[int]:
        """Store vectors in database"""
        if not self._initialized:
            await self.initialize()

        if not self._engine:
            raise VectorError("Database engine not initialized")

        try:
            query = """
            INSERT INTO ai_vectors (collection, vector, metadata)
            VALUES ($1, $2, $3)
            RETURNING id;
            """
            
            results = []
            for i, vector in enumerate(vectors):
                meta = metadata[i] if metadata else {}
                result = await self._engine.execute(
                    query, 
                    {"collection": collection, "vector": vector, "metadata": meta}
                )
                # Cast the row to use string keys
                row = cast(dict[str, Any], result.rows[0])
                results.append(row["id"])
            
            return results

        except Exception as e:
            raise VectorError(f"Failed to store vectors: {e}", cause=e)

    async def search_similar(
        self, 
        collection: str,
        query_vector: list[float],
        limit: int = 10,
        threshold: float = 0.8
    ) -> list[VectorResult]:
        """Search for similar vectors"""
        if not self._initialized:
            await self.initialize()

        if not self._engine:
            raise VectorError("Database engine not initialized")

        try:
            query = """
            SELECT id, vector, metadata, 
                   1 - (vector <=> $1::vector) as similarity
            FROM ai_vectors
            WHERE collection = $2
              AND 1 - (vector <=> $1::vector) >= $3
            ORDER BY vector <=> $1::vector
            LIMIT $4;
            """
            
            result = await self._engine.execute(
                query,
                {
                    "vector": query_vector,
                    "collection": collection,
                    "threshold": threshold,
                    "limit": limit
                }
            )

            return [
                VectorResult(
                    id=cast(dict[str, Any], row)["id"],
                    vector=cast(dict[str, Any], row)["vector"],
                    similarity=cast(dict[str, Any], row)["similarity"],
                    metadata=cast(dict[str, Any], row)["metadata"]
                )
                for row in result.rows
            ]

        except Exception as e:
            raise VectorError(f"Vector similarity search failed: {e}", cause=e)

    async def cleanup(self) -> None:
        """Cleanup resources"""
        if self._engine:
            await self._engine.cleanup()
        self._initialized = False 