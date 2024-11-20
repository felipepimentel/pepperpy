"""Text processing exceptions"""

from pepperpy.core.types import CoreError


class TextError(CoreError):
    """Base text error"""


class TextProcessorError(TextError):
    """Text processor error"""


class ChunkingError(TextError):
    """Text chunking error"""


class AnalysisError(TextError):
    """Text analysis error"""


class ProcessingError(TextError):
    """Text processing error"""
