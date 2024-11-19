"""Example of EPUB document analysis"""

import asyncio
import os
from pathlib import Path

from pepperpy.ai.text import TextAnalyzer
from pepperpy.ai.text.types import AnalysisConfig
from pepperpy.console import Console
from pepperpy.files import file_manager
from pepperpy.files.handlers.epub import EPUBHandler

console = Console()


async def analyze_epub(file_path: str | Path) -> None:
    """Analyze EPUB document"""
    try:
        # Criar configuração de análise
        config = AnalysisConfig(
            name="epub_analysis",
            version="1.0.0",
            model="en_core_web_sm",
            min_concept_frequency=2,
            context_window=100,
            min_phrase_length=3,
            top_phrases=50,
        )

        # Registrar handler EPUB
        file_manager.register_handler("epub", EPUBHandler())

        # Criar analisador
        analyzer = TextAnalyzer(config=config)
        await analyzer.initialize()

        try:
            # Carregar e processar EPUB
            book = await file_manager.read_file(file_path)
            
            # Extrair texto
            text = "\n\n".join(chapter.content for chapter in book.chapters)

            # Analisar texto
            analysis = await analyzer.analyze(text)

            # Exibir resultados
            console.info("📚 Analysis Results:")
            console.info(f"Tokens: {len(analysis.tokens)}")
            console.info(f"Sentences: {len(analysis.sentences)}")
            console.info(f"Key Phrases: {len(analysis.key_phrases)}")
            console.info(f"Concepts: {len(analysis.concepts)}")

            # Exibir frases-chave
            console.info("\n🔑 Key Phrases:")
            for phrase in analysis.key_phrases[:5]:
                console.info(f"- {phrase.text} (score: {phrase.score:.2f})")

            # Exibir conceitos
            console.info("\n💡 Main Concepts:")
            for concept in analysis.concepts[:5]:
                console.info(f"- {concept.term} ({concept.type})")
                console.info(f"  Context: {concept.context}")

        finally:
            await analyzer.cleanup()

    except Exception as e:
        console.error(f"Analysis failed: {e}")


if __name__ == "__main__":
    # Obter caminho do arquivo de exemplo
    example_file = os.path.join(
        os.path.dirname(__file__),
        "data",
        "example.epub",
    )

    # Executar análise
    asyncio.run(analyze_epub(example_file))
