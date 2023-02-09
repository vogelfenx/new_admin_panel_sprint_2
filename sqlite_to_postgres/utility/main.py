import os
from contextlib import closing
from dataclasses import fields

import dotenv
from database.postgres.dataclasses import FilmWork
from database.postgres.postgres_db_handler import PostgresConnection
from database.sqlite.sqlite_db_handler import SQLiteConnection
from database.table_dataclasses import Table


def load_from_sqlite(sqlite_conn: SQLiteConnection, pg_conn: PostgresConnection, tables: dict):
    """Migrate data from sqlite to postgres databases.

    Args:
        sqlite_conn (SQLiteConnection): sqlite connection instance
        pg_conn (PostgresConnection): postgres connection instance
        chunk_size (_type_): size of rows to read/write in a bundle
    """

    for table, dataclass in tables.items():

        table_rows = sqlite_conn.extract_data(
            from_table=table,
        )

        formatted_rows = (pg_conn.remap_fields(dict(**row)) for row in table_rows)
        dataclass_objects = (dataclass(**row) for row in formatted_rows)

        dataclass_fields = tuple(field.name for field in fields(dataclass))
        table = Table(
            table_name=table,
            table_columns=dataclass_fields,
            dataclass_objects=dataclass_objects,
        )

        pg_conn.insert_data(table_metadata=table)


if __name__ == '__main__':
    dotenv.load_dotenv()

    database_tables = {
        'film_work': FilmWork,
        # 'person': Person,
        # 'person_film_work': PersonFilmWork,
        # 'genre': Genre,
        # 'genre_film_work': GenreFilmWork,
    }

    sqlite_dbname = os.getenv('SQLITE_DB_NAME')

    dsn_postgres = {
        'dbname': os.getenv('PG_DB_NAME'),
        'user': os.getenv('PG_USER'),
        'password': os.getenv('PG_PASSWORD'),
        'host': os.getenv('PG_HOST'),
        'port': os.getenv('PG_PORT'),
        'options': '-c search_path=content',
    }

    with closing(SQLiteConnection(sqlite_dbname, package_limit=1000)) as sqlite_conn:
        with closing(PostgresConnection(dsn_postgres)) as pg_conn:
            load_from_sqlite(sqlite_conn, pg_conn, tables=database_tables)
