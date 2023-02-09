import os
import sqlite3
import unittest

import dotenv
import psycopg2

from utility.database.sqlite.util import convert_datetime

dotenv.load_dotenv()


class TestDatabaseConsistency(unittest.TestCase):
    """Tests for database consistency."""

    def setUp(self):
        """Prepare test environment."""
        dsn_sqlite = 'db.sqlite'
        dsn_postgres = {
            'dbname': 'movies_database',
            'user': os.getenv('PG_USER'),
            'password': os.getenv('PG_PASSWORD'),
            'host': os.getenv('PG_HOST'),
            'port': os.getenv('PG_PORT'),
            'options': '-c search_path=content',
        }

        self.postgres_connection = psycopg2.connect(**dsn_postgres)
        self.postgres_cursor = self.postgres_connection.cursor()

        sqlite3.register_converter('timestamp', convert_datetime)
        self.sqlite_connection = sqlite3.connect(dsn_sqlite, detect_types=sqlite3.PARSE_DECLTYPES)
        self.sqlite_cursor = self.sqlite_connection.cursor()

        self.tables = ('film_work', 'person', 'genre', 'person_film_work', 'genre_film_work')

    def tearDown(self):
        """Cleanup test environment."""
        self.sqlite_connection.close()
        self.postgres_connection.close()

    def test_tables_rows_count(self):
        """Test table rows count between source and target databases."""
        select_count_query = 'SELECT COUNT(*) FROM {table}'
        for table in self.tables:

            self.sqlite_cursor.execute(select_count_query.format(table=table))
            rows_count_sqlite = self.sqlite_cursor.fetchone()[0]

            self.postgres_cursor.execute(select_count_query.format(table=table))
            rows_count_postgres = self.postgres_cursor.fetchone()[0]
            self.assertEqual(rows_count_sqlite, rows_count_postgres)

    def test_tables_data_consistency(self):
        """Test data consistency between source and target databases."""
        select_query = """
        SELECT
            *
        FROM
            {table}
        ORDER BY
            id ASC
        """
        for table in self.tables:
            self.sqlite_cursor.execute(select_query.format(table=table))

            rows_data_sqlite = self.sqlite_cursor.fetchall()

            self.postgres_cursor.execute(select_query.format(table=table))

            rows_data_postgres = self.postgres_cursor.fetchall()

            rows_data_sqlite = self._remove_empty_or_none_list_items(rows_data_sqlite)
            rows_data_postgres = self._remove_empty_or_none_list_items(rows_data_postgres)

            sorted_rows_sqlite = [sorted((str(col) for col in row)) for row in rows_data_sqlite]
            sorted_rows_postgres = [sorted((str(col) for col in row)) for row in rows_data_postgres]

            self.assertListEqual(sorted(sorted_rows_sqlite), sorted(sorted_rows_postgres))

    def _remove_empty_or_none_list_items(self, items: list) -> list:
        cleaned_items = [
            tuple(elem for elem in elements if (elem is not None) and (elem != ''))
            for elements in items
        ]
        return cleaned_items
