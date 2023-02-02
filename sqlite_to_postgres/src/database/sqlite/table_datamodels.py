import datetime
from dataclasses import dataclass

from database import GenreMixin, PersonMixin, TableMetadata, UUIDMixin


@dataclass(frozen=True)
class TimestampMixin:
    created_at: datetime.time = None
    updated_at: datetime.time = None


@dataclass(frozen=True)
class Genre(TimestampMixin, GenreMixin, UUIDMixin):
    pass


@dataclass(frozen=True)
class Person(TimestampMixin, PersonMixin, UUIDMixin):
    pass
