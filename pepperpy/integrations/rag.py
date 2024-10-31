"""Enhanced RAG implementations."""
from typing import List, Optional, Dict, Any, Protocol
from dataclasses import dataclass
import numpy as np
from ..data.vector_store import VectorStore, SearchResult
from ..data.types import Document
from ..llm.base import BaseLLM
from ..telemetry import metrics

# ... resto do código permanece igual ... 