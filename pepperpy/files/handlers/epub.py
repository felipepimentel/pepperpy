"""EPUB file handler implementation"""

from datetime import datetime
from pathlib import Path
from typing import Any, cast

from bs4 import BeautifulSoup
from ebooklib import ITEM_DOCUMENT, ITEM_IMAGE, ITEM_STYLE, epub
from ebooklib.epub import EpubBook, EpubHtml, EpubItem

from ..exceptions import FileError
from ..types import Book, BookMetadata, Chapter, FileContent, FileType, PathLike
from .base import BaseFileHandler, FileHandler


class EPUBHandler(BaseFileHandler, FileHandler[Book]):
    """Handler for EPUB files"""

    def __init__(self) -> None:
        """Initialize handler"""
        super().__init__()

    async def cleanup(self) -> None:
        """Cleanup resources"""
        # No cleanup needed for EPUB handler
        pass

    async def read(self, file: PathLike) -> FileContent[Book]:
        """Read EPUB file"""
        try:
            path = self._to_path(file)
            book = epub.read_epub(str(path))
            return await self._process_book(book, path)
        except Exception as e:
            raise FileError(f"Failed to read EPUB file: {e!s}", cause=e)

    async def write(self, content: Book, output: PathLike) -> None:
        """Write EPUB file"""
        try:
            book = await self._create_epub(content)
            epub.write_epub(
                str(output) if isinstance(output, Path) else output,
                book,
                {"epub3_pages": True},
            )
        except Exception as e:
            raise FileError(f"Failed to write EPUB file: {e!s}", cause=e)

    async def _process_book(self, epub_book: EpubBook, source_path: Path) -> FileContent[Book]:
        """Process EPUB book"""
        try:
            # Extrair metadados
            book_metadata = BookMetadata(
                title=epub_book.get_metadata("DC", "title")[0][0],
                authors=[author[0] for author in epub_book.get_metadata("DC", "creator")],
                language=epub_book.get_metadata("DC", "language")[0][0],
                identifier=epub_book.get_metadata("DC", "identifier")[0][0],
                publisher=epub_book.get_metadata("DC", "publisher")[0][0]
                if epub_book.get_metadata("DC", "publisher")
                else None,
                publication_date=datetime.fromisoformat(
                    epub_book.get_metadata("DC", "date")[0][0]
                )
                if epub_book.get_metadata("DC", "date")
                else None,
                description=epub_book.get_metadata("DC", "description")[0][0]
                if epub_book.get_metadata("DC", "description")
                else None,
                subjects=[
                    subject[0]
                    for subject in epub_book.get_metadata("DC", "subject")
                ],
                rights=epub_book.get_metadata("DC", "rights")[0][0]
                if epub_book.get_metadata("DC", "rights")
                else None,
            )

            # Processar capítulos
            chapters: list[Chapter] = []
            for item in epub_book.get_items_of_type(ITEM_DOCUMENT):
                if isinstance(item, EpubHtml):
                    soup = BeautifulSoup(item.content, "html.parser")
                    chapter = Chapter(
                        title=item.title or "",
                        content=str(soup),
                        file_name=item.file_name,
                        order=len(chapters),
                        level=0,
                    )
                    chapters.append(chapter)

            # Criar livro
            book = Book(
                metadata=book_metadata,
                chapters=sorted(chapters, key=lambda x: x.order),
                cover_image=None,  # Implementar extração de capa
                styles={
                    item.file_name: item.content.decode("utf-8")
                    for item in epub_book.get_items_of_type(ITEM_STYLE)
                },
                images={
                    item.file_name: item.content
                    for item in epub_book.get_items_of_type(ITEM_IMAGE)
                },
                toc=epub_book.toc,
            )

            # Criar metadados do arquivo
            metadata = self._create_metadata(
                path=source_path,
                file_type=FileType.DOCUMENT,
                mime_type="application/epub+zip",
                format_str="epub",
            )

            return FileContent(content=book, metadata=metadata)

        except Exception as e:
            raise FileError(f"Failed to process EPUB book: {e}", cause=e)

    async def _create_epub(self, book: Book) -> EpubBook:
        """Create EPUB book from internal format"""
        try:
            epub_book = epub.EpubBook()

            # Configurar metadados
            epub_book.set_identifier(book.metadata.identifier)
            epub_book.set_title(book.metadata.title)
            for author in book.metadata.authors:
                epub_book.add_author(author)
            epub_book.set_language(book.metadata.language)

            if book.metadata.publisher:
                epub_book.add_metadata("DC", "publisher", book.metadata.publisher)
            if book.metadata.publication_date:
                epub_book.add_metadata("DC", "date", book.metadata.publication_date.isoformat())
            if book.metadata.description:
                epub_book.add_metadata("DC", "description", book.metadata.description)
            for subject in book.metadata.subjects:
                epub_book.add_metadata("DC", "subject", subject)
            if book.metadata.rights:
                epub_book.add_metadata("DC", "rights", book.metadata.rights)

            # Adicionar capítulos
            chapters: list[EpubHtml] = []
            for chapter in book.chapters:
                epub_chapter = epub.EpubHtml(
                    title=chapter.title,
                    file_name=f"chapter_{chapter.order}.xhtml",
                    content=f"<h1>{chapter.title}</h1>{chapter.content}",
                )
                epub_book.add_item(epub_chapter)
                chapters.append(epub_chapter)

            # Adicionar recursos
            for file_name, content in book.resources.items():
                item = EpubItem(
                    uid=f"resource_{len(epub_book.items)}",
                    file_name=file_name,
                    media_type=f"application/{Path(file_name).suffix[1:]}",
                    content=content,
                )
                epub_book.add_item(item)

            # Configurar spine e TOC
            epub_book.toc = cast(list[tuple[Any, ...]], book.toc)
            epub_book.spine = chapters

            # Adicionar navegação
            epub_book.add_item(epub.EpubNcx())
            epub_book.add_item(epub.EpubNav())

            return epub_book

        except Exception as e:
            raise FileError(f"Failed to create EPUB book: {e!s}", cause=e)
