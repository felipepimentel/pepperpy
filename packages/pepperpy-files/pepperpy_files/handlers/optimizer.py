"""Image optimizer handler implementation."""

from typing import Any, Optional

try:
    import PIL

    optimizer_available = True
except ImportError:
    optimizer_available = False

# Definir o módulo como opcional
optimizer_module: Optional[Any] = PIL if optimizer_available else None
