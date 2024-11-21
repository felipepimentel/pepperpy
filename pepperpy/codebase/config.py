"""Codebase configuration"""

from pathlib import Path

from pydantic import BaseModel, Field

from pepperpy.core.types import JsonDict


class CodebaseConfig(BaseModel):
    """Codebase configuration"""

    root_path: Path = Field(default=Path.cwd())
    ignore_patterns: list[str] = Field(default_factory=lambda: [".*", "__pycache__", "*.pyc"])
    max_file_size: int = Field(default=10 * 1024 * 1024)  # 10MB
    index_path: Path = Field(default=Path.cwd() / ".index")
    encoding: str = Field(default="utf-8")
    metadata: JsonDict = Field(default_factory=dict)

    class Config:
        """Pydantic config"""
        frozen = True

    @classmethod
    def get_default(cls) -> "CodebaseConfig":
        """Get default configuration"""
        return cls(
            root_path=Path.cwd(),
            ignore_patterns=[".*", "__pycache__", "*.pyc"],
            max_file_size=10 * 1024 * 1024,
            index_path=Path.cwd() / ".index",
            encoding="utf-8",
        )
