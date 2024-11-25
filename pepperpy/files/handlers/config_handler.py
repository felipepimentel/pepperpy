"""Configuration handler implementation"""

from pathlib import Path

from ..exceptions import FileError
from ..types import FileContent, FileType, PathLike
from .base import BaseFileHandler


class ConfigHandler(BaseFileHandler[dict]):
    """Handler for configuration files"""

    def _to_path(self, file: PathLike) -> Path:
        """Convert PathLike to Path"""
        return Path(file) if isinstance(file, str) else file

    def _get_mime_type(self, path: Path) -> str:
        """Get MIME type for file"""
        return "application/x-python"

    def _get_file_type(self, path: Path) -> str:
        """Get file type"""
        return FileType.CONFIG

    def _get_format(self, path: Path) -> str:
        """Get file format"""
        return "py"

    async def read(self, file: PathLike) -> FileContent[dict]:
        """Read configuration file"""
        try:
            path = self._to_path(file)
            with open(path, "r", encoding="utf-8") as f:
                content = eval(f.read())  # Implementar parser seguro

            metadata = self._create_metadata(
                path=path,
                size=len(str(content))  # Usando str() para obter um tamanho aproximado
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
