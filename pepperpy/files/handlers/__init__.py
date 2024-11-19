"""File handlers package"""

from .audio import AudioHandler
from .base import FileHandler
from .compression import CompressionHandler
from .document import DocumentHandler
from .epub import EPUBHandler
from .image import ImageHandler
from .json import JSONHandler
from .markdown import MarkdownHandler
from .markdown_enhanced import MarkdownEnhancedHandler
from .markup import MarkupHandler
from .media import MediaHandler
from .optimizer import FileOptimizer
from .pdf import PDFHandler
from .spreadsheet import SpreadsheetHandler
from .yaml import YAMLHandler

__all__ = [
    # Base
    "FileHandler",
    # Handlers
    "AudioHandler",
    "CompressionHandler",
    "DocumentHandler",
    "EPUBHandler",
    "FileOptimizer",
    "ImageHandler",
    "JSONHandler",
    "MarkdownHandler",
    "MarkdownEnhancedHandler",
    "MarkupHandler",
    "MediaHandler",
    "PDFHandler",
    "SpreadsheetHandler",
    "YAMLHandler",
]
