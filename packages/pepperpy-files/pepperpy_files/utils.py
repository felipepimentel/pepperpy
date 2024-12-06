"""Utility functions."""

from pathlib import Path

PathLike = Path | str  # Usando union type


def ensure_path(path: PathLike) -> Path:
    """Ensure path is a Path object."""
    return Path(path) if not isinstance(path, Path) else path
