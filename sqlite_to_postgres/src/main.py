import os
import sqlite3
from contextlib import closing, contextmanager

import dotenv
import psycopg2
from psycopg2.extensions import connection as _connection
from psycopg2.extras import DictCursor

dotenv.load_dotenv()
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
