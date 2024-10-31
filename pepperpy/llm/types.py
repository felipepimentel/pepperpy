"""Type definitions and common structures for LLM module."""
from typing import TypedDict, Literal, Union, Dict, List, Optional, Protocol, Any
from dataclasses import dataclass, field

Role = Literal["system", "user", "assistant"] 