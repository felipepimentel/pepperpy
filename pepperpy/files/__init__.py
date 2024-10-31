"""File operations with various formats."""
from typing import Any, Dict, List, Union, Optional
from pathlib import Path
import json
import yaml
import toml
import csv
import shutil
import tempfile
from abc import ABC, abstractmethod

class FileHandler(ABC):
    """Base class for file handlers."""
    
    @abstractmethod
    def read(self, path: Union[str, Path]) -> Any:
        """Read file content."""
        pass
    
    @abstractmethod
    def write(self, data: Any, path: Union[str, Path]) -> None:
        """Write data to file."""
        pass
    
    @abstractmethod
    def append(self, data: Any, path: Union[str, Path]) -> None:
        """Append data to file."""
        pass

class JSONHandler(FileHandler):
    """JSON file handler."""
    
    def read(self, path: Union[str, Path]) -> Dict:
        with open(path) as f:
            return json.load(f)
    
    def write(self, data: Dict, path: Union[str, Path]) -> None:
        with open(path, 'w') as f:
            json.dump(data, f, indent=2)
    
    def append(self, data: Dict, path: Union[str, Path]) -> None:
        current = self.read(path) if Path(path).exists() else {}
        current.update(data)
        self.write(current, path)

class YAMLHandler(FileHandler):
    """YAML file handler."""
    
    def read(self, path: Union[str, Path]) -> Dict:
        with open(path) as f:
            return yaml.safe_load(f)
    
    def write(self, data: Dict, path: Union[str, Path]) -> None:
        with open(path, 'w') as f:
            yaml.dump(data, f)
    
    def append(self, data: Dict, path: Union[str, Path]) -> None:
        current = self.read(path) if Path(path).exists() else {}
        current.update(data)
        self.write(current, path)

class CSVHandler(FileHandler):
    """CSV file handler."""
    
    def read(
        self,
        path: Union[str, Path],
        headers: bool = True
    ) -> List[Dict[str, str]]:
        with open(path) as f:
            reader = csv.DictReader(f) if headers else csv.reader(f)
            return list(reader)
    
    def write(
        self,
        data: List[Dict[str, str]],
        path: Union[str, Path],
        headers: Optional[List[str]] = None
    ) -> None:
        headers = headers or (list(data[0].keys()) if data else [])
        with open(path, 'w', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=headers)
            writer.writeheader()
            writer.writerows(data)
    
    def append(
        self,
        data: List[Dict[str, str]],
        path: Union[str, Path]
    ) -> None:
        current = self.read(path) if Path(path).exists() else []
        current.extend(data)
        self.write(current, path)

class TextHandler(FileHandler):
    """Text file handler."""
    
    def read(self, path: Union[str, Path]) -> str:
        with open(path) as f:
            return f.read()
    
    def write(self, data: str, path: Union[str, Path]) -> None:
        with open(path, 'w') as f:
            f.write(data)
    
    def append(self, data: str, path: Union[str, Path]) -> None:
        with open(path, 'a') as f:
            f.write(data)

class FileManager:
    """Central file operations manager."""
    
    _handlers = {
        '.json': JSONHandler(),
        '.yaml': YAMLHandler(),
        '.yml': YAMLHandler(),
        '.csv': CSVHandler(),
        '.txt': TextHandler()
    }
    
    @classmethod
    def read(cls, path: Union[str, Path]) -> Any:
        """Read file content."""
        path = Path(path)
        if path.suffix not in cls._handlers:
            raise ValueError(f"Unsupported file type: {path.suffix}")
        return cls._handlers[path.suffix].read(path)
    
    @classmethod
    def write(cls, data: Any, path: Union[str, Path]) -> None:
        """Write data to file."""
        path = Path(path)
        if path.suffix not in cls._handlers:
            raise ValueError(f"Unsupported file type: {path.suffix}")
        cls._handlers[path.suffix].write(data, path)
    
    @classmethod
    def append(cls, data: Any, path: Union[str, Path]) -> None:
        """Append data to file."""
        path = Path(path)
        if path.suffix not in cls._handlers:
            raise ValueError(f"Unsupported file type: {path.suffix}")
        cls._handlers[path.suffix].append(data, path)
    
    @classmethod
    def copy(
        cls,
        source: Union[str, Path],
        destination: Union[str, Path]
    ) -> None:
        """Copy file."""
        shutil.copy2(source, destination)
    
    @classmethod
    def move(
        cls,
        source: Union[str, Path],
        destination: Union[str, Path]
    ) -> None:
        """Move file."""
        shutil.move(source, destination)
    
    @classmethod
    def delete(cls, path: Union[str, Path]) -> None:
        """Delete file."""
        Path(path).unlink()
    
    @classmethod
    def exists(cls, path: Union[str, Path]) -> bool:
        """Check if file exists."""
        return Path(path).exists()
    
    @classmethod
    def is_file(cls, path: Union[str, Path]) -> bool:
        """Check if path is a file."""
        return Path(path).is_file()
    
    @classmethod
    def is_dir(cls, path: Union[str, Path]) -> bool:
        """Check if path is a directory."""
        return Path(path).is_dir()
    
    @classmethod
    def create_temp_file(
        cls,
        suffix: Optional[str] = None,
        prefix: Optional[str] = None,
        dir: Optional[Union[str, Path]] = None
    ) -> Path:
        """Create temporary file."""
        return Path(tempfile.mktemp(suffix=suffix, prefix=prefix, dir=dir))

# Convenience functions
def read_file(path: Union[str, Path]) -> Any:
    return FileManager.read(path)

def write_file(data: Any, path: Union[str, Path]) -> None:
    FileManager.write(data, path)

def append_file(data: Any, path: Union[str, Path]) -> None:
    FileManager.append(data, path) 