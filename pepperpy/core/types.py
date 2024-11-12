"""Core type definitions"""

from typing import Any, Dict, Union

# Type alias for JSON-serializable dictionary
JsonDict = Dict[str, Any]

# Type alias for primitive JSON values
JsonValue = Union[str, int, float, bool, None, Dict[str, Any], list]
