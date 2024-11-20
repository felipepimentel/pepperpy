"""YAML file handler implementation"""

import yaml

from ..exceptions import FileError
from ..types import FileContent, FileType, PathLike
from .base import BaseFileHandler, FileHandler


class YAMLHandler(BaseFileHandler, FileHandler[dict]):
    """Handler for YAML files"""

    async def read(self, file: PathLike) -> FileContent[dict]:
        """Read YAML file"""
        try:
            path = self._to_path(file)
            with open(path, "r", encoding="utf-8") as f:
                content = yaml.safe_load(f)

            metadata = self._create_metadata(
                path=path,
                file_type=FileType.DATA,
                mime_type="application/yaml",
                format_str="yaml",
            )

            return FileContent(content=content, metadata=metadata)
        except Exception as e:
            raise FileError(f"Failed to read YAML file: {e}", cause=e)

    async def write(self, content: dict, output: PathLike) -> None:
        """Write YAML file"""
        try:
            path = self._to_path(output)
            with open(path, "w", encoding="utf-8") as f:
                yaml.safe_dump(content, f)
        except Exception as e:
            raise FileError(f"Failed to write YAML file: {e}", cause=e)

    async def cleanup(self) -> None:
        """Cleanup resources"""
        pass
