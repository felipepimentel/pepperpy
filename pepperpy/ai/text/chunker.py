"""Text chunking implementation"""

from dataclasses import dataclass, field
from typing import Any

from pepperpy.core.module import BaseModule, ModuleMetadata


@dataclass
class ChunkerConfig:
    """Text chunker configuration"""

    chunk_size: int = 1000
    overlap: int = 200
    separator: str = "\n"
    min_chunk_size: int = 100
    max_chunk_size: int = 2000
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass
class TextChunker(BaseModule):
    """Text chunker implementation"""

    config: ChunkerConfig = field(default_factory=ChunkerConfig)
    metadata: ModuleMetadata = field(init=False)

    def __post_init__(self) -> None:
        """Post initialization"""
        self.metadata = ModuleMetadata(
            name="text_chunker",
            version="1.0.0",
            description="Text chunking module",
            config={"chunker": self.config},
        )

    # ... rest of implementation ...
