"""Sentence Transformers embedding provider."""

from typing import Any, cast

from ..base import EmbeddingProvider

# Define module-level variables
_have_sentence_transformers = False
_sentence_transformers = None
_SentenceTransformer: type[Any] | None = None

try:
    import sentence_transformers  # type: ignore
    from sentence_transformers import SentenceTransformer  # type: ignore

    _sentence_transformers = sentence_transformers
    _SentenceTransformer = SentenceTransformer
    _have_sentence_transformers = True
except ImportError:
    pass


class SentenceTransformersProvider(EmbeddingProvider):
    """Sentence Transformers embedding provider."""

    def __init__(self, config: Any) -> None:
        """Initialize provider."""
        super().__init__(config)
        self._model: Any | None = None

    async def _setup(self) -> None:
        """Setup provider resources.

        Raises:
            ImportError: If sentence-transformers is not installed
            RuntimeError: If model initialization fails
        """
        if not _have_sentence_transformers or _SentenceTransformer is None:
            raise ImportError(
                "sentence-transformers package not installed. "
                "Please install it with: pip install sentence-transformers"
            )

        try:
            model_name = self.config.settings["model_name"]
            device = self.config.settings.get("device", "cpu")
            model_class = cast(type[Any], _SentenceTransformer)
            self._model = model_class(model_name_or_path=model_name, device=device)
        except (AttributeError, ImportError) as e:
            raise RuntimeError(
                "Failed to initialize SentenceTransformer model. "
                "Please ensure you have the correct version installed."
            ) from e

    async def _teardown(self) -> None:
        """Teardown provider resources."""
        self._model = None

    async def embed(self, text: str) -> list[float]:
        """Generate embedding for text.

        Args:
            text: Text to embed

        Returns:
            Embedding vector

        Raises:
            RuntimeError: If provider not initialized
        """
        if not self.is_initialized or not self._model:
            raise RuntimeError("Provider not initialized")

        # Generate embedding
        embedding = self._model.encode(
            text,
            batch_size=self.config.settings.get("batch_size", 32),
            normalize_embeddings=self.config.settings.get("normalize_embeddings", True),
        )

        return cast(list[float], embedding.tolist())

    async def embed_batch(self, texts: list[str]) -> list[list[float]]:
        """Generate embeddings for multiple texts.

        Args:
            texts: Texts to embed

        Returns:
            List of embedding vectors

        Raises:
            RuntimeError: If provider not initialized
        """
        if not self.is_initialized or not self._model:
            raise RuntimeError("Provider not initialized")

        # Generate embeddings
        embeddings = self._model.encode(
            texts,
            batch_size=self.config.settings.get("batch_size", 32),
            normalize_embeddings=self.config.settings.get("normalize_embeddings", True),
        )

        return cast(list[list[float]], embeddings.tolist())
