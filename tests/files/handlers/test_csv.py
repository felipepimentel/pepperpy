"""Tests for CSV file handler"""

import csv
from pathlib import Path
from unittest.mock import Mock, mock_open, patch

import pytest

from pepperpy.files.exceptions import FileError
from pepperpy.files.handlers.csv import CSVFileHandler
from pepperpy.files.types import FileContent, FileMetadata


@pytest.fixture
def csv_handler():
    """Fixture for CSV handler"""
    return CSVFileHandler()


@pytest.mark.asyncio
async def test_csv_handler_read(csv_handler):
    """Test CSV handler read operation"""
    await csv_handler.initialize()

    test_content = "header1,header2\nvalue1,value2\n"
    mock_path = Mock(spec=Path)
    mock_path.exists.return_value = True
    mock_path.is_file.return_value = True
    mock_path.stat.return_value = Mock(st_size=len(test_content))
    mock_path.name = "test.csv"
    mock_path.suffix = ".csv"

    m = mock_open(read_data=test_content)
    with patch("builtins.open", m):
        content = await csv_handler.read(mock_path)
        assert isinstance(content.content, list)
        assert len(content.content) == 1
        assert content.content[0] == {"header1": "value1", "header2": "value2"}


@pytest.mark.asyncio
async def test_csv_handler_write(csv_handler):
    """Test CSV handler write operation"""
    await csv_handler.initialize()

    test_file = Path("/test/test.csv")
    csv_data = [{"header1": "value1", "header2": "value2"}]
    content = FileContent(
        content=csv_data,
        metadata=FileMetadata(
            name="test.csv",
            mime_type="text/csv",
            path=test_file,
            type="text/csv",
            extension=".csv",
            format="utf-8",
            size=100,
        ),
    )

    mock_path = Mock(spec=Path)
    mock_path.exists.return_value = True
    mock_path.parent.exists.return_value = True
    mock_path.name = "test.csv"
    mock_path.suffix = ".csv"

    m = mock_open()
    with patch("builtins.open", m):
        await csv_handler.write(mock_path, content)


@pytest.mark.asyncio
async def test_csv_handler_invalid_content(csv_handler):
    """Test CSV handler with invalid content"""
    await csv_handler.initialize()

    # Conteúdo CSV inválido (sem headers e com número irregular de campos)
    test_content = "a,b,c\n1,2\n3,4,5,6"
    mock_path = Mock(spec=Path)
    mock_path.exists.return_value = True
    mock_path.is_file.return_value = True
    mock_path.stat.return_value = Mock(st_size=len(test_content))
    mock_path.name = "test.csv"
    mock_path.suffix = ".csv"
    mock_path.__str__ = Mock(return_value="/test/test.csv")

    m = mock_open(read_data=test_content)
    with patch("builtins.open", m):
        with pytest.raises(FileError, match="Invalid CSV format"):
            await csv_handler.read(mock_path)


@pytest.mark.asyncio
async def test_csv_handler_empty_content(csv_handler):
    """Test CSV handler with empty content"""
    await csv_handler.initialize()

    test_file = Path("/test/empty.csv")
    content = FileContent(
        content=[{"header": "value"}],  # Minimal valid content
        metadata=FileMetadata(
            name="empty.csv",
            mime_type="text/csv",
            path=test_file,
            type="text/csv",
            extension=".csv",
            format="utf-8",
            size=0,
        ),
    )

    mock_path = Mock(spec=Path)
    mock_path.exists.return_value = True
    mock_path.parent.exists.return_value = True
    mock_path.name = "empty.csv"
    mock_path.suffix = ".csv"

    m = mock_open()
    with patch("builtins.open", m):
        await csv_handler.write(mock_path, content)


@pytest.mark.asyncio
async def test_csv_handler_invalid_write_content(csv_handler):
    """Test CSV handler with invalid write content"""
    await csv_handler.initialize()

    test_file = Path("/test/test.csv")
    content = FileContent(
        content="invalid content type",  # Should be list of dicts
        metadata=FileMetadata(
            name="test.csv",
            mime_type="text/csv",
            path=test_file,
            type="text/csv",
            extension=".csv",
            format="utf-8",
            size=100,
        ),
    )

    mock_path = Mock(spec=Path)
    mock_path.exists.return_value = True
    mock_path.parent.exists.return_value = True
    mock_path.name = "test.csv"
    mock_path.suffix = ".csv"

    with patch("pathlib.Path", return_value=mock_path), pytest.raises(
        FileError, match="Invalid CSV content"
    ):
        await csv_handler.write(mock_path, content)


@pytest.mark.asyncio
async def test_csv_handler_read_with_custom_delimiter(csv_handler):
    """Test CSV handler read operation with custom delimiter"""
    await csv_handler.initialize()

    test_content = "header1;header2\nvalue1;value2\n"
    mock_path = Mock(spec=Path)
    mock_path.exists.return_value = True
    mock_path.is_file.return_value = True
    mock_path.stat.return_value = Mock(st_size=len(test_content))
    mock_path.name = "test.csv"
    mock_path.suffix = ".csv"

    # Create a list to simulate DictReader rows
    mock_rows = [{"header1": "value1", "header2": "value2"}]
    mock_reader = Mock()
    mock_reader.fieldnames = ["header1", "header2"]
    mock_reader.__iter__ = lambda self: iter(mock_rows)

    m = mock_open(read_data=test_content)
    with patch("builtins.open", m), patch(
        "csv.DictReader", return_value=mock_reader
    ) as mock_dict_reader:
        content = await csv_handler.read(mock_path, delimiter=";")
        assert isinstance(content.content, list)
        assert len(content.content) == 1
        assert content.content[0] == {"header1": "value1", "header2": "value2"}

        # Verify DictReader was called with correct delimiter
        mock_dict_reader.assert_called_once()
        _, kwargs = mock_dict_reader.call_args
        assert kwargs["delimiter"] == ";"


@pytest.mark.asyncio
async def test_csv_handler_write_with_custom_delimiter(csv_handler):
    """Test CSV handler write operation with custom delimiter"""
    await csv_handler.initialize()

    test_file = Path("/test/test.csv")
    csv_data = [{"header1": "value1", "header2": "value2"}]
    content = FileContent(
        content=csv_data,
        metadata=FileMetadata(
            name="test.csv",
            mime_type="text/csv",
            path=test_file,
            type="text/csv",
            extension=".csv",
            format="utf-8",
            size=100,
        ),
    )

    mock_path = Mock(spec=Path)
    mock_path.exists.return_value = True
    mock_path.parent.exists.return_value = True
    mock_path.name = "test.csv"
    mock_path.suffix = ".csv"

    m = mock_open()
    with patch("builtins.open", m), patch("csv.DictWriter") as mock_dict_writer:
        # Configure mock DictWriter
        mock_writer_instance = Mock()
        mock_dict_writer.return_value = mock_writer_instance

        await csv_handler.write(mock_path, content, delimiter=";")

        # Verify DictWriter was called with correct parameters
        _, kwargs = mock_dict_writer.call_args
        assert kwargs.get("delimiter") == ";"
        assert kwargs.get("fieldnames") == ["header1", "header2"]


@pytest.mark.asyncio
async def test_csv_handler_read_empty_file(csv_handler):
    """Test CSV handler read operation with empty file"""
    await csv_handler.initialize()

    test_content = ""
    mock_path = Mock(spec=Path)
    mock_path.exists.return_value = True
    mock_path.is_file.return_value = True
    mock_path.stat.return_value = Mock(st_size=0)
    mock_path.name = "test.csv"
    mock_path.suffix = ".csv"

    m = mock_open(read_data=test_content)
    with patch("builtins.open", m):
        with pytest.raises(FileError, match="Empty CSV file"):
            await csv_handler.read(mock_path)


@pytest.mark.asyncio
async def test_csv_handler_read_headers_only(csv_handler):
    """Test CSV handler read operation with headers but no data"""
    await csv_handler.initialize()

    test_content = "header1,header2\n"
    mock_path = Mock(spec=Path)
    mock_path.exists.return_value = True
    mock_path.is_file.return_value = True
    mock_path.stat.return_value = Mock(st_size=len(test_content))
    mock_path.name = "test.csv"
    mock_path.suffix = ".csv"

    # Create an empty list to simulate DictReader with no rows
    mock_rows = []
    mock_reader = Mock()
    mock_reader.fieldnames = ["header1", "header2"]
    mock_reader.__iter__ = lambda self: iter(mock_rows)

    m = mock_open(read_data=test_content)
    with patch("builtins.open", m), patch("csv.DictReader", return_value=mock_reader):
        with pytest.raises(FileError, match="Empty CSV file"):
            await csv_handler.read(mock_path)


@pytest.mark.asyncio
async def test_csv_handler_write_no_headers(csv_handler):
    """Test CSV handler write operation with empty data (no headers)"""
    await csv_handler.initialize()

    test_file = Path("/test/test.csv")
    csv_data = []  # Empty data
    content = FileContent(
        content=csv_data,
        metadata=FileMetadata(
            name="test.csv",
            mime_type="text/csv",
            path=test_file,
            type="text/csv",
            extension=".csv",
            format="utf-8",
            size=0,
        ),
    )

    mock_path = Mock(spec=Path)
    mock_path.exists.return_value = True
    mock_path.parent.exists.return_value = True
    mock_path.name = "test.csv"
    mock_path.suffix = ".csv"

    with pytest.raises(FileError, match="Invalid CSV content: cannot be empty"):
        await csv_handler.write(mock_path, content)


@pytest.mark.asyncio
async def test_csv_handler_read_with_custom_encoding(csv_handler):
    """Test CSV handler read operation with custom encoding"""
    await csv_handler.initialize()

    test_content = "header1,header2\nvalue1,value2\n"
    mock_path = Mock(spec=Path)
    mock_path.exists.return_value = True
    mock_path.is_file.return_value = True
    mock_path.stat.return_value = Mock(st_size=len(test_content))
    mock_path.name = "test.csv"
    mock_path.suffix = ".csv"

    # Create a list to simulate DictReader rows
    mock_rows = [{"header1": "value1", "header2": "value2"}]
    mock_reader = Mock()
    mock_reader.fieldnames = ["header1", "header2"]
    mock_reader.__iter__ = lambda self: iter(mock_rows)

    m = mock_open(read_data=test_content)
    with patch("builtins.open", m) as mock_open_call, patch(
        "csv.DictReader", return_value=mock_reader
    ):
        await csv_handler.read(mock_path, encoding="utf-16")

        # Verify open was called with correct encoding
        mock_open_call.assert_called_once_with(mock_path, "r", encoding="utf-16", newline="")


@pytest.mark.asyncio
async def test_csv_handler_write_with_custom_encoding(csv_handler):
    """Test CSV handler write operation with custom encoding"""
    await csv_handler.initialize()

    test_file = Path("/test/test.csv")
    csv_data = [{"header1": "value1", "header2": "value2"}]
    content = FileContent(
        content=csv_data,
        metadata=FileMetadata(
            name="test.csv",
            mime_type="text/csv",
            path=test_file,
            type="text/csv",
            extension=".csv",
            format="utf-16",
            size=100,
        ),
    )

    mock_path = Mock(spec=Path)
    mock_path.exists.return_value = True
    mock_path.parent.exists.return_value = True
    mock_path.name = "test.csv"
    mock_path.suffix = ".csv"

    m = mock_open()
    with patch("builtins.open", m) as mock_open_call:
        await csv_handler.write(mock_path, content, encoding="utf-16")

        # Verify open was called with correct encoding
        _, kwargs = mock_open_call.call_args
        assert kwargs.get("encoding") == "utf-16"


@pytest.mark.asyncio
async def test_csv_handler_read_with_quoting(csv_handler):
    """Test CSV handler read operation with quoted fields"""
    await csv_handler.initialize()

    test_content = 'header1,header2\n"value,1","value,2"\n'
    mock_path = Mock(spec=Path)
    mock_path.exists.return_value = True
    mock_path.is_file.return_value = True
    mock_path.stat.return_value = Mock(st_size=len(test_content))
    mock_path.name = "test.csv"
    mock_path.suffix = ".csv"

    m = mock_open(read_data=test_content)
    with patch("builtins.open", m):
        content = await csv_handler.read(mock_path)
        assert isinstance(content.content, list)
        assert len(content.content) == 1
        assert content.content[0] == {"header1": "value,1", "header2": "value,2"}


@pytest.mark.asyncio
async def test_csv_handler_write_with_quoting(csv_handler):
    """Test CSV handler write operation with fields requiring quotes"""
    await csv_handler.initialize()

    test_file = Path("/test/test.csv")
    csv_data = [{"header1": "value,1", "header2": "value,2"}]
    content = FileContent(
        content=csv_data,
        metadata=FileMetadata(
            name="test.csv",
            mime_type="text/csv",
            path=test_file,
            type="text/csv",
            extension=".csv",
            format="utf-8",
            size=100,
        ),
    )

    mock_path = Mock(spec=Path)
    mock_path.exists.return_value = True
    mock_path.parent.exists.return_value = True
    mock_path.name = "test.csv"
    mock_path.suffix = ".csv"

    m = mock_open()
    with patch("builtins.open", m), patch("csv.DictWriter") as mock_dict_writer:
        # Configure mock DictWriter
        mock_writer_instance = Mock()
        mock_dict_writer.return_value = mock_writer_instance

        await csv_handler.write(mock_path, content)

        # Verify DictWriter was called with correct parameters
        _, kwargs = mock_dict_writer.call_args
        assert kwargs.get("quoting") == csv.QUOTE_MINIMAL
        assert kwargs.get("fieldnames") == ["header1", "header2"]


@pytest.mark.asyncio
async def test_csv_handler_read_invalid_path(csv_handler):
    """Test CSV handler read operation with invalid path"""
    await csv_handler.initialize()

    mock_path = Mock(spec=Path)
    mock_path.exists.return_value = False
    mock_path.name = "test.csv"
    mock_path.suffix = ".csv"
    mock_path.__str__ = Mock(return_value="/test/test.csv")

    with pytest.raises(FileError, match="File does not exist"):
        await csv_handler.read(mock_path)


@pytest.mark.asyncio
async def test_csv_handler_write_invalid_path(csv_handler):
    """Test CSV handler write operation with invalid path"""
    await csv_handler.initialize()

    test_file = Path("/test/test.csv")
    csv_data = [{"header1": "value1", "header2": "value2"}]
    content = FileContent(
        content=csv_data,
        metadata=FileMetadata(
            name="test.csv",
            mime_type="text/csv",
            path=test_file,
            type="text/csv",
            extension=".csv",
            format="utf-8",
            size=100,
        ),
    )

    mock_path = Mock(spec=Path)
    mock_path.exists.return_value = True
    mock_path.name = "test.csv"
    mock_path.suffix = ".csv"
    mock_path.__str__ = Mock(return_value="/test/test.csv")

    # Mock do parent path
    parent_mock = Mock(spec=Path)
    parent_mock.exists.return_value = False
    mock_path.parent = parent_mock

    with pytest.raises(FileError, match="Parent directory does not exist"):
        await csv_handler.write(mock_path, content)
