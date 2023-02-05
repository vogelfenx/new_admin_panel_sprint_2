import psycopg2
from psycopg2.extras import DictCursor
from dataclasses import asdict, astuple


class PostgresConnection:

    def __init__(self, dsn: dict):
        self.connection = psycopg2.connect(**dsn, cursor_factory=DictCursor)

        self.cursor = self.connection.cursor()
        self.offset = 0

    def close(self):
        self.connection.close()

    def insert_data(self, *, table_metadata, table_rows):
        table_name = table_metadata.table_name
        column_names = ','.join(table_metadata.target_db_columns)

        columns_count = len(table_metadata.target_db_columns)
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
