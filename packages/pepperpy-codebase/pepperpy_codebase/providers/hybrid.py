"""Hybrid provider implementation."""

from collections.abc import Sequence
from typing import Any

from ..config import CodebaseConfig
from ..types import FileContent
from .analysis import AnalysisProvider
from .base import BaseProvider, SearchResult


class HybridProvider(BaseProvider[CodebaseConfig]):
    """Hybrid provider implementation.

    Combines static analysis with AI-powered analysis.
    """

    def __init__(self, config: CodebaseConfig) -> None:
        """Initialize provider.

        Args:
            config: Provider configuration
        """
        super().__init__(config)
        self._analysis_provider = AnalysisProvider(config)

    async def _setup(self) -> None:
        """Setup provider resources."""
        await self._analysis_provider.initialize()

    async def _teardown(self) -> None:
        """Teardown provider resources."""
        await self._analysis_provider.cleanup()

    async def get_file(self, path: str) -> FileContent | None:
        """Get file content."""
        self._ensure_initialized()
        return await self._analysis_provider.get_file(path)

    async def search(self, query: str, **kwargs: Any) -> Sequence[SearchResult]:
        """Search files."""
        self._ensure_initialized()

        # Combine static and AI-powered search
        static_results = await self._analysis_provider.search(query, **kwargs)

        # TODO: Add AI-powered search enhancement
        # This could include:
        # - Semantic search
        # - Natural language understanding
        # - Code similarity analysis

        return static_results

    async def analyze_file(self, file: FileContent) -> dict[str, Any]:
        """Analyze file.

        Args:
            file: File to analyze

        Returns:
            Analysis results

        Raises:
            RuntimeError: If provider not initialized
        """
        self._ensure_initialized()

        # Get static analysis results
        static_results = await self._analysis_provider.analyze_file(file)

        # TODO: Add AI-powered analysis
        # This could include:
        # - Code quality assessment
        # - Security analysis
        # - Best practices recommendations

        return {
            "static_analysis": static_results,
            "ai_analysis": {
                "quality_score": 0.0,
                "security_score": 0.0,
                "recommendations": [],
            },
        }

    async def get_stats(self) -> dict[str, Any]:
        """Get provider statistics."""
        self._ensure_initialized()

        static_stats = await self._analysis_provider.get_stats()
        return {
            **static_stats,
            "ai_queries": 0,
            "ai_suggestions": 0,
        }
