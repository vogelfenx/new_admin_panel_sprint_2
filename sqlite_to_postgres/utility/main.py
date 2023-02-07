import configparser
import os
from contextlib import closing

import dotenv

from database.postgres import PostgresConnection
from database.sqlite import SQLiteConnection
from database.table_dataclasses import TableMetadata


def load_from_sqlite(sqlite_conn: SQLiteConnection, pg_conn: PostgresConnection, chunk_size):
    """Migrate data from sqlite to postgres databases.

    Args:
        sqlite_conn (SQLiteConnection): sqlite connection instance
        pg_conn (PostgresConnection): postgres connection instance
        chunk_size (_type_): size of rows to read/write in a bundle
    """
    tables_from_config = (table for table in config.sections())

    tables_meta_sqlite = ()
    for table_name in tables_from_config:
        table_columns = dict(config.items(table_name))
        tables_meta_sqlite += (
            TableMetadata(
                table_name=table_name,
                source_db_columns=tuple(table_columns.keys()),
                target_db_columns=tuple(table_columns.values()),
            ),
        )

    for table_meta in tables_meta_sqlite:

        sqlite_conn.offset = 0

        is_table_fetch_empty = False
        while not is_table_fetch_empty:
            table_rows = sqlite_conn.extract_data(
                from_table=table_meta.table_name,
                columns=table_meta.source_db_columns,
                chunk_size=chunk_size,
            )

            if not table_rows:
                is_table_fetch_empty = True
                break

            pg_conn.insert_data(table_metadata=table_meta, table_rows=table_rows)


if __name__ == '__main__':
    dotenv.load_dotenv()

    config = configparser.ConfigParser()
    config.read('app.ini')

    dsn_sqlite = 'db.sqlite'
    dsn_postgres = {
        'dbname': os.getenv('PG_DB_NAME'),
        'user': os.getenv('PG_USER'),
        'password': os.getenv('PG_PASSWORD'),
        'host': os.getenv('PG_HOST'),
        'port': os.getenv('PG_PORT'),
        'options': '-c search_path=content',
    }

    with closing(SQLiteConnection(dsn_sqlite)) as sqlite_conn:
        with closing(PostgresConnection(dsn_postgres)) as pg_conn:
            load_from_sqlite(sqlite_conn, pg_conn, chunk_size=2000)
