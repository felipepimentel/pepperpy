"""Text analyzer implementation"""

from pathlib import Path
from typing import Any

from pepperpy.core.module import InitializableModule
from pepperpy.core.validation import ValidatorFactory

from .config import TextProcessorConfig
from .exceptions import TextProcessorError
from .handlers import EPUBHandler
from .types import FileType, TextAnalysisResult


class TextAnalyzer(InitializableModule):
    """Text analyzer implementation"""

    def __init__(self, config: TextProcessorConfig) -> None:
        super().__init__()
        self.config = config
        self._config_validator = ValidatorFactory.create_schema_validator(TextProcessorConfig)
        self._current_file: Path | None = None
        self._handlers = {
            FileType.DOCUMENT: {
                "epub": EPUBHandler(),
            }
        }

    async def _initialize(self) -> None:
        """Initialize analyzer"""
        result = await self._config_validator.validate(self.config.dict())
        if not result.is_valid:
            raise TextProcessorError(f"Invalid configuration: {', '.join(result.errors)}")

    async def _cleanup(self) -> None:
        """Cleanup analyzer resources"""
        self._current_file = None
        self._handlers.clear()

    async def analyze_file(self, file_path: Path) -> TextAnalysisResult:
        """Analyze file content"""
        self._ensure_initialized()
        try:
            self._current_file = file_path
            suffix = file_path.suffix.lower()[1:]  # Remove o ponto
            handler = self._get_handler(suffix)

            file_content = await handler.read(file_path)
            if hasattr(file_content.content, "chapters"):
                content = "\n\n".join(
                    f"# {chapter.title}\n{chapter.content}"
                    for chapter in file_content.content.chapters
                )
            else:
                content = str(file_content.content)

            return TextAnalysisResult(
                content=content,
                metadata={"file": str(file_path), **file_content.metadata}
            )
        except Exception as e:
            raise TextProcessorError(f"File analysis failed: {e}", cause=e)
        finally:
            self._current_file = None

    def _get_handler(self, suffix: str) -> Any:
        """Get appropriate file handler"""
        for handlers in self._handlers.values():
            if suffix in handlers:
                return handlers[suffix]
        raise TextProcessorError(f"No handler found for file type: {suffix}")
