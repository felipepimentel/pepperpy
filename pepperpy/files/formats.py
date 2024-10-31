"""File format handlers for various file types."""
from typing import Any, Dict, List, Union, Optional
from pathlib import Path
import json
import yaml
import toml
import configparser
import ebooklib
from ebooklib import epub
import webvtt
from bs4 import BeautifulSoup
import csv
import xml.etree.ElementTree as ET

class FileHandler:
    """Base class for file handlers."""
    
    @classmethod
    def read(cls, path: Union[str, Path], **kwargs) -> Any:
        """Read file content."""
        raise NotImplementedError
    
    @classmethod
    def write(cls, data: Any, path: Union[str, Path], **kwargs) -> None:
        """Write data to file."""
        raise NotImplementedError

class JSONHandler(FileHandler):
    """JSON file handler."""
    
    @classmethod
    def read(cls, path: Union[str, Path], **kwargs) -> Dict:
        with open(path, 'r', encoding='utf-8') as f:
            return json.load(f)
    
    @classmethod
    def write(cls, data: Dict, path: Union[str, Path], **kwargs) -> None:
        with open(path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=kwargs.get('indent', 2))

class YAMLHandler(FileHandler):
    """YAML file handler."""
    
    @classmethod
    def read(cls, path: Union[str, Path], **kwargs) -> Dict:
        with open(path, 'r', encoding='utf-8') as f:
            return yaml.safe_load(f)
    
    @classmethod
    def write(cls, data: Dict, path: Union[str, Path], **kwargs) -> None:
        with open(path, 'w', encoding='utf-8') as f:
            yaml.dump(data, f, **kwargs)

class TOMLHandler(FileHandler):
    """TOML file handler."""
    
    @classmethod
    def read(cls, path: Union[str, Path], **kwargs) -> Dict:
        with open(path, 'r', encoding='utf-8') as f:
            return toml.load(f)
    
    @classmethod
    def write(cls, data: Dict, path: Union[str, Path], **kwargs) -> None:
        with open(path, 'w', encoding='utf-8') as f:
            toml.dump(data, f)

class INIHandler(FileHandler):
    """INI file handler."""
    
    @classmethod
    def read(cls, path: Union[str, Path], **kwargs) -> Dict:
        config = configparser.ConfigParser()
        config.read(path)
        return {
            section: dict(config[section])
            for section in config.sections()
        }
    
    @classmethod
    def write(cls, data: Dict, path: Union[str, Path], **kwargs) -> None:
        config = configparser.ConfigParser()
        for section, values in data.items():
            config[section] = {k: str(v) for k, v in values.items()}
        with open(path, 'w', encoding='utf-8') as f:
            config.write(f)

class EPUBHandler(FileHandler):
    """EPUB file handler."""
    
    @classmethod
    def read(cls, path: Union[str, Path], **kwargs) -> Dict:
        book = epub.read_epub(str(path))
        content = []
        
        for item in book.get_items():
            if item.get_type() == ebooklib.ITEM_DOCUMENT:
                soup = BeautifulSoup(item.get_content(), 'html.parser')
                content.append(soup.get_text())
                
        return {
            'title': book.get_metadata('DC', 'title')[0][0],
            'creator': book.get_metadata('DC', 'creator')[0][0],
            'content': content
        }
    
    @classmethod
    def write(cls, data: Dict, path: Union[str, Path], **kwargs) -> None:
        book = epub.EpubBook()
        
        # Set metadata
        book.set_title(data.get('title', 'Untitled'))
        book.set_language('en')
        book.add_author(data.get('creator', 'Unknown'))
        
        # Add content
        chapters = []
        for i, content in enumerate(data.get('content', []), 1):
            chapter = epub.EpubHtml(
                title=f'Chapter {i}',
                file_name=f'chapter_{i}.xhtml',
                content=content
            )
            book.add_item(chapter)
            chapters.append(chapter)
        
        # Create table of contents
        book.toc = chapters
        
        # Add default NCX and Nav file
        book.add_item(epub.EpubNcx())
        book.add_item(epub.EpubNav())
        
        # Write EPUB file
        epub.write_epub(str(path), book, {})

class VTTHandler(FileHandler):
    """WebVTT subtitle file handler."""
    
    @classmethod
    def read(cls, path: Union[str, Path], **kwargs) -> List[Dict]:
        captions = []
        for caption in webvtt.read(str(path)):
            captions.append({
                'start': caption.start,
                'end': caption.end,
                'text': caption.text
            })
        return captions
    
    @classmethod
    def write(cls, data: List[Dict], path: Union[str, Path], **kwargs) -> None:
        vtt = webvtt.WebVTT()
        for caption in data:
            vtt.captions.append(
                webvtt.Caption(
                    caption['start'],
                    caption['end'],
                    caption['text']
                )
            )
        vtt.save(str(path))

class XMLHandler(FileHandler):
    """XML file handler."""
    
    @classmethod
    def read(cls, path: Union[str, Path], **kwargs) -> Dict:
        tree = ET.parse(path)
        root = tree.getroot()
        
        def xml_to_dict(element):
            result = {}
            for child in element:
                if len(child) > 0:
                    value = xml_to_dict(child)
                else:
                    value = child.text
                
                if child.tag in result:
                    if isinstance(result[child.tag], list):
                        result[child.tag].append(value)
                    else:
                        result[child.tag] = [result[child.tag], value]
                else:
                    result[child.tag] = value
            return result
        
        return xml_to_dict(root)
    
    @classmethod
    def write(cls, data: Dict, path: Union[str, Path], **kwargs) -> None:
        def dict_to_xml(parent: ET.Element, data: Dict):
            for key, value in data.items():
                child = ET.SubElement(parent, key)
                if isinstance(value, dict):
                    dict_to_xml(child, value)
                elif isinstance(value, list):
                    for item in value:
                        subchild = ET.SubElement(parent, key)
                        if isinstance(item, dict):
                            dict_to_xml(subchild, item)
                        else:
                            subchild.text = str(item)
                else:
                    child.text = str(value)
        
        root = ET.Element('root')
        dict_to_xml(root, data)
        tree = ET.ElementTree(root)
        tree.write(path, encoding='utf-8', xml_declaration=True)

class FileManager:
    """Central file operations manager."""
    
    _handlers = {
        '.json': JSONHandler,
        '.yaml': YAMLHandler,
        '.yml': YAMLHandler,
        '.toml': TOMLHandler,
        '.ini': INIHandler,
        '.epub': EPUBHandler,
        '.vtt': VTTHandler,
        '.xml': XMLHandler
    }
    
    @classmethod
    def read(cls, path: Union[str, Path], **kwargs) -> Any:
        """Read file content."""
        path = Path(path)
        if path.suffix not in cls._handlers:
            raise ValueError(f"Unsupported file type: {path.suffix}")
        return cls._handlers[path.suffix].read(path, **kwargs)
    
    @classmethod
    def write(cls, data: Any, path: Union[str, Path], **kwargs) -> None:
        """Write data to file."""
        path = Path(path)
        if path.suffix not in cls._handlers:
            raise ValueError(f"Unsupported file type: {path.suffix}")
        cls._handlers[path.suffix].write(data, path, **kwargs)

# Convenience functions
def read_file(path: Union[str, Path], **kwargs) -> Any:
    """Read file content."""
    return FileManager.read(path, **kwargs)

def write_file(data: Any, path: Union[str, Path], **kwargs) -> None:
    """Write data to file."""
    FileManager.write(data, path, **kwargs) 