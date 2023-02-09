from dataclasses import dataclass
from typing import Iterator


@dataclass(frozen=True)
class Table:
    """Store database table information and data object references."""

    table_name: str
    table_columns: tuple[str]
    dataclass_objects: Iterator[object]
