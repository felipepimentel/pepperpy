"""Configuration file handler implementation"""

import configparser
from pathlib import Path
from typing import Any, Dict, Optional

from ..exceptions import FileError
from ..types import FileContent, FileMetadata
from .base import BaseHandler


class ConfigHandler(BaseHandler):
    """Handler for INI/Config files"""

    async def read(self, path: Path) -> FileContent:
        """Read config file"""
        try:
            metadata = await self._get_metadata(path)

            # Parse config content
            config = configparser.ConfigParser()
            config.read(path)

            # Convert to dictionary
            data = {section: dict(config[section]) for section in config.sections()}

            return FileContent(content=data, metadata=metadata, format="config")
        except Exception as e:
            raise FileError(f"Failed to read config file: {str(e)}", cause=e)

    async def write(
        self,
        path: Path,
        content: Dict[str, Dict[str, Any]],
        metadata: Optional[Dict[str, Any]] = None,
    ) -> FileMetadata:
        """Write config file"""
        try:
            config = configparser.ConfigParser()

            # Add sections and values
            for section, values in content.items():
                config[section] = values

            # Write to file
            with open(path, "w") as file:
                config.write(file)

            return await self._get_metadata(path)
        except Exception as e:
            raise FileError(f"Failed to write config file: {str(e)}", cause=e)
