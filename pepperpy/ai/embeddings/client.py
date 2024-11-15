"""Embedding client implementation"""


from pepperpy.core.module import BaseModule, ModuleMetadata

from .config import EmbeddingConfig
from .exceptions import EmbeddingError
from .providers import get_provider
from .providers.base import BaseEmbeddingProvider
from .types import EmbeddingVector


class EmbeddingClient(BaseModule):
    """Client for embedding operations"""

    _config: EmbeddingConfig | None
    _provider: BaseEmbeddingProvider | None

    def __init__(self, config: EmbeddingConfig | None = None):
        super().__init__()
        self._config = config or EmbeddingConfig(
            model="all-MiniLM-L6-v2",
            provider="sentence_transformers",
        )
        self.metadata = ModuleMetadata(
            name="embeddings",
            version="1.0.0",
            description="Text embedding operations",
            dependencies=[],
            config=self._config.dict(),
        )
        self._provider = None

    async def _setup(self) -> None:
        """Initialize embedding provider"""
        try:
            if not self._config:
                raise EmbeddingError("Embedding configuration is required")
            self._provider = get_provider(self._config)
            if hasattr(self._provider, "initialize"):
                await self._provider.initialize()
        except Exception as e:
            raise EmbeddingError("Failed to initialize embedding provider", cause=e)

    async def _cleanup(self) -> None:
        """Cleanup embedding resources"""
        if self._provider and hasattr(self._provider, "cleanup"):
            await self._provider.cleanup()

    async def embed(self, text: str) -> EmbeddingVector:
        """Generate embedding for text"""
        if not self._provider:
            raise EmbeddingError("Embedding provider not initialized")
        return await self._provider.embed_text(text)

    async def embed_batch(self, texts: list[str]) -> list[EmbeddingVector]:
        """Generate embeddings for multiple texts"""
        if not self._provider:
            raise EmbeddingError("Embedding provider not initialized")
        return await self._provider.embed_batch(texts)


# Global embedding client instance
embeddings = EmbeddingClient()
