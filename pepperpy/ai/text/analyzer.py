"""Text analyzer implementation"""

from pathlib import Path
from typing import Any

from pepperpy.core.module import BaseModule
from pepperpy.files.handlers.epub import EPUBHandler
from pepperpy.files.types import FileType

from .config import TextProcessorConfig
from .exceptions import TextProcessorError
from .types import TextAnalysisResult


class TextAnalyzer(BaseModule[TextProcessorConfig]):
    """Text analyzer implementation"""

    def __init__(self, config: TextProcessorConfig) -> None:
        super().__init__(config)
        self._current_file: Path | None = None
        self._handlers = {
            FileType.DOCUMENT: {
                "epub": EPUBHandler(),
                # Adicionar outros handlers conforme necessário
            }
        }

    async def analyze_file(self, file_path: Path) -> TextAnalysisResult:
        """Analyze file content"""
        if not self._initialized:
            await self.initialize()

        try:
            self._current_file = file_path
            suffix = file_path.suffix.lower()[1:]  # Remove o ponto
            handler = self._get_handler(suffix)

            file_content = await handler.read(file_path)
            if hasattr(file_content.content, "chapters"):
                # Processar conteúdo de livro (EPUB, etc)
                content = "\n\n".join(
                    f"# {chapter.title}\n{chapter.content}"
                    for chapter in file_content.content.chapters
                )
            else:
                content = str(file_content.content)

            return TextAnalysisResult(
                content=content, metadata={"file": str(file_path), **file_content.metadata}
            )
        except Exception as e:
            raise TextProcessorError(f"File analysis failed: {e}", cause=e)
        finally:
            self._current_file = None

    def _get_handler(self, format_str: str) -> Any:
        """Get appropriate file handler"""
        for handlers in self._handlers.values():
            if format_str in handlers:
                return handlers[format_str]
        raise TextProcessorError(f"No handler found for format: {format_str}")
