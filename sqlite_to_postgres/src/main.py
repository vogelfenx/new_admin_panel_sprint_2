import os
import sqlite3
from contextlib import closing, contextmanager

import dotenv
import psycopg2
from psycopg2.extensions import connection as _connection
from psycopg2.extras import DictCursor

from sqlite_db_handler import SQLiteExtractor

dotenv.load_dotenv()


def load_from_sqlite(sqlite_conn: sqlite3.Connection, pg_conn: _connection):
    """Основной метод загрузки данных из SQLite в Postgres."""
    sqlite_extractor = SQLiteExtractor(sqlite_conn)
    # postgres_saver = PostgresSaver(pg_conn)

    data = sqlite_extractor.extract_data(from_table='genre',
                                         columns=(
                                             'id',
                                             'name',
                                             'description',
                                             'created_at',
                                             'updated_at',
                                         ))
    # postgres_saver.save_all_data(data)


if __name__ == '__main__':
    dsn_postgres = {
        'dbname': 'movies_database',
        'user': os.getenv('PG_USER'),
        'password': os.getenv('PG_PASSWORD'),
        'host': os.getenv('PG_HOST'),
        'port': os.getenv('PG_PORT'),
        'options': '-c search_path=content',
    }
    dsn_sqlite = 'db.sqlite'

    with closing(sqlite3.connect(dsn_sqlite)) as sqlite_conn:
        with closing(psycopg2.connect(**dsn_postgres, cursor_factory=DictCursor)) as pg_conn:
            load_from_sqlite(sqlite_conn, pg_conn)
            pass
