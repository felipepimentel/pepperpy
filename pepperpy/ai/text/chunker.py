"""Text chunking implementation"""

from typing import List

from ...core.exceptions import PepperPyError
from ...core.module import BaseModule
from .config import TextProcessorConfig


class TextChunker(BaseModule[TextProcessorConfig]):
    """Text chunker implementation"""

    def __init__(self, config: TextProcessorConfig) -> None:
        """Initialize chunker.

        Args:
            config: Chunker configuration
        """
        super().__init__(config)
        self._chunk_size = config.metadata.get("chunk_size", 1000)
        self._overlap = config.metadata.get("overlap", 200)

    def chunk_text(self, text: str) -> List[str]:
        """Split text into chunks.

        Args:
            text: Text to split

        Returns:
            List[str]: List of text chunks

        Raises:
            PepperPyError: If chunking fails
        """
        try:
            if not text:
                return []

            # Split text into sentences (simple implementation)
            sentences = [s.strip() for s in text.split(".") if s.strip()]

            chunks: List[str] = []
            current_chunk = ""

            for sentence in sentences:
                # If adding this sentence would exceed chunk size
                if len(current_chunk) + len(sentence) > self._chunk_size:
                    # Save current chunk if not empty
                    if current_chunk:
                        chunks.append(current_chunk.strip())

                    # Start new chunk with overlap from previous chunk
                    if self._overlap > 0 and current_chunk:
                        words = current_chunk.split()
                        overlap_words = words[-min(len(words), self._overlap // 10) :]
                        current_chunk = " ".join(overlap_words) + " " + sentence
                    else:
                        current_chunk = sentence
                else:
                    # Add sentence to current chunk
                    current_chunk = (current_chunk + " " + sentence).strip()

            # Add final chunk if not empty
            if current_chunk:
                chunks.append(current_chunk.strip())

            return chunks

        except Exception as e:
            raise PepperPyError(f"Failed to chunk text: {e}", cause=e)

    async def _initialize(self) -> None:
        """Initialize chunker"""
        pass

    async def _cleanup(self) -> None:
        """Cleanup chunker resources"""
        pass
