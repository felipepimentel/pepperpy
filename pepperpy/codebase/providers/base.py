"""Base provider for code analysis"""

from abc import ABC, abstractmethod
from typing import AsyncGenerator, Protocol

from pepperpy.core.module import BaseModule

from ..types import CodeEntity, IndexEntry, RefactorSuggestion, ReviewComment, ScanResult


class CodeScanProvider(Protocol):
    """Protocol for code scan providers"""

    async def initialize(self) -> None:
        """Initialize provider"""
        ...

    async def scan_code(self, index: list[IndexEntry]) -> ScanResult:
        """Scan code and provide analysis"""
        ...

    async def stream_reviews(self, entity: CodeEntity) -> AsyncGenerator[ReviewComment, None]:
        """Stream code review comments"""
        ...

    async def suggest_refactors(self, entity: CodeEntity) -> list[RefactorSuggestion]:
        """Suggest code refactorings"""
        ...

    async def cleanup(self) -> None:
        """Cleanup resources"""
        ...


class BaseCodeProvider(BaseModule, ABC):
    """Base class for code analysis providers"""

    @abstractmethod
    async def initialize(self) -> None:
        """Initialize provider"""
        ...

    @abstractmethod
    async def scan_code(self, index: list[IndexEntry]) -> ScanResult:
        """Scan code and provide analysis"""
        ...

    @abstractmethod
    async def stream_reviews(self, entity: CodeEntity) -> AsyncGenerator[ReviewComment, None]:
        """Stream code review comments"""
        ...

    @abstractmethod
    async def suggest_refactors(self, entity: CodeEntity) -> list[RefactorSuggestion]:
        """Suggest code refactorings"""
        ...

    @abstractmethod
    async def cleanup(self) -> None:
        """Cleanup resources"""
        ...
