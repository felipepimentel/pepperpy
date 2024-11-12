"""Plugin type definitions"""

from dataclasses import dataclass
from typing import List, Type


@dataclass
class PluginMetadata:
    """Plugin metadata"""

    name: str
    version: str
    description: str
    dependencies: List[str]


@dataclass
class Plugin:
    """Plugin information"""

    metadata: PluginMetadata
    class_: Type
