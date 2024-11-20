"""Text processor configuration"""

from dataclasses import dataclass, field

from pepperpy.core.types import JsonDict, ModuleConfig


@dataclass
class TextProcessorConfig(ModuleConfig):
    """Text processor configuration"""

    name: str
    max_length: int | None = None
    min_length: int | None = None
    strip_html: bool = False
    normalize_whitespace: bool = True
    chunk_size: int = 1000
    overlap: int = 0
    metadata: JsonDict = field(default_factory=dict)
