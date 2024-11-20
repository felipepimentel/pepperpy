"""Text chunking implementation"""

from typing import AsyncGenerator

from pepperpy.core.module import BaseModule

from .config import TextProcessorConfig
from .exceptions import TextProcessorError
from .types import TextChunk


class TextChunker(BaseModule[TextProcessorConfig]):
    """Text chunker implementation"""

    def __init__(self, config: TextProcessorConfig) -> None:
        super().__init__(config)
        self._chunk_size = config.chunk_size or 1000
        self._overlap = config.overlap or 0

    async def _initialize(self) -> None:
        """Initialize chunker"""
        pass

    async def _cleanup(self) -> None:
        """Cleanup resources"""
        pass

    async def chunk_text(self, text: str) -> AsyncGenerator[TextChunk, None]:
        """Split text into chunks"""
        if not self._initialized:
            await self.initialize()

        try:
            # Split text into chunks with overlap
            start = 0
            index = 0

            while start < len(text):
                end = min(start + self._chunk_size, len(text))
                
                # Adjust end to not split words
                if end < len(text):
                    while end > start and not text[end].isspace():
                        end -= 1
                    if end == start:  # No space found
                        end = min(start + self._chunk_size, len(text))

                chunk = text[start:end]
                yield TextChunk(
                    content=chunk.strip(),
                    index=index,
                    metadata={
                        "start": start,
                        "end": end,
                        "length": len(chunk)
                    }
                )

                start = end - self._overlap
                index += 1

        except Exception as e:
            raise TextProcessorError(f"Text chunking failed: {e}", cause=e)
