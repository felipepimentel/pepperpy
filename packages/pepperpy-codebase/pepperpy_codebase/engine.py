"""Code analysis engine"""

from typing import Any

from bko.ai.client import AIClient
from bko.core.module import BaseModule

from .config import CodebaseConfig
from .indexer import CodeIndexer


class CodebaseEngine(BaseModule[CodebaseConfig]):
    """Code analysis engine"""

    def __init__(
        self, config: CodebaseConfig, ai_client: AIClient | None = None, **kwargs: Any
    ) -> None:
        super().__init__(config)
        self._ai_client = ai_client
        self._indexer = CodeIndexer(config)
        self._provider = None
