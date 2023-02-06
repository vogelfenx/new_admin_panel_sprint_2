from dataclasses import dataclass


@dataclass(frozen=True)
class TableMetadata:
    """Store database table metadata."""

    table_name: str
    source_db_columns: tuple[str]
    target_db_columns: tuple[str]
