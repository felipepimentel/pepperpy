"""Markup file handler implementation"""

from pathlib import Path
from typing import Any, cast

from bs4 import BeautifulSoup
from lxml import etree, html
from lxml.cssselect import CSSSelector

from ..exceptions import FileError
from ..types import FileContent, FileMetadata
from .base import BaseHandler


class MarkupHandler(BaseHandler):
    """Handler for markup files (HTML, XML)"""

    def __init__(self):
        super().__init__()
        self._parsers = {
            "html": html.HTMLParser(),
            "xml": etree.XMLParser(
                resolve_entities=False,
                no_network=True,
                huge_tree=False,
            ),
        }

    async def read(self, path: Path) -> FileContent:
        """Read markup file"""
        try:
            metadata = await self._get_metadata(path)
            content = await self._read_file(path)

            format = self._detect_format(content)
            if format == "html":
                doc = self._parse_html(content)
            else:
                doc = self._parse_xml(content)

            return FileContent(content=doc, metadata=metadata.metadata, format=format)
        except Exception as e:
            raise FileError(f"Failed to read markup file: {e!s}", cause=e)

    async def write(
        self,
        path: Path,
        content: str | BeautifulSoup | etree._Element,
        metadata: dict[str, Any] | None = None,
    ) -> FileMetadata:
        """Write markup file"""
        try:
            if isinstance(content, BeautifulSoup):
                markup = str(content)
            elif isinstance(content, etree._Element):
                if self._detect_format(content) == "xml":
                    markup = cast(bytes, etree.tostring(content)).decode("utf-8")
                else:
                    markup = cast(
                        bytes,
                        html.tostring(
                            content,
                            doctype="<!DOCTYPE html>",
                        ),
                    ).decode("utf-8")
            else:
                markup = content

            return await self._write_file(path, markup)
        except Exception as e:
            raise FileError(f"Failed to write markup file: {e!s}", cause=e)

    def _detect_format(self, content: str | etree._Element) -> str:
        """Detect markup format"""
        if isinstance(content, etree._Element):
            return "xml" if content.getroottree().docinfo.doctype else "html"

        content = content.strip()
        if content.startswith("<?xml") or content.startswith("<!DOCTYPE"):
            return "xml"
        return "html"

    def _parse_html(self, content: str) -> BeautifulSoup:
        """Parse HTML content"""
        return BeautifulSoup(content, "lxml", parser=self._parsers["html"])

    def _parse_xml(self, content: str) -> etree._Element:
        """Parse XML content securely"""
        parser = etree.XMLParser(
            resolve_entities=False,
            no_network=True,
            huge_tree=False,
            collect_ids=False,
            load_dtd=False,
            remove_comments=True,
            remove_pis=True,
        )

        try:
            return etree.fromstring(content.encode("utf-8"), parser=parser)  # noqa: S320
        except etree.XMLSyntaxError as e:
            raise FileError(f"Invalid XML content: {e!s}") from e

    def _create_selector(self, selector: str, format: str = "html") -> CSSSelector:
        """Create CSS selector"""
        namespaces = (
            {"html": "http://www.w3.org/1999/xhtml"} if format == "html" else None
        )
        return CSSSelector(selector, namespaces=namespaces)

    def _query(self, doc: BeautifulSoup | etree._Element, selector: str) -> Any:
        """Query document using CSS selector"""
        if isinstance(doc, BeautifulSoup):
            return doc.select(selector)

        css = self._create_selector(
            selector, format="xml" if doc.getroottree().docinfo.doctype else "html",
        )
        return css(doc)
