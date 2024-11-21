"""Text processor configuration"""

from pydantic import BaseModel, Field

from pepperpy.core.types import JsonDict


class TextProcessorConfig(BaseModel):
    """Text processor configuration"""

    chunk_size: int = Field(default=1000, gt=0)
    overlap: int = Field(default=200, ge=0)
    encoding: str = Field(default="utf-8")
    strip_html: bool = Field(default=True)
    normalize_whitespace: bool = Field(default=True)
    max_length: int = Field(default=100000, gt=0)
    min_length: int = Field(default=10, ge=0)
    metadata: JsonDict = Field(default_factory=dict)

    class Config:
        """Pydantic config"""
        frozen = True

    @classmethod
    def get_default(cls) -> "TextProcessorConfig":
        """Get default configuration"""
        return cls(
            chunk_size=1000,
            overlap=200,
            encoding="utf-8",
            strip_html=True,
            normalize_whitespace=True,
            max_length=100000,
            min_length=10,
        )
