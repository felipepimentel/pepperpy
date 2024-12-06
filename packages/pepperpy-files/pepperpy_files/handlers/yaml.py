"""YAML file handler implementation"""

from pathlib import Path
from typing import Any

from ..base import BaseHandler, FileHandlerConfig
from ..enums import FileType
from ..exceptions import FileError
from ..types import FileContent, FileMetadata


class YAMLError(FileError):
    """YAML specific error"""

    def __init__(self, message: str, cause: Exception | None = None) -> None:
        super().__init__(message)
        self.cause = cause


# YAML module setup
try:
    import yaml
    from yaml.error import YAMLError as YAMLLibError

    yaml_available = True
    yaml_error: type[Exception] = YAMLLibError
except ImportError:
    yaml_available = False
    yaml_error = Exception


class YAMLHandler(BaseHandler):
    """YAML file handler implementation"""

    def __init__(self) -> None:
        """Initialize handler"""
        if not yaml_available:
            raise YAMLError(
                "YAML support requires additional dependencies. "
                "Please install with: pip install pyyaml"
            )

        super().__init__(
            config=FileHandlerConfig(
                allowed_extensions=self._convert_extensions([".yml", ".yaml"]),
                max_file_size=10 * 1024 * 1024,  # 10MB
                metadata={
                    "type": FileType.CONFIG,
                    "mime_type": "application/x-yaml",
                },
            )
        )
        self._initialized = True
        self._yaml = yaml

    def _to_path(self, file: str | Path) -> Path:
        """Convert to Path object.

        Args:
            file: Path-like object to convert

        Returns:
            Converted Path object
        """
        return Path(file) if isinstance(file, str) else file

    def _get_mime_type(self, path: Path) -> str:
        """Get MIME type for file"""
        return "application/x-yaml"

    def _get_file_type(self, path: Path) -> str:
        """Get file type"""
        return FileType.CONFIG

    def _get_format(self, path: Path) -> str:
        """Get file format"""
        return path.suffix.lstrip(".")

    def _validate_path(self, path: Path) -> None:
        """Validate file path"""
        if not path.exists():
            raise YAMLError(f"File not found: {path}")
        if not path.is_file():
            raise YAMLError(f"Not a file: {path}")
        if path.suffix not in self.config.allowed_extensions:
            raise YAMLError(f"Invalid file extension: {path.suffix}")

    def _validate_size(self, path: Path) -> None:
        """Validate file size"""
        size = path.stat().st_size
        if size > self.config.max_file_size:
            raise YAMLError(
                f"File size ({size} bytes) exceeds limit ({self.config.max_file_size} bytes)"
            )

    def _validate_content(self, content: Any) -> dict[str, Any]:
        """Validate and convert YAML content.

        Args:
            content: Content to validate

        Returns:
            Validated content as dictionary

        Raises:
            YAMLError: If content is invalid
        """
        if content is None:
            return {}
        if isinstance(content, dict):
            return content
        if isinstance(content, list):
            return {"items": content}
        raise YAMLError("Invalid YAML content: must be dictionary or list")

    async def read(self, file: str | Path) -> FileContent:
        """Read YAML file"""
        try:
            path = self._to_path(file)
            self._validate_path(path)
            self._validate_size(path)

            with open(path, encoding="utf-8") as f:
                content = self._yaml.safe_load(f)

            validated_content = self._validate_content(content)
            content_str = self._yaml.safe_dump(validated_content)
            if content_str is None:
                content_str = ""  # Fallback para string vazia se o dump retornar None

            file_metadata = FileMetadata(
                name=path.name,
                mime_type=self._get_mime_type(path),
                size=path.stat().st_size,
                format=self._get_format(path),
                additional_metadata=validated_content,
            )

            return FileContent(path=path, content=content_str, metadata=file_metadata)
        except yaml_error as e:
            raise YAMLError(f"Invalid YAML: {e}", cause=e)
        except Exception as e:
            raise YAMLError(f"Failed to read YAML file: {e}", cause=e)

    async def write(self, content: dict[str, Any], output: str | Path) -> None:
        """Write YAML file"""
        try:
            path = self._to_path(output)
            self._validate_path(path.parent)

            validated_content = self._validate_content(content)

            with open(path, "w", encoding="utf-8") as f:
                self._yaml.safe_dump(validated_content, f, default_flow_style=False)
        except yaml_error as e:
            raise YAMLError(f"Invalid YAML: {e}", cause=e)
        except Exception as e:
            raise YAMLError(f"Failed to write YAML file: {e}", cause=e)

    async def cleanup(self) -> None:
        """Cleanup resources"""
        pass
