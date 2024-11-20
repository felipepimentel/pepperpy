"""EPUB handling examples"""

import asyncio
from pathlib import Path

from pepperpy.console import Console
from pepperpy.files.handlers.epub import EPUBHandler

console = Console()


async def demonstrate_epub_handling() -> None:
    """Demonstrate EPUB handling capabilities"""
    try:
        await console.info("📚 Initializing EPUB Handler...")

        # Create handler
        handler = EPUBHandler()

        # Example EPUB file
        epub_path = Path("examples/data/sample.epub")
        output_path = Path("examples/output/processed.epub")

        # Read EPUB
        await console.info(f"Reading EPUB from {epub_path}")
        content = await handler.read(epub_path)

        # Process content
        book = content.content
        await console.info(
            "Book Information:",
            content=(
                f"Title: {book.metadata.title}\n"
                f"Authors: {', '.join(book.metadata.authors)}\n"
                f"Chapters: {len(book.chapters)}\n"
                f"Images: {len(book.images)}\n"
                f"Styles: {len(book.styles)}"
            )
        )

        # Process chapters
        for chapter in book.chapters:
            await console.info(
                f"Chapter: {chapter.title}",
                content=f"Length: {len(chapter.content)} characters"
            )

        # Write processed EPUB
        await console.info(f"Writing processed EPUB to {output_path}")
        await handler.write(book, output_path)

        await console.success("EPUB processing completed!")

    except Exception as e:
        await console.error("EPUB handling failed", str(e))


async def demonstrate_epub_search() -> None:
    """Demonstrate EPUB search capabilities"""
    try:
        await console.info("🔍 Initializing EPUB Search...")

        handler = EPUBHandler()
        epub_path = Path("examples/data/sample.epub")

        # Read EPUB
        content = await handler.read(epub_path)
        book = content.content

        # Search in content
        search_term = "Python"
        await console.info(f"Searching for '{search_term}'...")

        results = []
        for chapter in book.chapters:
            if search_term.lower() in chapter.content.lower():
                results.append(f"Found in chapter: {chapter.title}")

        if results:
            await console.success(
                "Search Results",
                content="\n".join(results)
            )
        else:
            await console.info(f"No matches found for '{search_term}'")

    except Exception as e:
        await console.error("EPUB search failed", str(e))


if __name__ == "__main__":
    try:
        asyncio.run(demonstrate_epub_handling())
        asyncio.run(demonstrate_epub_search())
    except KeyboardInterrupt:
        print("\n\n⚠️ Examples interrupted by user")
    except Exception as e:
        print(f"\n❌ Fatal error: {e}")
