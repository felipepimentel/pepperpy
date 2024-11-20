"""Hybrid code analysis provider"""

from pepperpy.ai.client import AIClient
from pepperpy.core.module import BaseModule

from ..config import CodebaseConfig
from .static import StaticAnalysisProvider


class HybridProvider(BaseModule[CodebaseConfig]):
    """Hybrid analysis provider"""

    def __init__(self, config: CodebaseConfig, ai_client: AIClient) -> None:
        super().__init__(config)
        self._ai_client = ai_client
        self._static_provider = StaticAnalysisProvider(config)
