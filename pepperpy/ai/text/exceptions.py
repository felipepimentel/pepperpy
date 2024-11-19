"""Text processing exceptions"""

from pepperpy.core.exceptions import PepperPyError


class TextError(PepperPyError):
    """Base text processing error"""


class ProcessingError(TextError):
    """Text processing error"""


class ChunkingError(TextError):
    """Text chunking error"""


class AnalysisError(TextError):
    """Text analysis error"""
