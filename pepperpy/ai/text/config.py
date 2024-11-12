"""Text processing configuration"""

from dataclasses import dataclass

from pepperpy.core.config import ModuleConfig


@dataclass
class TextConfig(ModuleConfig):
    """Configuration for text processing"""

    max_chunk_size: int = 1000
    overlap: int = 100
    respect_sentences: bool = True
    respect_paragraphs: bool = True
    use_tokenizer: bool = False
    tokenizer_model: str = "gpt2"
    min_chunk_size: int = 100
    preserve_whitespace: bool = False
