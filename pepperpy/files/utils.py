"""File utilities"""

from pathlib import Path
from typing import Union

PathLike = Union[str, Path]

def ensure_path(path: PathLike) -> Path:
    """Ensure path is a Path object."""
    return Path(path) if not isinstance(path, Path) else path
