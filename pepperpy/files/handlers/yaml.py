"""YAML file handler implementation"""

from pathlib import Path
from typing import Any, Union

import yaml

from ..exceptions import FileError
from ..types import FileContent, FileType, PathLike
from .base import BaseFileHandler, FileHandlerConfig


class YAMLFileHandler(BaseFileHandler[Union[dict, list]]):
    """Handler for YAML files"""

    def __init__(self) -> None:
        """Initialize handler"""
        super().__init__(
            config=FileHandlerConfig(
                base_path=Path("."),
                allowed_extensions={".yml", ".yaml"},
                max_file_size=10 * 1024 * 1024,  # 10MB
                metadata={
                    "type": FileType.CONFIG,
                    "mime_type": "application/yaml",
                },
            )
        )
        self._initialized = True

    def _to_path(self, file: PathLike) -> Path:
        """Convert PathLike to Path"""
        return Path(file) if isinstance(file, str) else file

    def _get_mime_type(self, path: Path) -> str:
        """Get MIME type for file"""
        return "application/yaml"

    def _get_file_type(self, path: Path) -> str:
        """Get file type"""
        return FileType.CONFIG

    def _get_format(self, path: Path) -> str:
        """Get file format"""
        return path.suffix[1:]

    def _validate_path(self, path: Path) -> None:
        """Validate file path"""
        if not path.exists():
            raise FileError(f"File not found: {path}")
        if not path.is_file():
            raise FileError(f"Not a file: {path}")
        if path.suffix not in self.config.allowed_extensions:
            raise FileError(f"Invalid file extension: {path.suffix}")

    def _validate_size(self, path: Path) -> None:
        """Validate file size"""
        size = path.stat().st_size
        if size > self.config.max_file_size:
            raise FileError(
                f"File size ({size} bytes) exceeds limit ({self.config.max_file_size} bytes)"
            )

    def _validate_yaml_content(self, content: Any) -> None:
        """Validate YAML content"""
        if not isinstance(content, (dict, list)):
            raise FileError("Invalid YAML content: must be dictionary or list")
        try:
            yaml.safe_dump(content)
        except yaml.YAMLError:
            raise FileError("Failed to write file: Invalid YAML format")

    async def read(self, file: PathLike) -> FileContent[Union[dict, list]]:
        """Read YAML file"""
        try:
            path = self._to_path(file)
            self._validate_path(path)
            self._validate_size(path)

            with open(path, "r", encoding="utf-8") as f:
                content = yaml.safe_load(f)

            if content is None:
                content = {}  # Empty YAML file

            metadata = self._create_metadata(path=path, size=path.stat().st_size)

            return FileContent(content=content, metadata=metadata)
        except yaml.YAMLError as e:
            raise FileError("Invalid YAML format") from e
        except Exception as e:
            raise FileError(f"Failed to read YAML file: {e}", cause=e)

    async def write(self, content: Union[dict, list], output: PathLike) -> None:
        """Write YAML file"""
        try:
            path = self._to_path(output)
            self._validate_path(path.parent)
            self._validate_yaml_content(content)

            with open(path, "w", encoding="utf-8") as f:
                yaml.safe_dump(content, f, default_flow_style=False)
        except Exception as e:
            raise FileError(f"Failed to write YAML file: {e}", cause=e)

    async def cleanup(self) -> None:
        """Cleanup resources"""
        pass
