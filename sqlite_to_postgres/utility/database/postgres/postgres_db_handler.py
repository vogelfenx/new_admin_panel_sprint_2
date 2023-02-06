import psycopg2
from psycopg2.extras import DictCursor
from database import TableMetadata


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

    def insert_data(self, *, table_metadata: TableMetadata, table_rows: list):
        """Insert rows to specified tables in target database.

        Args:
            table_metadata (TableMetadata): target database metadata
            table_rows (list): rows to be inserted
        """
        table_name = table_metadata.table_name
        table_columns = table_metadata.target_db_columns

        self._check_table_consistency(table_name=table_name)
        self._check_columns_consistency(columns=table_columns, table=table_name)

        column_names = ','.join(table_columns)

        columns_count = len(table_columns)
        parameter_placeholders = ['%s' for _ in range(columns_count)]
        parameter_placeholders = ','.join(parameter_placeholders)

        column_values = ()
        for table_row in table_rows:
            column_values += ((self.cursor.mogrify(f'({parameter_placeholders})', table_row).decode()),)
        column_values = ','.join(column_values)

        sql_query = f"""
        INSERT INTO {table_name} ({column_names})
        VALUES {column_values}
        ON CONFLICT (id) DO NOTHING
        """
        self.cursor.execute(sql_query)
        self.connection.commit()

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
