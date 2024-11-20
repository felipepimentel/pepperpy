"""Configuration handler implementation"""

from ..exceptions import FileError
from ..types import FileContent, FileType, PathLike
from .base import BaseFileHandler, FileHandler


class ConfigHandler(BaseFileHandler, FileHandler[dict]):
    """Handler for configuration files"""

    async def read(self, file: PathLike) -> FileContent[dict]:
        """Read configuration file"""
        try:
            path = self._to_path(file)
            with open(path, "r", encoding="utf-8") as f:
                content = eval(f.read())  # Implementar parser seguro

            metadata = self._create_metadata(
                path=path,
                file_type=FileType.CONFIG,
                mime_type="application/x-python",
                format_str="py",
            )

            return FileContent(content=content, metadata=metadata)
        except Exception as e:
            raise FileError(f"Failed to read config file: {e}", cause=e)

    async def write(self, content: dict, output: PathLike) -> None:
        """Write configuration file"""
        try:
            path = self._to_path(output)
            with open(path, "w", encoding="utf-8") as f:
                f.write(repr(content))
        except Exception as e:
            raise FileError(f"Failed to write config file: {e}", cause=e)

    async def cleanup(self) -> None:
        """Cleanup resources"""
        pass
