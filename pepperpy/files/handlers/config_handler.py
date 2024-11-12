"""Configuration file handler implementation"""

import json
from configparser import ConfigParser
from pathlib import Path
from typing import Any, Dict, Optional, Sequence

import tomli
import tomli_w
import yaml

from ..base import FileHandler
from ..exceptions import FileError


class ConfigHandler(FileHandler):
    """Handler for configuration files"""

    SUPPORTED_FORMATS = {
        ".toml": ("tomli", "tomli_w"),
        ".yaml": ("yaml", "yaml"),
        ".yml": ("yaml", "yaml"),
        ".json": ("json", "json"),
        ".ini": ("ini", "ini"),
    }

    async def read(self, path: Path) -> Dict[str, Any]:
        """Read configuration file"""
        try:
            format_type = path.suffix.lower()
            if format_type not in self.SUPPORTED_FORMATS:
                raise FileError(f"Unsupported config format: {format_type}")

            with open(path, "r", encoding="utf-8") as f:
                if format_type in (".yaml", ".yml"):
                    return yaml.safe_load(f)
                elif format_type == ".toml":
                    return tomli.load(f)
                elif format_type == ".json":
                    return json.load(f)
                elif format_type == ".ini":
                    config = ConfigParser()
                    config.read_file(f)
                    return {section: dict(config.items(section)) for section in config.sections()}

        except Exception as e:
            raise FileError(f"Failed to read config: {str(e)}", cause=e)

    async def write(self, path: Path, content: Dict[str, Any], **kwargs: Any) -> None:
        """Write configuration file"""
        try:
            format_type = path.suffix.lower()
            if format_type not in self.SUPPORTED_FORMATS:
                raise FileError(f"Unsupported config format: {format_type}")

            with open(path, "w", encoding="utf-8") as f:
                if format_type in (".yaml", ".yml"):
                    yaml.safe_dump(content, f, **kwargs)
                elif format_type == ".toml":
                    tomli_w.dump(content, f)
                elif format_type == ".json":
                    json.dump(content, f, indent=2, **kwargs)
                elif format_type == ".ini":
                    config = ConfigParser()
                    for section, values in content.items():
                        config[section] = values
                    config.write(f)

        except Exception as e:
            raise FileError(f"Failed to write config: {str(e)}", cause=e)

    async def merge(
        self, paths: Sequence[Path], output_path: Path, strategy: str = "update"
    ) -> None:
        """Merge multiple configuration files"""
        try:
            result = {}

            for path in paths:
                config = await self.read(path)
                if strategy == "update":
                    result.update(config)
                elif strategy == "deep":
                    result = self._deep_merge(result, config)
                else:
                    raise FileError(f"Invalid merge strategy: {strategy}")

            await self.write(output_path, result)

        except Exception as e:
            raise FileError(f"Failed to merge configs: {str(e)}", cause=e)

    async def validate(self, path: Path, schema: Optional[Dict[str, Any]] = None) -> bool:
        """Validate configuration file"""
        try:
            config = await self.read(path)

            if schema:
                from jsonschema import validate

                validate(instance=config, schema=schema)

            return True

        except Exception as e:
            raise FileError(f"Config validation failed: {str(e)}", cause=e)

    def _deep_merge(self, dict1: Dict[str, Any], dict2: Dict[str, Any]) -> Dict[str, Any]:
        """Deep merge two dictionaries"""
        result = dict1.copy()

        for key, value in dict2.items():
            if key in result and isinstance(result[key], dict) and isinstance(value, dict):
                result[key] = self._deep_merge(result[key], value)
            else:
                result[key] = value

        return result
