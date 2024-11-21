"""Text processor types"""

from dataclasses import dataclass, field
from enum import Enum, auto

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
