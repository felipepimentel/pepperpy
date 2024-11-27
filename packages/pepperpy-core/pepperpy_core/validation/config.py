"""Validation configuration"""

from pydantic import BaseModel

from ..base.types import JsonDict


class ValidationConfig(BaseModel):
    """Validation pipeline configuration"""

    fail_fast: bool = False
    max_errors: int = 100
    metadata: JsonDict = {}
