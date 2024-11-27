"""File handlers package"""

from .audio import AudioFileHandler
from .base import BaseFileHandler
from .binary import BinaryFileHandler
from .csv import CSVFileHandler
from .json import JSONFileHandler
from .markdown import MarkdownFileHandler
from .optimizer import FileOptimizerHandler
from .pdf import PDFFileHandler
from .text import TextFileHandler
from .yaml import YAMLFileHandler

__all__ = [
    "BaseFileHandler",
    "TextFileHandler",
    "JSONFileHandler",
    "YAMLFileHandler",
    "CSVFileHandler",
    "BinaryFileHandler",
    "AudioFileHandler",
    "PDFFileHandler",
    "MarkdownFileHandler",
    "FileOptimizerHandler",
]
