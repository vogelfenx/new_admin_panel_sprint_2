import os
import sqlite3
from contextlib import closing

import dotenv
import psycopg2
from psycopg2.extensions import connection as _connection
from psycopg2.extras import DictCursor

from database import sqlite
from database.sqlite import SQLiteExtractor
from database.table_dataclasses import TableMetadata
import configparser


def load_from_sqlite(sqlite_conn: SQLiteConnection, pg_conn: PostgresConnection, chunk_size):
    """Основной метод загрузки данных из SQLite в Postgres."""

    tables_meta_sqlite = {
        TableMetadata('person', sqlite.Person.get_fields(), sqlite.Person),
        # TableMetadata('genre', sqlite.Genre.get_fields(), sqlite.Genre),
    }

    for table_meta in tables_meta_sqlite:

        is_table_fetch_empty = False
        while not is_table_fetch_empty:
            dataclass_objects = ()
            table_data = sqlite_extractor.extract_data(
                from_table=table_meta.table_name, columns=table_meta.columns, chunk_size=chunk_size,
            )
            if not table_data:
                is_table_fetch_empty = True
                break

            # dataclass_objects = ()
            for row_data in table_data:
                dataclass_object = table_meta.data_class(**row_data)
                dataclass_objects += (dataclass_object, )

            print([i.full_name for i in dataclass_objects])
            # breakpoint()

            #############
            # postgres_saver.save_all_data(data)
            #############

        # print(f'Table {dataclass_objects[0].__class__} has {len(dataclass_objects)} records')
if __name__ == '__main__':
    dotenv.load_dotenv()

    config = configparser.ConfigParser()
    config.read('app.ini')

    dsn_sqlite = 'db.sqlite'
    dsn_postgres = {
        'dbname': 'movies_database',
        'user': os.getenv('PG_USER'),
        'password': os.getenv('PG_PASSWORD'),
        'host': os.getenv('PG_HOST'),
        'port': os.getenv('PG_PORT'),
        'options': '-c search_path=content',
    }

    with closing(SQLiteConnection(dsn_sqlite)) as sqlite_conn:
        with closing(PostgresConnection(dsn_postgres)) as pg_conn:
            load_from_sqlite(sqlite_conn, pg_conn, chunk_size=2000)
