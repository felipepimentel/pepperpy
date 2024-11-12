"""XML/HTML handler implementation"""

import json
import re
from pathlib import Path
from typing import Any, Dict, List, Optional

import cssselect
import lxml.etree as etree
from bs4 import BeautifulSoup, Tag

from ..exceptions import FileError
from ..types import FileContent
from .base import BaseHandler


class MarkupHandler(BaseHandler):
    """Handler for XML and HTML files"""

    def __init__(self):
        self._parser = "lxml"
        self._css_translator = cssselect.HTMLTranslator()

    async def read(self, path: Path) -> FileContent:
        """Read markup file"""
        try:
            metadata = await self._get_metadata(path)
            content = await self._read_file(path)

            return FileContent(content=content, metadata=metadata, format="markup")
        except Exception as e:
            raise FileError(f"Failed to read markup file: {str(e)}", cause=e)

    async def parse(self, content: str, parser: str = "html.parser") -> BeautifulSoup:
        """Parse markup content"""
        try:
            return BeautifulSoup(content, parser)
        except Exception as e:
            raise FileError(f"Failed to parse markup: {str(e)}", cause=e)

    async def query_selector(self, soup: BeautifulSoup, selector: str) -> List[Tag]:
        """Query elements using CSS selector"""
        try:
            return soup.select(selector)
        except Exception as e:
            raise FileError(f"Invalid CSS selector: {str(e)}", cause=e)

    async def xpath_query(self, content: str, xpath: str) -> List[Any]:
        """Query elements using XPath"""
        try:
            tree = etree.fromstring(content)
            return tree.xpath(xpath)
        except Exception as e:
            raise FileError(f"Invalid XPath query: {str(e)}", cause=e)

    async def extract_data(self, soup: BeautifulSoup, schema: Dict[str, str]) -> Dict[str, Any]:
        """Extract data using CSS selectors"""
        try:
            result = {}
            for key, selector in schema.items():
                elements = soup.select(selector)
                if elements:
                    if len(elements) == 1:
                        result[key] = elements[0].get_text(strip=True)
                    else:
                        result[key] = [el.get_text(strip=True) for el in elements]
            return result
        except Exception as e:
            raise FileError(f"Failed to extract data: {str(e)}", cause=e)

    async def transform_xslt(self, content: str, xslt_path: Path) -> str:
        """Transform XML using XSLT"""
        try:
            xml_doc = etree.fromstring(content)
            xslt_doc = etree.parse(str(xslt_path))
            transform = etree.XSLT(xslt_doc)
            return str(transform(xml_doc))
        except Exception as e:
            raise FileError(f"XSLT transformation failed: {str(e)}", cause=e)

    async def validate_schema(self, content: str, schema_path: Path) -> List[str]:
        """Validate XML against schema"""
        try:
            schema_doc = etree.parse(str(schema_path))
            schema = etree.XMLSchema(schema_doc)
            parser = etree.XMLParser(schema=schema)

            try:
                etree.fromstring(content, parser)
                return []
            except etree.XMLSyntaxError as e:
                return [str(error) for error in e.error_log]
        except Exception as e:
            raise FileError(f"Schema validation failed: {str(e)}", cause=e)

    async def to_json(self, soup: BeautifulSoup, pretty: bool = True) -> str:
        """Convert markup to JSON"""
        try:

            def node_to_dict(node):
                if isinstance(node, str):
                    return node.strip()

                result = {
                    "tag": node.name,
                    "attrs": dict(node.attrs),
                }

                children = [
                    node_to_dict(child)
                    for child in node.children
                    if not isinstance(child, str) or child.strip()
                ]

                if children:
                    result["children"] = children

                text = node.get_text(strip=True)
                if text:
                    result["text"] = text

                return result

            data = node_to_dict(soup)
            return json.dumps(data, indent=2 if pretty else None)

        except Exception as e:
            raise FileError(f"JSON conversion failed: {str(e)}", cause=e)

    async def clean_html(
        self, content: str, allowed_tags: Optional[List[str]] = None, strip_comments: bool = True
    ) -> str:
        """Clean and sanitize HTML"""
        try:
            soup = BeautifulSoup(content, "html.parser")

            if strip_comments:
                for comment in soup.find_all(string=lambda text: isinstance(text, str)):
                    comment.extract()

            if allowed_tags:
                for tag in soup.find_all():
                    if tag.name not in allowed_tags:
                        tag.unwrap()

            return str(soup)

        except Exception as e:
            raise FileError(f"HTML cleaning failed: {str(e)}", cause=e)

    async def extract_links(
        self, soup: BeautifulSoup, base_url: Optional[str] = None
    ) -> List[Dict[str, str]]:
        """Extract all links with metadata"""
        try:
            links = []
            for a in soup.find_all("a", href=True):
                href = a["href"]
                if base_url and not href.startswith(("http://", "https://")):
                    href = f"{base_url.rstrip('/')}/{href.lstrip('/')}"

                links.append(
                    {
                        "text": a.get_text(strip=True),
                        "href": href,
                        "title": a.get("title", ""),
                        "rel": a.get("rel", []),
                        "target": a.get("target", "_self"),
                    }
                )
            return links
        except Exception as e:
            raise FileError(f"Failed to extract links: {str(e)}", cause=e)

    async def extract_tables(self, soup: BeautifulSoup) -> List[List[List[str]]]:
        """Extract tables as 2D arrays"""
        try:
            tables = []
            for table in soup.find_all("table"):
                table_data = []
                rows = table.find_all("tr")

                for row in rows:
                    cols = row.find_all(["td", "th"])
                    row_data = [col.get_text(strip=True) for col in cols]
                    table_data.append(row_data)

                tables.append(table_data)
            return tables
        except Exception as e:
            raise FileError(f"Failed to extract tables: {str(e)}", cause=e)

    async def minify(
        self, content: str, remove_comments: bool = True, remove_whitespace: bool = True
    ) -> str:
        """Minify markup content"""
        try:
            soup = BeautifulSoup(content, "html.parser")

            if remove_comments:
                for comment in soup.find_all(string=lambda text: isinstance(text, str)):
                    comment.extract()

            if remove_whitespace:
                content = str(soup)
                content = re.sub(r"\s+", " ", content)
                content = re.sub(r">\s+<", "><", content)

            return content.strip()

        except Exception as e:
            raise FileError(f"Minification failed: {str(e)}", cause=e)
