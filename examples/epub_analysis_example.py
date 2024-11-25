"""EPUB analysis example"""

import asyncio
from pathlib import Path
from typing import Any

from pepperpy.console import Console
from pepperpy.files import FileMetadata
from pepperpy.files.handlers.epub import EPUBHandler
from pepperpy.files.manager import FileManager

console = Console()


async def analyze_epub_content(epub_path: str | Path) -> None:
    """Analyze EPUB content"""
    file_manager = None
    try:
        console.info("📚 Analyzing EPUB content...")

        # Initialize handlers
        epub_handler = EPUBHandler()
        file_manager = FileManager()
        await file_manager.initialize()
        file_manager.register_handler(".epub", epub_handler)

        # Convert to Path if string
        path = Path(epub_path) if isinstance(epub_path, str) else epub_path

        # Read EPUB file
        file_content = await file_manager.read_file(path)

        # Garantir que o tipo está correto
        metadata: FileMetadata = file_content.metadata
        content: Any = file_content.content  # Usando Any temporariamente até definir o tipo correto

        # Basic analysis
        console.info(
            "Book Information:",
            content=(
                f"Title: {metadata.metadata.get('title', 'Unknown')}\n"
                f"Authors: {metadata.metadata.get('authors', [])}\n"
                f"Language: {metadata.metadata.get('language', 'Unknown')}\n"
                f"Chapters: {len(content.chapters)}\n"
                f"Total Images: {len(content.images)}"
            ),
        )

        # Analyze chapters
        total_words = 0
        total_chars = 0

        for chapter in content.chapters:
            # Simple analysis
            words = len(chapter.content.split())
            chars = len(chapter.content)
            total_words += words
            total_chars += chars

            console.info(
                f"Chapter: {chapter.title}",
                content=(f"Words: {words}\n" f"Characters: {chars}"),
            )

        # Summary
        console.success(
            "Analysis Complete",
            content=(
                f"Total Words: {total_words}\n"
                f"Total Characters: {total_chars}\n"
                f"Average Words per Chapter: {total_words // len(content.chapters)}"
            ),
        )

    except Exception as e:
        console.error("Analysis failed", str(e))
    finally:
        if file_manager:
            await file_manager.cleanup()


async def main() -> None:
    """Run EPUB analysis example"""
    try:
        epub_path = Path("examples/data/sample.epub")
        await analyze_epub_content(epub_path)
    except Exception as e:
        console.error("Example failed", str(e))


if __name__ == "__main__":
    asyncio.run(main())
