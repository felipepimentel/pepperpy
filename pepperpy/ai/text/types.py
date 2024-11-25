"""Text processor types"""

from dataclasses import dataclass, field
from enum import Enum, auto
from typing import Any, Dict

from pepperpy.core.types import JsonDict


class FileType(Enum):
    """File type enumeration"""

    DOCUMENT = auto()
    CODE = auto()
    DATA = auto()


class TextAnalysisResult:
    """Text analysis result"""

    def __init__(self, content: str, metadata: JsonDict | None = None) -> None:
        self.content = content
        self.metadata = metadata or {}


@dataclass
class TextChunk:
    """Text chunk"""

    content: str
    index: int
    metadata: JsonDict = field(default_factory=dict)


@dataclass
class TextAnalysis:
    """Result of text analysis"""

    text: str
    language: str
    word_count: int
    sentence_count: int
    avg_word_length: float
    avg_sentence_length: float
    complexity_score: float
    metadata: Dict[str, Any] = field(default_factory=dict)
