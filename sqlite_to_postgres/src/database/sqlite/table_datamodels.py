import datetime
from dataclasses import dataclass

from database import BasicDataClass, GenreMixin, PersonMixin, UUIDMixin


@dataclass(frozen=True)
class TimestampMixin:
    created_at: datetime.time = None
    updated_at: datetime.time = None


@dataclass(frozen=True)
class Genre(TimestampMixin, GenreMixin, UUIDMixin, BasicDataClass):
    pass


@dataclass(frozen=True)
class Person(TimestampMixin, PersonMixin, UUIDMixin, BasicDataClass):
    pass
