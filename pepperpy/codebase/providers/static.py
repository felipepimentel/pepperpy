"""Static code analysis provider"""

from typing import AsyncGenerator

from pepperpy.core.module import BaseModule

from ..types import (
    CodeEntity,
    IndexEntry,
    RefactorSuggestion,
    ReviewComment,
    ScanResult,
)


class StaticAnalysisProvider(BaseModule):
    """Static code analysis implementation"""

    async def _initialize(self) -> None:
        """Initialize provider"""
        pass

    async def _cleanup(self) -> None:
        """Cleanup resources"""
        pass

    async def scan_code(self, index: list[IndexEntry]) -> ScanResult:
        """Scan code using static analysis"""
        return ScanResult(
            success=True,
            entities=index,
            reviews=[],
            refactors=[],
            metadata={"tool": "static_analysis"},
        )

    async def stream_reviews(self, entity: CodeEntity) -> AsyncGenerator[ReviewComment, None]:
        """Stream code review comments"""
        yield ReviewComment(
            message="Static analysis review", location=entity.location, severity="info"
        )

    async def suggest_refactors(self, entity: CodeEntity) -> list[RefactorSuggestion]:
        """Suggest code refactorings"""
        return []
