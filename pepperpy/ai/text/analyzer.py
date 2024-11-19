"""Text analysis implementation"""

from collections import Counter
from dataclasses import asdict
from typing import Optional

from pepperpy.core.module import BaseModule, ModuleMetadata

from .exceptions import AnalysisError
from .types import AnalysisConfig, AnalysisResult, TextMetadata


class TextAnalyzer(BaseModule):
    """Text analysis implementation"""

    def __init__(self, config: Optional[AnalysisConfig] = None) -> None:
        super().__init__()
        self._config: AnalysisConfig = config or AnalysisConfig()
        self.metadata = ModuleMetadata(
            name="text_analyzer",
            version="1.0.0",
            description="Text analysis utilities",
            dependencies=[],
            config=asdict(self._config),
        )
        self._nlp = None

    @property
    def config(self) -> AnalysisConfig:
        """Get analyzer configuration"""
        return self._config

    @config.setter
    def config(self, value: AnalysisConfig) -> None:
        """Set analyzer configuration"""
        self._config = value
        if self.metadata is not None:
            self.metadata.config = asdict(value)

    async def analyze(self, text: str) -> AnalysisResult:
        """Analyze text content"""
        try:
            if not text:
                return AnalysisResult(
                    text="",
                    summary="",
                    keywords=[],
                    concepts=[],
                    phrases=[],
                    metadata=TextMetadata(),
                )

            # Extrair métricas básicas
            words = text.split()
            sentences = text.split(".")
            paragraphs = text.split("\n\n")

            # Criar metadata
            metadata = TextMetadata(
                language=await self._detect_language(text),
                tokens=len(words),
                sentences=len(sentences),
                paragraphs=len(paragraphs),
            )

            # Criar resultado
            result = AnalysisResult(
                text=text,
                metadata=metadata,
            )

            # Adicionar análises configuradas
            if self.config.extract_keywords:
                result.keywords = await self._extract_keywords(text)

            if self.config.extract_entities:
                result.entities = await self._extract_entities(text)

            if self.config.extract_summary:
                result.summary = await self._generate_summary(text)

            return result

        except Exception as e:
            raise AnalysisError(f"Text analysis failed: {e!s}", cause=e)

    async def _detect_language(self, text: str) -> str:
        """Detect text language"""
        try:
            # Implementação básica - pode ser melhorada com biblioteca específica
            import langdetect

            return langdetect.detect(text)
        except Exception:
            return "unknown"

    async def _extract_keywords(self, text: str) -> list[str]:
        """Extract keywords from text"""
        try:
            # Implementação básica usando frequência
            words = text.lower().split()
            word_freq = Counter(words)
            return [
                word
                for word, freq in word_freq.most_common(self.config.max_keywords)
                if freq >= self.config.min_keyword_freq
            ]
        except Exception as e:
            raise AnalysisError(f"Keyword extraction failed: {str(e)}", cause=e)

    async def _extract_entities(self, text: str) -> dict[str, list[str]]:
        """Extract named entities from text"""
        try:
            # Implementação básica - pode ser melhorada com spaCy ou similar
            return {
                "locations": [],
                "persons": [],
                "organizations": [],
                "dates": [],
            }
        except Exception as e:
            raise AnalysisError(f"Entity extraction failed: {str(e)}", cause=e)

    async def _generate_summary(self, text: str) -> str:
        """Generate text summary"""
        try:
            # Implementação básica - extrair primeiras sentenças
            sentences = text.split(".")
            summary_size = int(len(sentences) * self.config.summary_ratio)
            return ". ".join(sentences[:summary_size]) + "."
        except Exception as e:
            raise AnalysisError(f"Summary generation failed: {e!s}", cause=e)

    async def _setup(self) -> None:
        """Initialize analyzer resources"""
        try:
            import spacy

            self._nlp = spacy.load(self.config.model)
        except Exception as e:
            raise AnalysisError(f"Failed to initialize analyzer: {e!s}", cause=e)

    async def _cleanup(self) -> None:
        """Cleanup analyzer resources"""
        self._nlp = None


# Global analyzer instance
analyzer = TextAnalyzer()
