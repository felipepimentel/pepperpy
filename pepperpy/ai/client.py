"""AI client implementation"""

from typing import Any, AsyncGenerator

from pepperpy.core.module import BaseModule
from pepperpy.db.vector import VectorEngine

from .config import AIConfig
from .exceptions import AIError
from .types import AIResponse


class AIClient(BaseModule[AIConfig]):
    """AI client implementation"""

    def __init__(self, config: AIConfig) -> None:
        super().__init__(config)
        self._vector_engine: VectorEngine | None = None

    async def _initialize(self) -> None:
        """Initialize client"""
        if self.config.vector_enabled and not self._vector_engine and self.config.vector_config:
            self._vector_engine = VectorEngine(self.config.vector_config)
            await self._vector_engine.initialize()

    async def _cleanup(self) -> None:
        """Cleanup resources"""
        if self._vector_engine:
            await self._vector_engine.cleanup()

    async def complete(self, prompt: str) -> AIResponse:
        """Complete text using AI model"""
        if not self._initialized:
            await self.initialize()

        try:
            return AIResponse(
                content=f"AI response to: {prompt}",
                model=self.config.model,
            )
        except Exception as e:
            raise AIError(f"Completion failed: {e}", cause=e)

    async def stream(self, prompt: str) -> AsyncGenerator[str, None]:
        """Stream text generation results"""
        if not self._initialized:
            await self.initialize()

        try:
            # Implementação real aqui
            yield f"Streaming response to: {prompt}"
        except Exception as e:
            raise AIError(f"Stream generation failed: {e}", cause=e)

    async def get_embedding(self, text: str) -> list[float]:
        """Get text embedding"""
        if not self._initialized:
            await self.initialize()

        try:
            # Implementação real aqui
            # Retorna um vetor de exemplo com dimensão 1536 (padrão OpenAI)
            return [0.0] * 1536
        except Exception as e:
            raise AIError(f"Embedding generation failed: {e}", cause=e)

    async def find_similar(
        self,
        collection: str,
        text: str,
        limit: int = 10,
        threshold: float = 0.8,
    ) -> list[dict[str, Any]]:
        """Find similar texts by embedding"""
        if not self._initialized:
            await self.initialize()

        try:
            if not self._vector_engine:
                raise AIError("Vector engine not initialized")

            # Gerar embedding para o texto de consulta
            embedding = await self.get_embedding(text)

            # Buscar vetores similares
            results = await self._vector_engine.search_similar(
                collection=collection,
                query_vector=embedding,
                limit=limit,
                threshold=threshold,
            )

            return [
                {
                    "id": result.id,
                    "similarity": result.similarity,
                    "metadata": result.metadata,
                }
                for result in results
            ]
        except Exception as e:
            raise AIError(f"Similarity search failed: {e}", cause=e)

    async def cleanup(self) -> None:
        """Cleanup resources"""
        if self._vector_engine:
            await self._vector_engine.cleanup()
        self._initialized = False
