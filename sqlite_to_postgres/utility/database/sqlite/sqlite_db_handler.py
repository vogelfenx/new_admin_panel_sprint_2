import sqlite3


class SQLiteConnection:
    """SQLiteExtractor."""

    def __init__(self, dsn: str):
        """Sqlite database handler.

        Args:
            dsn (str): sqlite database name
        """
        self.connection = sqlite3.connect(dsn)

        self.cursor = self.connection.cursor()
        self.offset = 0

    def close(self):
        """Close database connection."""
        self.connection.close()

    def extract_data(self, *, from_table: str, columns: list, chunk_size: int) -> list:
        """Read rows from the given table by the given chunk_size.

        Args:
            from_table (_type_): source table
            columns (_type_): table columns to select
            chunk_size (_type_): number of rows to read in a bundle

        Returns:
            list: rows of data limited by the size of the chunk
        """
        chunk_size = int(chunk_size)

        self._check_table_consistency(table_name=from_table)

        self._check_columns_consistency(columns=columns, table=from_table)

        cursor = self.cursor

        columns = ','.join(columns)
        cursor.execute(f'SELECT {columns} FROM {from_table} LIMIT {chunk_size} OFFSET {self.offset}')
        self.offset += chunk_size

        fetched_rows = cursor.fetchall()

        return fetched_rows

    def _check_table_consistency(self, *, table_name: str):
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
            raise sqlite3.OperationalError(f"table doesn't exist: {table_name}")

    def _check_columns_consistency(self, *, columns: list, table: str):
        """Check if the specified columns exist in the given table or not.

        Args:
            columns (list): columns to test
            table (str): the table to be searched in

        Raises:
            OperationalError: Raise if the columns doesn't match the columns in the table
        """
        sql_query = """
        SELECT name FROM pragma_table_info(?);
        """
        self.cursor.execute(sql_query, (table, ))
        columns_in_table = self.cursor.fetchall()

        columns_in_table = [column[0] for column in columns_in_table]

        if not all(column in columns_in_table for column in columns):
            raise sqlite3.OperationalError(
                f"Columns [ {columns} ] do not match the columns [ {list(columns_in_table)} ] in the table [ '{table}' ].")
