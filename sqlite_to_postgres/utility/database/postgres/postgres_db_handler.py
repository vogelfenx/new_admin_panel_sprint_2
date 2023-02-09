from dataclasses import asdict

import psycopg2
from database.table_dataclasses import Table
from psycopg2.extras import DictCursor, execute_values
from util.logging import logging


class PostgresConnection:

    def __init__(self, dsn: dict):
        """Postgres database handler

        Args:
            dsn (dict): data source name for postgres connection
        """
        self.connection = psycopg2.connect(**dsn, cursor_factory=DictCursor)

        self.cursor = self.connection.cursor()
        self.offset = 0

    def close(self):
        self.connection.close()

    def insert_data(self, *, table: Table):
        """Insert rows to specified tables in target database.

        Args:
            table_rows (list): rows to be inserted
            table (Table): target database table object with references to data class objects
        """
        table_name = table.table_name
        table_columns = table.table_columns
        data_objects = table.dataclass_objects

        self._check_table_consistency(table_name=table_name)

        self._check_columns_consistency(columns=table_columns, table=table_name)

        table_columns = ', '.join(col for col in table_columns)
        table_values = ((list(asdict(data_row).values())) for data_row in data_objects)

        insert_query = f"""
        INSERT INTO {table_name} ({table_columns}) VALUES %s
        ON CONFLICT DO NOTHING;
        """

        try:
            execute_values(self.cursor, insert_query, table_values)
        except psycopg2.Error as error:
            logging.error('%s: %s', error.__class__.__name__, error)
            raise error

        self.connection.commit()

    def remap_fields(self, elem: dict) -> dict:
        if 'created_at' in elem.keys():
            elem['created'] = elem['created_at']
            del (elem['created_at'])

        if 'updated_at' in elem.keys():
            elem['modified'] = elem['updated_at']
            del (elem['updated_at'])

        if 'file_path' in elem.keys():
            del (elem['file_path'])

        return elem

    def _check_table_consistency(self, *, table_name):
        """Check if the given table exists.

        Args:
            table_name (str): name of the table to test

        Raises:
            OperationalError: Raise exception if table doesn't exist
        """
        sql_query = """
        SELECT EXISTS (
            SELECT FROM
            pg_tables
        WHERE
            tablename  = %s
        );
        """

        self.cursor.execute(sql_query, (table_name, ))
        is_table_exists = self.cursor.fetchone()[0]

        if not is_table_exists:
            raise psycopg2.OperationalError(f"table doesn't exist: {table_name}")

    def _check_columns_consistency(self, *, columns, table):
        """Check if the specified columns exist in the given table or not.

        Args:
            columns (list): columns to test
            table (str): the table to be searched in

        Raises:
            OperationalError: Raise if the columns doesn't match the columns in the table
        """
        sql_query = """
        SELECT
            column_name
        FROM
            information_schema.columns
        WHERE
            table_name = %s
        """

        self.cursor.execute(sql_query, (table, ))
        columns_in_table = self.cursor.fetchall()

        columns_in_table = [column[0] for column in columns_in_table]

        if not all(column in columns_in_table for column in columns):
            raise psycopg2.OperationalError(
                f"Columns [ {columns} ] do not match the columns [ {list(columns_in_table)} ] in the table [ '{table}' ].")
