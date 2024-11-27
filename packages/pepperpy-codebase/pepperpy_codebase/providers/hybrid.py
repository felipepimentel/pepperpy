"""Hybrid codebase provider implementation"""

from typing import Any, AsyncGenerator, Sequence

from ..config import CodebaseConfig
from ..exceptions import CodebaseError
from ..types import CodeFile, CodeSearchResult
from .analysis import StaticAnalysisProvider
from .base import BaseProvider


class HybridProvider(BaseProvider):
    """Hybrid provider implementation"""

    def __init__(self, config: CodebaseConfig) -> None:
        super().__init__(config)
        self._static_provider = StaticAnalysisProvider(config)

    async def _initialize(self) -> None:
        """Initialize provider"""
        try:
            await self._static_provider.initialize()
        except Exception as e:
            raise CodebaseError(f"Failed to initialize hybrid provider: {e}", cause=e)

    async def _cleanup(self) -> None:
        """Cleanup provider resources"""
        await self._static_provider.cleanup()

    async def search(self, query: str, **kwargs: Any) -> AsyncGenerator[CodeSearchResult, None]:
        """Search codebase"""
        try:
            # First try static analysis
            async for result in self._static_provider.search(query, **kwargs):
                yield result

            # TODO: Add dynamic/LLM-based search
        except Exception as e:
            raise CodebaseError(f"Hybrid search failed: {e}", cause=e)

    async def get_file(self, path: str) -> CodeFile:
        """Get file content"""
        return await self._static_provider.get_file(path)

    async def get_files(self, pattern: str) -> Sequence[CodeFile]:
        """Get files matching pattern"""
        return await self._static_provider.get_files(pattern)
