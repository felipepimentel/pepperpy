"""Text processor implementation"""

from typing import Any

from ...core.exceptions import PepperPyError
from ...core.module import BaseModule
from .config import TextProcessorConfig


class TextProcessor(BaseModule[TextProcessorConfig]):
    """Text processor implementation"""

    def __init__(self, config: TextProcessorConfig) -> None:
        """Initialize processor.
        
        Args:
            config: Processor configuration
        """
        super().__init__(config)
        self._normalize_whitespace = config.metadata.get("normalize_whitespace", True)

    async def _initialize(self) -> None:
        """Initialize processor"""
        pass

    async def _cleanup(self) -> None:
        """Cleanup processor resources"""
        pass

    def process_text(self, text: str, **kwargs: Any) -> str:
        """Process text.
        
        Args:
            text: Text to process
            **kwargs: Additional processing options
            
        Returns:
            str: Processed text
            
        Raises:
            PepperPyError: If processing fails
        """
        try:
            if not text:
                return ""

            processed = text

            # Normalize whitespace if enabled
            if self._normalize_whitespace:
                # Replace multiple spaces with single space
                processed = " ".join(processed.split())
                # Remove leading/trailing whitespace
                processed = processed.strip()

            return processed

        except Exception as e:
            raise PepperPyError(f"Failed to process text: {e}", cause=e)
