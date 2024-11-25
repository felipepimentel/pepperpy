import json
from pathlib import Path

import pytest
import yaml


@pytest.fixture
def test_files(tmp_path: Path) -> Path:
    """Create test files for handlers"""
    data_dir = tmp_path / "data"
    data_dir.mkdir()

    # Text file
    text_file = data_dir / "test.txt"
    text_file.write_text("Test content", encoding="utf-8")

    # JSON file
    json_file = data_dir / "test.json"
    json_data = {"test": "data", "number": 42}
    json_file.write_text(json.dumps(json_data), encoding="utf-8")

    # YAML file
    yaml_file = data_dir / "test.yaml"
    yaml_data = {"test": "data", "list": [1, 2, 3]}
    yaml_file.write_text(yaml.dump(yaml_data), encoding="utf-8")

    # Markdown file
    md_file = data_dir / "test.md"
    md_file.write_text("# Test\nContent with *markdown*", encoding="utf-8")

    # PDF file
    pdf_file = data_dir / "test.pdf"
    pdf_file.write_bytes(b"%PDF-1.4\ntest pdf content")

    return data_dir


@pytest.fixture
def test_write_dir(test_files: Path) -> Path:
    """Get write directory path"""
    write_dir = test_files / "write"
    write_dir.mkdir(exist_ok=True)
    return write_dir


@pytest.fixture
def handler_config(test_files: Path):
    """Fixture for handler config"""
    from pepperpy.files.config import FileHandlerConfig

    return FileHandlerConfig(
        base_path=test_files,
        allowed_extensions={".txt", ".json", ".yaml", ".md", ".mp3", ".wav", ".pdf", ".csv"},
        max_file_size=1024 * 1024,
        metadata={"environment": "test"},
    )


@pytest.fixture
def mock_audio_content() -> bytes:
    """Get mock audio content"""
    return b"%MP3\x00test audio content"


@pytest.fixture
def mock_wav_content() -> bytes:
    """Get mock WAV content"""
    return b"RIFF\x00\x00\x00\x00WAVEtest audio content"
