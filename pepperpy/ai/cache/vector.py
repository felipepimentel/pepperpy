"""Vector cache implementation"""

from typing import Any, Dict, List, Optional

import numpy as np
from sklearn.neighbors import NearestNeighbors

from .config import CacheConfig
from .exceptions import CacheError
from .types import VectorEntry


class VectorCache:
    """Cache for vector embeddings"""

    def __init__(self, config: CacheConfig):
        self.config = config
        self._vectors = []
        self._metadata = []
        self._index = None

    async def initialize(self) -> None:
        """Initialize vector cache"""
        try:
            self._index = NearestNeighbors(
                n_neighbors=min(10, self.config.max_size), metric="cosine"
            )
        except Exception as e:
            raise CacheError(f"Failed to initialize vector cache: {str(e)}", cause=e)

    async def cleanup(self) -> None:
        """Cleanup vector cache"""
        self._vectors = []
        self._metadata = []
        self._index = None

    async def add(self, key: str, vector: Any, metadata: Optional[Dict] = None) -> None:
        """Add vector to cache"""
        try:
            vector = np.array(vector).reshape(1, -1)
            self._vectors.append(vector)
            self._metadata.append(VectorEntry(key=key, vector=vector, metadata=metadata or {}))

            if len(self._vectors) > 1:
                self._index.fit(np.vstack(self._vectors))
        except Exception as e:
            raise CacheError(f"Failed to add vector: {str(e)}", cause=e)

    async def search(
        self, vector: Any, limit: int = 1, threshold: float = 0.8
    ) -> List[VectorEntry]:
        """Search for similar vectors"""
        try:
            if not self._vectors:
                return []

            vector = np.array(vector).reshape(1, -1)
            distances, indices = self._index.kneighbors(
                vector, n_neighbors=min(limit, len(self._vectors))
            )

            results = []
            for dist, idx in zip(distances[0], indices[0]):
                similarity = 1 - dist
                if similarity >= threshold:
                    results.append(self._metadata[idx])

            return results
        except Exception as e:
            raise CacheError(f"Vector search failed: {str(e)}", cause=e)
