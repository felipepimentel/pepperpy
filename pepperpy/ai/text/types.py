"""Text analysis types"""

from dataclasses import dataclass, field

from pepperpy.core.types import JsonDict


@dataclass
class TextAnalysisResult:
    """Text analysis result"""

    content: str
    metadata: JsonDict = field(default_factory=dict)


@dataclass
class TextChunk:
    """Text chunk"""

    content: str
    index: int
    metadata: JsonDict = field(default_factory=dict)
