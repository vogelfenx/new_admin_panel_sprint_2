import uuid
from abc import ABC
from dataclasses import dataclass


@dataclass(frozen=True)
class TableMetadata:
    """Store database table metadata."""

    table_name: str
    source_db_columns: tuple[str, list]
    target_db_columns: tuple[str, list]


@dataclass(frozen=True)
class BasicDataClass(ABC):

    @classmethod
    def get_fields(cls):
        return tuple(cls.__dataclass_fields__.keys())


@dataclass(frozen=True)
class UUIDMixin(ABC):
    id: uuid.UUID


@dataclass(frozen=True)
class GenreMixin(ABC):
    name: str = None
    description: str = None


@dataclass(frozen=True)
class PersonMixin(ABC):
    full_name: str = None
