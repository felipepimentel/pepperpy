"""Vector database engine"""

from typing import Any, Sequence, cast

from ..engines import BaseEngine
from ..exceptions import DatabaseError
from .config import VectorConfig
from .exceptions import VectorError
from .types import VectorResult, VectorRow


class VectorEngine(BaseEngine):
    """Vector database operations"""

    def __init__(self, config: VectorConfig) -> None:
        super().__init__(config.db_config)
        self.config = config
        self._initialized = False

    async def initialize(self) -> None:
        """Initialize vector operations"""
        if self._initialized:
            return

        try:
            await super().initialize()
            
            # Enable vector extension
            await self.execute("CREATE EXTENSION IF NOT EXISTS vector;")
            
            # Create vector table
            await self._create_vector_table()
            
            self._initialized = True
        except Exception as e:
            raise VectorError("Failed to initialize vector engine", cause=e)

    async def _create_vector_table(self) -> None:
        """Create vector storage table"""
        query = f"""
        CREATE TABLE IF NOT EXISTS vectors (
            id SERIAL PRIMARY KEY,
            collection TEXT NOT NULL,
            vector vector({self.config.dimension}),
            metadata JSONB,
            created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
        );
        CREATE INDEX IF NOT EXISTS vectors_collection_idx ON vectors(collection);
        CREATE INDEX IF NOT EXISTS vectors_vector_idx ON vectors 
        USING ivfflat (vector vector_cosine_ops)
        WITH (lists = 100);
        """
        await self.execute(query)

    async def store_vectors(
        self,
        collection: str,
        vectors: Sequence[list[float]],
        metadata: list[dict[str, Any]] | None = None
    ) -> list[int]:
        """Store vectors in database"""
        try:
            if not self._initialized:
                await self.initialize()

            query = """
            INSERT INTO vectors (collection, vector, metadata)
            VALUES ($1, $2, $3)
            RETURNING id;
            """
            
            results = []
            for i, vector in enumerate(vectors):
                meta = metadata[i] if metadata else {}
                result = await self.execute(
                    query,
                    {"collection": collection, "vector": vector, "metadata": meta}
                )
                # Cast row to correct type
                row = cast(VectorRow, result.rows[0])
                results.append(row["id"])
            
            return results
        except Exception as e:
            raise DatabaseError(f"Failed to store vectors: {e}", cause=e)

    async def search_similar(
        self,
        collection: str,
        query_vector: list[float],
        limit: int = 10,
        threshold: float = 0.8
    ) -> list[VectorResult]:
        """Search for similar vectors"""
        try:
            if not self._initialized:
                await self.initialize()

            query = """
            SELECT id, vector, metadata,
                   1 - (vector <=> $1::vector) as similarity
            FROM vectors
            WHERE collection = $2
              AND 1 - (vector <=> $1::vector) >= $3
            ORDER BY vector <=> $1::vector
            LIMIT $4;
            """
            
            result = await self.execute(
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
                    id=cast(VectorRow, row)["id"],
                    vector=cast(VectorRow, row)["vector"],
                    similarity=cast(VectorRow, row)["similarity"],
                    metadata=cast(VectorRow, row)["metadata"]
                )
                for row in result.rows
            ]
        except Exception as e:
            raise DatabaseError(f"Vector similarity search failed: {e}", cause=e) 