"""EPUB handling examples demonstrating advanced file operations and content analysis"""

import asyncio
from pathlib import Path

from pepperpy.console import Console
from pepperpy.files.handlers import EPUBHandler

console = Console()


async def demonstrate_epub_features(epub_path: Path) -> None:
    """Demonstrate EPUB handler features"""
    try:
        console.info(f"📚 Processing EPUB: {epub_path}")

        handler = EPUBHandler()
        content = await handler.read(epub_path)
        book = content.content

        # Analyze structure
        structure = await handler.analyze_structure(book)
        console.info(f"Found {len(structure.chapters)} chapters and {len(structure.assets)} assets")

        # Extract resources
        output_dir = Path("epub_output")
        await handler.extract_resources(book, output_dir)
        console.success(f"✨ Resources extracted to: {output_dir}")

        # Search content
        results = await handler.search_content(book, "Python")
        console.info(f"🔍 Found {len(results)} matches for 'Python'")
        for result in results:
            console.print(f"  📄 {result['chapter']} ({result['type']})")
            console.print(f"     {result['context']}\n")

    except Exception as e:
        console.error(f"❌ Error processing EPUB: {e!s}")


if __name__ == "__main__":
    try:
        epub_path = Path("modern_python_guide.epub")
        if epub_path.exists():
            asyncio.run(demonstrate_epub_features(epub_path))
        else:
            console.error(f"❌ EPUB file not found: {epub_path}")

    except KeyboardInterrupt:
        console.info("\n👋 Processing finished!")
