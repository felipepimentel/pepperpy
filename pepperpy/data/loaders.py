"""Document loaders for different formats."""
from typing import List, Optional, Dict, Any
from abc import ABC, abstractmethod
import json
import csv
from pathlib import Path
from .types import Document, TextFormat

class DocumentLoader(ABC):
    """Base class for document loaders."""
    
    @abstractmethod
    async def load(self, source: str) -> List[Document]:
        """Load documents from source."""
        pass

class TextLoader(DocumentLoader):
    """Load plain text documents."""
    
    async def load(self, source: str) -> List[Document]:
        with open(source, 'r', encoding='utf-8') as f:
            content = f.read()
            
        return [Document(
            content=content,
            format=TextFormat.PLAIN,
            metadata={"source": source}
        )]

class JSONLoader(DocumentLoader):
    """Load JSON documents."""
    
    def __init__(
        self,
        content_key: str = "content",
        metadata_keys: Optional[List[str]] = None
    ):
        self.content_key = content_key
        self.metadata_keys = metadata_keys or []
    
    async def load(self, source: str) -> List[Document]:
        with open(source, 'r', encoding='utf-8') as f:
            data = json.load(f)
            
        if isinstance(data, list):
            return [self._create_document(item) for item in data]
        return [self._create_document(data)]
    
    def _create_document(self, data: Dict) -> Document:
        metadata = {
            key: data[key]
            for key in self.metadata_keys
            if key in data
        }
        metadata["source"] = "json"
        
        return Document(
            content=data[self.content_key],
            format=TextFormat.PLAIN,
            metadata=metadata
        )

class CSVLoader(DocumentLoader):
    """Load CSV documents."""
    
    def __init__(
        self,
        content_columns: List[str],
        metadata_columns: Optional[List[str]] = None,
        delimiter: str = ','
    ):
        self.content_columns = content_columns
        self.metadata_columns = metadata_columns or []
        self.delimiter = delimiter
    
    async def load(self, source: str) -> List[Document]:
        documents = []
        
        with open(source, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f, delimiter=self.delimiter)
            
            for row in reader:
                content = ' '.join(
                    str(row[col])
                    for col in self.content_columns
                    if col in row
                )
                
                metadata = {
                    col: row[col]
                    for col in self.metadata_columns
                    if col in row
                }
                metadata["source"] = "csv"
                
                documents.append(Document(
                    content=content,
                    format=TextFormat.PLAIN,
                    metadata=metadata
                ))
                
        return documents

class LoaderFactory:
    """Factory for document loaders."""
    
    _loaders = {
        ".txt": TextLoader,
        ".json": JSONLoader,
        ".csv": CSVLoader
    }
    
    @classmethod
    def get_loader(
        cls,
        file_path: str,
        **kwargs
    ) -> DocumentLoader:
        """Get appropriate loader for file type."""
        ext = Path(file_path).suffix.lower()
        
        if ext not in cls._loaders:
            raise ValueError(f"Unsupported file type: {ext}")
            
        return cls._loaders[ext](**kwargs) 