"""EPUB text analysis"""

from dataclasses import asdict
from pathlib import Path

from pepperpy.core.module import BaseModule, ModuleMetadata
from pepperpy.files.handlers.epub import EPUBHandler
from pepperpy.files.types import Book

from .analyzer import TextAnalyzer
from .chunker import TextChunker
from .exceptions import AnalysisError
from .types import AnalysisConfig, AnalysisResult


class EPUBAnalyzer(BaseModule):
    """EPUB document analyzer"""

    def __init__(self, config: AnalysisConfig | None = None) -> None:
        super().__init__()
        self._config: AnalysisConfig = config or AnalysisConfig()
        self.metadata = ModuleMetadata(
            name="epub_analyzer",
            version="1.0.0",
            description="EPUB document analysis",
            dependencies=["spacy"],
            config=asdict(self._config),
        )
        self._analyzer = TextAnalyzer(config)
        self._chunker = TextChunker()
        self._handler = EPUBHandler()

    @property
    def config(self) -> AnalysisConfig:
        """Get analyzer configuration"""
        return self._config

    @config.setter
    def config(self, value: AnalysisConfig) -> None:
        """Set analyzer configuration"""
        self._config = value
        if hasattr(self, "metadata"):
            self.metadata.config = asdict(value)

    async def analyze_file(self, file_path: str | Path) -> AnalysisResult:
        """
        Analyze EPUB file content

        Args:
            file_path: Path to EPUB file

        Returns:
            AnalysisResult: Analysis results

        Raises:
            AnalysisError: If analysis fails
        """
        try:
            # Carregar EPUB
            content = await self._handler.read(file_path)
            book: Book = content.content

            # Extrair texto de todos os capítulos
            full_text = "\n\n".join(chapter.content for chapter in book.chapters)

            # Analisar texto completo
            result = await self._analyzer.analyze(full_text)

            # Adicionar metadados do EPUB
            result.metadata.update(
                {
                    "title": book.metadata.title,
                    "authors": book.metadata.authors,
                    "language": book.metadata.language,
                    "chapters": len(book.chapters),
                    "file_path": str(file_path),
                }
            )

            return result

        except Exception as e:
            raise AnalysisError(f"EPUB analysis failed: {e!s}", cause=e)

    async def analyze_chapter(self, chapter_content: str) -> AnalysisResult:
        """
        Analyze single chapter content

        Args:
            chapter_content: Chapter text content

        Returns:
            AnalysisResult: Analysis results

        Raises:
            AnalysisError: If analysis fails
        """
        try:
            return await self._analyzer.analyze(chapter_content)
        except Exception as e:
            raise AnalysisError(f"Chapter analysis failed: {e!s}", cause=e)

    async def _setup(self) -> None:
        """Setup analyzer"""
        await self._analyzer._setup()

    async def _cleanup(self) -> None:
        """Cleanup analyzer"""
        await self._analyzer._cleanup()


# Global analyzer instance
epub_analyzer = EPUBAnalyzer()
