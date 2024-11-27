"""Plugin core configuration"""

from pathlib import Path

from pydantic import BaseModel, ConfigDict, Field

from ...base.types import JsonDict


class PluginConfig(BaseModel):
    """Plugin configuration"""

    plugins_path: Path = Field(default=Path.cwd() / "plugins")
    enabled_plugins: list[str] = Field(default_factory=list)
    auto_discover: bool = Field(default=True)
    auto_load: bool = Field(default=True)
    reload_on_change: bool = Field(default=False)
    metadata: JsonDict = Field(default_factory=dict)
    model_config = ConfigDict(frozen=True)

    @classmethod
    def get_default(cls) -> "PluginConfig":
        """Get default configuration"""
        return cls(
            plugins_path=Path.cwd() / "plugins",
            enabled_plugins=[],
            auto_discover=True,
            auto_load=True,
            reload_on_change=False,
            metadata={},
        )
