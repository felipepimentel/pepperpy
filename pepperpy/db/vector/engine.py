"""Vector database engine implementation"""

from time import perf_counter
from typing import Any, Sequence, cast

from pepperpy.core.module import InitializableModule
from pepperpy.core.validation import ValidatorFactory

from ..engines import BaseEngine
from ..exceptions import DatabaseError
from ..types import QueryResult
from .config import VectorConfig
from .exceptions import VectorError
from .types import VectorQuery, VectorResult, VectorRow


class VectorEngine(BaseEngine, InitializableModule):
    """Vector database engine implementation"""

    def __init__(self, config: VectorConfig) -> None:
        BaseEngine.__init__(self, config.db_config)
        InitializableModule.__init__(self)
        self.vector_config = config
        self._query_validator = ValidatorFactory.create_schema_validator(VectorQuery)
        self._vector_validator = ValidatorFactory.create_type_validator(list)

    async def _validate_query(self, query: VectorQuery) -> None:
        """Validate vector query"""
        result = await self._query_validator.validate(query.model_dump())
        if not result.is_valid:
            raise VectorError(f"Invalid vector query: {', '.join(result.errors)}")

    async def _validate_vectors(self, vectors: Sequence[list[float]]) -> None:
        """Validate vector data"""
        results = await self._vector_validator.validate_many(vectors)
        errors = []
        for i, result in enumerate(results):
            if not result.is_valid:
                errors.extend(f"Vector {i}: {err}" for err in result.errors)
        if errors:
            raise VectorError(f"Invalid vectors: {', '.join(errors)}")

    async def execute(self, query: str, params: dict[str, Any] | None = None) -> QueryResult:
        """Execute database query"""
        try:
            self._ensure_initialized()

            start_time = perf_counter()
            # Implement actual query execution here
            # This is a placeholder that should be overridden by concrete implementations
            execution_time = perf_counter() - start_time

            return QueryResult(rows=[], affected_rows=0, execution_time=execution_time)
        except Exception as e:
            raise DatabaseError(f"Query execution failed: {e}", cause=e)

    async def _initialize(self) -> None:
        """Initialize vector operations"""
        await super()._initialize()
        try:
            # Enable vector extension
            await self.execute("CREATE EXTENSION IF NOT EXISTS vector;")
            # Create vector table
            await self._create_vector_table()
        except Exception as e:
            raise VectorError("Failed to initialize vector engine", cause=e)

    async def _cleanup(self) -> None:
        """Cleanup vector operations"""
        # Implementar limpeza específica se necessário
        pass

    async def _create_vector_table(self) -> None:
        """Create vector storage table"""
        query = f"""
        CREATE TABLE IF NOT EXISTS vectors (
            id SERIAL PRIMARY KEY,
            collection TEXT NOT NULL,
            vector vector({self.vector_config.dimension}),
            metadata JSONB,
            created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
        );
        """
        await self.execute(query)

    async def store_vectors(
        self,
        collection: str,
        vectors: Sequence[list[float]],
        metadata: list[dict[str, Any]] | None = None,
    ) -> list[int]:
        """Store vectors in database"""
        try:
            self._ensure_initialized()
            await self._validate_vectors(vectors)

            query = """
            INSERT INTO vectors (collection, vector, metadata)
            VALUES ($1, $2, $3)
            RETURNING id;
            """

            results = []
            for i, vector in enumerate(vectors):
                meta = metadata[i] if metadata else {}
                result = await self.execute(
                    query, {"collection": collection, "vector": vector, "metadata": meta}
                )
                row = cast(VectorRow, result.rows[0])
                results.append(row["id"])

            return results
        except Exception as e:
            raise DatabaseError(f"Failed to store vectors: {e}", cause=e)

    async def search_similar(
        self, collection: str, query_vector: list[float], limit: int = 10, threshold: float = 0.8
    ) -> list[VectorResult]:
        """Search for similar vectors"""
        try:
            self._ensure_initialized()

            query_obj = VectorQuery(
                vector=query_vector, collection=collection, limit=limit, threshold=threshold
            )
            await self._validate_query(query_obj)

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
                    "limit": limit,
                },
            )

            return [
                VectorResult(
                    id=cast(VectorRow, row)["id"],
                    vector=cast(VectorRow, row)["vector"],
                    similarity=cast(VectorRow, row)["similarity"],
                    metadata=cast(VectorRow, row)["metadata"],
                )
                for row in result.rows
            ]
        except Exception as e:
            raise DatabaseError(f"Vector similarity search failed: {e}", cause=e)
