import sqlite3
from collections.abc import Iterator

from util.logging import logging


class SQLiteConnection:
    """SQLiteExtractor."""

    def __init__(self, dsn: str, package_limit: int):
        """SQLite database handler.

        Args:
            dsn (str): SQLite database name
            package_limit (int): rows count to be read by fetchmany
        """
        self.connection = sqlite3.connect(dsn)
        self.connection.row_factory = sqlite3.Row
        self.cursor = self.connection.cursor()

        self.package_limit = package_limit

    def close(self):
        """Close database connection."""
        self.connection.close()

    def extract_data(self, *, from_table: str) -> Iterator[sqlite3.Row]:
        """Read rows from the given table.

        Args:
            from_table (str): source table

        Raises:
            error: an sqlite3.Error on table

        Yields:
            Iterator[sqlite3.Row]: fetched data rows
        """
        self._validate_table(table_name=from_table)

        cursor = self.cursor

        try:
            cursor.execute(f'SELECT * FROM {from_table}')
        except sqlite3.Error as error:
            logging.error('sqlite3.Error: %s', error.args)
            raise error

        while True:
            rows = cursor.fetchmany(size=self.package_limit)
            if not rows:
                return
            yield from rows

    def _validate_table(self, *, table_name: str):
        """Check if the given table exists.

        Args:
            table_name (str): name of the table to test

        Raises:
            OperationalError: Raise exception if table doesn't exist
        """
        sql_query = """
        SELECT
            name
        FROM
            sqlite_master
        WHERE
            type = 'table'
            AND name = ?
            LIMIT 1;
        """

        self.cursor.execute(sql_query, (table_name, ))
        is_table_exists = self.cursor.fetchone() is not None

        if not is_table_exists:
            error_message = f"table doesn't exist: {table_name}"
            logging.error('sqlite3.OperationalError: %s', error_message)
            raise sqlite3.OperationalError(error_message)
