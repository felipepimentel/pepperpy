"""Hybrid code analysis provider combining static analysis and AI"""

from typing import AsyncGenerator

from pepperpy.ai.client import AIClient

from ..types import (
    CodeEntity,
    IndexEntry,
    RefactorSuggestion,
    ReviewComment,
    ScanResult,
)
from .base import BaseCodeProvider
from .static import StaticAnalysisProvider


class HybridProvider(BaseCodeProvider):
    """Combines static analysis with AI insights"""

    def __init__(self, ai_client: AIClient) -> None:
        self._ai_client = ai_client
        self._static_provider = StaticAnalysisProvider()
        self._initialized = False

    async def initialize(self) -> None:
        """Initialize provider"""
        if self._initialized:
            return
        await self._static_provider.initialize()
        await self._ai_client.initialize()
        self._initialized = True

    async def scan_code(self, index: list[IndexEntry]) -> ScanResult:
        """Scan code using both static analysis and AI"""
        if not self._initialized:
            await self.initialize()

        # Get static analysis results
        static_result = await self._static_provider.scan_code(index)

        # Enhance with AI insights
        ai_insights = await self._get_ai_insights(index)

        # Combine results
        return ScanResult(
            success=static_result.success and ai_insights.success,
            entities=static_result.entities,
            reviews=[*static_result.reviews, *ai_insights.reviews],
            refactors=[*static_result.refactors, *ai_insights.refactors],
            metadata={**static_result.metadata, **ai_insights.metadata, "provider": "hybrid"},
        )

    async def _get_ai_insights(self, index: list[IndexEntry]) -> ScanResult:
        """Get AI insights for code"""
        # Implement AI analysis using self._ai_client
        raise NotImplementedError

    async def stream_reviews(self, entity: CodeEntity) -> AsyncGenerator[ReviewComment, None]:
        """Stream reviews from both static analysis and AI"""
        # Get static analysis reviews
        async for review in self._static_provider.stream_reviews(entity):
            yield review

        # Get AI reviews
        # Implement AI review streaming
        raise NotImplementedError

    async def suggest_refactors(self, entity: CodeEntity) -> list[RefactorSuggestion]:
        """Get refactoring suggestions from both sources"""
        # Get static analysis suggestions
        static_suggestions = await self._static_provider.suggest_refactors(entity)

        # Get AI suggestions
        # Implement AI refactoring suggestions
        raise NotImplementedError

        return static_suggestions  # + ai_suggestions

    async def cleanup(self) -> None:
        """Cleanup resources"""
        await self._static_provider.cleanup()
        self._initialized = False
