"""File manager configuration"""

from pathlib import Path

from pydantic import BaseModel, Field

from pepperpy.core.types import JsonDict


class FileManagerConfig(BaseModel):
    """File manager configuration"""

    base_path: Path = Field(default=Path.cwd())
    temp_path: Path = Field(default=Path.cwd() / "temp")
    max_file_size: int = Field(default=10 * 1024 * 1024)  # 10MB
    allowed_extensions: set[str] = Field(default_factory=lambda: {"txt", "pdf", "md"})
    metadata: JsonDict = Field(default_factory=dict)

    class Config:
        """Pydantic config"""
        frozen = True
