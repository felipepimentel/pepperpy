"""Code analysis engine"""

from pathlib import Path
from typing import Any, AsyncGenerator

from pepperpy.ai.client import AIClient
from pepperpy.core.module import BaseModule

from .config import CodebaseConfig
from .exceptions import CodebaseError
from .indexer import CodeIndexer
from .providers import get_provider
from .types import CodeEntity, RefactorSuggestion, ReviewComment, ScanResult


class CodebaseEngine(BaseModule):
    """Code analysis engine"""

    def __init__(
        self, config: CodebaseConfig, ai_client: AIClient | None = None, **kwargs: Any
    ) -> None:
        self.config = config
        self._ai_client = ai_client
        self._indexer = CodeIndexer(config)
        self._provider = None
        self._initialized = False

    async def initialize(self) -> None:
        """Initialize codebase engine"""
        if self._initialized:
            return

        # Initialize provider
        self._provider = await get_provider(self.config.provider, self.config, self._ai_client)
        if not self._provider:
            raise CodebaseError("Failed to initialize provider")
            
        await self._provider.initialize()

        # Initialize indexer
        await self._indexer.initialize()

        self._initialized = True

    async def scan_project(self, path: Path) -> ScanResult:
        """Scan and analyze project"""
        if not self._initialized:
            await self.initialize()

        if not self._provider:
            raise CodebaseError("Provider not initialized")

        # Index code first
        index = await self._indexer.index_project(path)

        # Run analysis through provider
        return await self._provider.scan_code(index)

    async def get_reviews(self, entity: CodeEntity) -> AsyncGenerator[ReviewComment, None]:
        """Get code review comments"""
        if not self._initialized:
            await self.initialize()

        if not self._provider:
            raise CodebaseError("Provider not initialized")

        async for review in self._provider.stream_reviews(entity):
            yield review

    async def get_refactors(self, entity: CodeEntity) -> list[RefactorSuggestion]:
        """Get refactoring suggestions"""
        if not self._initialized:
            await self.initialize()

        if not self._provider:
            raise CodebaseError("Provider not initialized")

        return await self._provider.suggest_refactors(entity)

    async def cleanup(self) -> None:
        """Cleanup resources"""
        if self._provider:
            await self._provider.cleanup()
        await self._indexer.cleanup()
        self._initialized = False
