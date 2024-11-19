"""Pipeline input validation"""

from pathlib import Path
from typing import Protocol

from pepperpy.core.exceptions import PepperPyError


class ValidationError(PepperPyError):
    """Error during input validation"""


class InputValidator(Protocol):
    """Protocol for input validators"""

    async def validate(self, input_path: Path) -> None:
        """Validate input file"""
        ...


class EPUBValidator:
    """Validator for EPUB files"""

    async def validate(self, input_path: Path) -> None:
        """Validate EPUB file"""
        if not input_path.exists():
            raise ValidationError(f"File not found: {input_path}")
        if input_path.suffix.lower() != ".epub":
            raise ValidationError(f"Invalid file type: {input_path.suffix}")
        if input_path.stat().st_size == 0:
            raise ValidationError(f"Empty file: {input_path}")


VALIDATORS = {
    "epub": EPUBValidator(),
    # Adicionar mais validadores aqui
} 