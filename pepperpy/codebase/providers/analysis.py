"""Static analysis provider implementation"""

from pathlib import Path
from typing import Any, AsyncGenerator, Sequence

from ..exceptions import CodebaseError
from ..types import CodeFile, CodeSearchResult
from .base import BaseProvider


class StaticAnalysisProvider(BaseProvider):
    """Static analysis provider implementation"""

    async def _initialize(self) -> None:
        """Initialize provider"""
        try:
            if not self.config.root_path.exists():
                raise CodebaseError(f"Root path does not exist: {self.config.root_path}")
        except Exception as e:
            raise CodebaseError(f"Failed to initialize static analysis provider: {e}", cause=e)

    async def _cleanup(self) -> None:
        """Cleanup provider resources"""
        pass

    async def search(self, query: str, **kwargs: Any) -> AsyncGenerator[CodeSearchResult, None]:
        """Search codebase"""
        try:
            for file in self._find_files():
                if await self._matches_query(file, query):
                    yield CodeSearchResult(
                        file=file,
                        score=1.0,
                        metadata={"provider": "static_analysis"},
                    )
        except Exception as e:
            raise CodebaseError(f"Static analysis search failed: {e}", cause=e)

    async def get_file(self, path: str) -> CodeFile:
        """Get file content"""
        try:
            file_path = Path(path)
            if not file_path.exists():
                raise CodebaseError(f"File not found: {path}")

            content = await self._read_file(file_path)
            return CodeFile(
                path=str(file_path),
                content=content,
                metadata={"provider": "static_analysis"},
            )
        except Exception as e:
            raise CodebaseError(f"Failed to get file: {e}", cause=e)

    async def get_files(self, pattern: str) -> Sequence[CodeFile]:
        """Get files matching pattern"""
        try:
            files = []
            for file_path in self.config.root_path.glob(pattern):
                if file_path.is_file():
                    content = await self._read_file(file_path)
                    files.append(
                        CodeFile(
                            path=str(file_path),
                            content=content,
                            metadata={"provider": "static_analysis"},
                        )
                    )
            return files
        except Exception as e:
            raise CodebaseError(f"Failed to get files: {e}", cause=e)

    def _find_files(self) -> Sequence[Path]:
        """Find all files in codebase"""
        files = []
        for file_path in self.config.root_path.rglob("*"):
            if file_path.is_file() and not self._is_ignored(file_path):
                files.append(file_path)
        return files

    def _is_ignored(self, path: Path) -> bool:
        """Check if path should be ignored"""
        for pattern in self.config.ignore_patterns:
            if path.match(pattern):
                return True
        return False

    async def _read_file(self, path: Path) -> str:
        """Read file content"""
        if path.stat().st_size > self.config.max_file_size:
            raise CodebaseError(f"File too large: {path}")
        return path.read_text(encoding=self.config.encoding)

    async def _matches_query(self, file: Path, query: str) -> bool:
        """Check if file matches query"""
        try:
            content = await self._read_file(file)
            return query.lower() in content.lower()
        except Exception:
            return False
