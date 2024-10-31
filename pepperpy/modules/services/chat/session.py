"""Chat session management."""
from typing import List, Optional, Dict, Any
from dataclasses import dataclass
from datetime import datetime

from ....modules.llm import BaseLLM, Message
from .memory import ChatMemory

# ... resto do código ... 