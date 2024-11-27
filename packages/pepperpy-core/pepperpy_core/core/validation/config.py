"""Validation configuration"""

from pydantic import BaseModel, ConfigDict, Field

from ...base.types import JsonDict


class ValidationConfig(BaseModel):
    """Validation configuration"""

    fail_fast: bool = Field(default=False)
    max_errors: int = Field(default=100)
    ignore_none: bool = Field(default=True)
    metadata: JsonDict = Field(default_factory=dict)
    model_config = ConfigDict(frozen=True)
