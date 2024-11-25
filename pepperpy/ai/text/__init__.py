"""Text processing package initialization"""

from .analyzer import TextAnalyzer
from .config import TextAnalyzerConfig, TextProcessorConfig
from .exceptions import TextAnalysisError, TextError
from .types import TextAnalysis, TextAnalysisResult

__all__ = [
    'TextAnalyzer',
    'TextAnalyzerConfig',
    'TextProcessorConfig',
    'TextAnalysisError',
    'TextError',
    'TextAnalysis',
    'TextAnalysisResult'
]
