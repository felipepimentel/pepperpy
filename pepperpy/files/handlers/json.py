"""JSON file handler implementation"""

import json
from pathlib import Path
from typing import Any, Dict, Optional

from ..exceptions import FileError
from ..types import FileContent, FileMetadata
from .base import BaseHandler


class JSONHandler(BaseHandler):
    """Handler for JSON files"""

    async def read(self, path: Path) -> FileContent:
        """Read JSON file"""
        try:
            metadata = await self._get_metadata(path)
            content = await self._read_file(path)

            # Parse JSON content
            data = json.loads(content)

            return FileContent(content=data, metadata=metadata, format="json")
        except Exception as e:
            raise FileError(f"Failed to read JSON file: {str(e)}", cause=e)

    async def write(
        self, path: Path, content: Dict[str, Any], metadata: Optional[Dict[str, Any]] = None
    ) -> FileMetadata:
        """Write JSON file"""
        try:
            # Convert to JSON
            json_content = json.dumps(content, indent=2, ensure_ascii=False)

            return await self._write_file(path, json_content)
        except Exception as e:
            raise FileError(f"Failed to write JSON file: {str(e)}", cause=e)
