"""Serialization utilities"""

import json
from abc import ABC, abstractmethod
from datetime import datetime
from typing import Any, Protocol

import msgpack
from typing_extensions import TypeAlias

SerializableData: TypeAlias = Any  # Pode ser refinado para tipos específicos


class DateTimeSerializer(Protocol):
    """Protocol for datetime serialization"""

    @staticmethod
    def serialize(obj: Any) -> str | Any: ...

    @staticmethod
    def deserialize(obj: dict[str, Any]) -> datetime | dict[str, Any]: ...


class DefaultDateTimeHandler:
    """Default handler for datetime serialization"""

    @staticmethod
    def serialize(obj: Any) -> str | Any:
        """Serialize datetime objects"""
        if isinstance(obj, datetime):
            return {"__datetime__": obj.isoformat()}
        return obj

    @staticmethod
    def deserialize(obj: dict[str, Any]) -> datetime | dict[str, Any]:
        """Deserialize datetime objects"""
        if "__datetime__" in obj:
            return datetime.fromisoformat(obj["__datetime__"])
        return obj


class BaseSerializer(ABC):
    """Base class for serializers"""

    def __init__(
        self,
        encoding: str = "utf-8",
        pretty: bool = False,
        datetime_handler: DateTimeSerializer = DefaultDateTimeHandler,
    ):
        self.encoding = encoding
        self.pretty = pretty
        self.datetime_handler = datetime_handler

    @abstractmethod
    def serialize(self, data: SerializableData) -> bytes:
        """Serialize data to bytes"""

    @abstractmethod
    def deserialize(self, data: bytes) -> SerializableData:
        """Deserialize data from bytes"""


class JsonSerializer(BaseSerializer):
    """JSON serializer implementation"""

    def serialize(self, data: SerializableData) -> bytes:
        """Serialize to JSON"""
        json_kwargs: dict[str, Any] = {
            "default": self.datetime_handler.serialize,
            "ensure_ascii": False,
            "check_circular": True,
            "allow_nan": True,
            "sort_keys": False,
            "separators": (",", ": ") if self.pretty else (",", ":"),
        }

        if self.pretty:
            json_kwargs["indent"] = 2

        return json.dumps(data, **json_kwargs).encode(self.encoding)

    def deserialize(self, data: bytes) -> SerializableData:
        """Deserialize from JSON"""
        return json.loads(
            data.decode(self.encoding),
            object_hook=self.datetime_handler.deserialize,
        )


class MsgPackSerializer(BaseSerializer):
    """MessagePack serializer implementation"""

    def serialize(self, data: SerializableData) -> bytes:
        """Serialize to MessagePack"""
        packed = msgpack.packb(
            data,
            default=self.datetime_handler.serialize,
            use_bin_type=True,
            strict_types=True,
        )
        if packed is None:
            raise ValueError("MessagePack serialization failed")
        return packed

    def deserialize(self, data: bytes) -> SerializableData:
        """Deserialize from MessagePack"""
        return msgpack.unpackb(data, object_hook=self.datetime_handler.deserialize, raw=False)


def create_serializer(
    format: str = "json",
    encoding: str = "utf-8",
    pretty: bool = False,
    datetime_handler: DateTimeSerializer | None = None,
) -> BaseSerializer:
    """Create serializer instance with given configuration"""
    serializers = {
        "json": JsonSerializer,
        "msgpack": MsgPackSerializer,
    }

    if format not in serializers:
        raise ValueError(f"Unsupported format: {format}")

    kwargs = {
        "encoding": encoding,
        "pretty": pretty,
    }

    if datetime_handler:
        kwargs["datetime_handler"] = datetime_handler

    return serializers[format](**kwargs)
