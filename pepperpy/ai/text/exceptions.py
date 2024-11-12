"""Text processing exceptions"""

from pepperpy.core.exceptions import CoreError


class TextProcessingError(CoreError):
    """Base exception for text processing errors"""

    pass


class TextValidationError(TextProcessingError):
    """Error during text validation"""

    pass


class TextChunkingError(TextProcessingError):
    """Error during text chunking"""

    pass
