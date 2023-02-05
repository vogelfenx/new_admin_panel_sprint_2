import sqlite3


class SQLiteConnection:
    """SQLiteExtractor."""

    def __init__(self, dsn: dict):
        """_summary_.

        Args:
            connection (sqlite3.Connection): _description_
        """
        self.connection = sqlite3.connect(dsn)
        # self.connection.row_factory = sqlite3.Row

        self.cursor = self.connection.cursor()
        self.offset = 0

    def close(self):
        self.connection.close()

    def extract_data(self, *, from_table, columns, chunk_size):
        chunk_size = int(chunk_size)

        self._check_table_consistency(table_name=from_table)

        self._check_columns_consistency(columns=columns, table=from_table)

        cursor = self.cursor

        columns = ','.join(columns)
        cursor.execute(f'SELECT {columns} FROM {from_table} LIMIT {chunk_size} OFFSET {self.offset}')
        self.offset += chunk_size

        fetched_rows = cursor.fetchall()

        return (fetched_rows)

    def _check_table_consistency(self, *, table_name):
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

    def _check_columns_consistency(self, *, columns, table):
        sql_query = """
        SELECT name FROM pragma_table_info(?);
        """
        self.cursor.execute(sql_query, (table, ))
        columns_in_table = self.cursor.fetchall()

        columns_in_table = (column[0] for column in columns_in_table)

        if not all(column in columns_in_table for column in columns):
            raise sqlite3.OperationalError('Columns do not match the columns in the table.')
