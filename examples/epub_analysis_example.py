"""EPUB analysis example"""

import asyncio
from pathlib import Path

from pepperpy.console import Console
from pepperpy.files.handlers.epub import EPUBHandler
from pepperpy.files.manager import FileManager

console = Console()


async def analyze_epub_content(file_path: Path) -> None:
    """Analyze EPUB content"""
    file_manager = None
    try:
        await console.info("📚 Analyzing EPUB content...")

        # Initialize handlers
        epub_handler = EPUBHandler()
        file_manager = FileManager()
        await file_manager.initialize()

        # Register EPUB handler
        file_manager.register_handler(".epub", epub_handler)

        # Read EPUB content
        content = await file_manager.read_file(file_path)
        book = content.content

        # Basic analysis
        await console.info(
            "Book Information:",
            content=(
                f"Title: {book.metadata.title}\n"
                f"Authors: {', '.join(book.metadata.authors)}\n"
                f"Language: {book.metadata.language}\n"
                f"Chapters: {len(book.chapters)}\n"
                f"Total Images: {len(book.images)}"
            ),
        )

        # Analyze chapters
        total_words = 0
        total_chars = 0

        for chapter in book.chapters:
            words = len(chapter.content.split())
            chars = len(chapter.content)
            total_words += words
            total_chars += chars

            await console.info(
                f"Chapter: {chapter.title}",
                content=(f"Words: {words:,}\n" f"Characters: {chars:,}"),
            )

        # Summary
        await console.success(
            "Analysis Complete",
            content=(
                f"Total Words: {total_words:,}\n"
                f"Total Characters: {total_chars:,}\n"
                f"Average Words per Chapter: {total_words // len(book.chapters):,}"
            ),
        )

    except Exception as e:
        await console.error("Analysis failed", str(e))
    finally:
        if file_manager:
            await file_manager.cleanup()


async def main() -> None:
    """Run EPUB analysis example"""
    try:
        epub_path = Path("examples/data/sample.epub")
        await analyze_epub_content(epub_path)
    except Exception as e:
        await console.error("Example failed", str(e))


if __name__ == "__main__":
    asyncio.run(main())
