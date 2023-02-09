import uuid
from dataclasses import dataclass, field
from datetime import date, datetime


@dataclass(frozen=True)
class MixinId:
    """Dataclass Mixin to extend dataclasses with id."""

    id: uuid.UUID


@dataclass(frozen=True)
class MixinDate:
    """Dataclass Mixin to extend dataclasses with date."""

    created: datetime
    modified: datetime


@dataclass(frozen=True)
class FilmWork(MixinId, MixinDate):
    """Dataclass for table FilmWork in postgres schema."""

    title: str
    creation_date: date
    certificate_file_path: str = field(default='')
    description: str = field(default='')
    rating: float = field(default=0)
    type: str = field(default='')


@dataclass(frozen=True)
class Person(MixinId, MixinDate):
    """Dataclass for table Person in postgres schema."""

    full_name: str
    gender: str = field(default='')


@dataclass(frozen=True)
class Genre(MixinId, MixinDate):
    """Dataclass for table Genre in postgres schema."""

    name: str
    description: str = field(default='')


@dataclass(frozen=True)
class PersonFilmWork(MixinId):
    """Dataclass for table PersonFilmWork in postgres schema."""

    film_work_id: uuid
    person_id: uuid
    created: datetime
    role: str = field(default='')
