import configparser
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

        self.config = configparser.ConfigParser()
        self.config.read('app.ini')
        self.tables = tuple(table.replace(' ', '') for table in self.config.sections())

    def tearDown(self):
        """Cleanup test environment."""
        self.sqlite_connection.close()
        self.postgres_connection.close()

    def test_table_rows_count(self):
        """Test table rows count between source and target databases."""
        for table in self.tables:
            sql_query = f'SELECT COUNT(*) FROM {table}'

            self.sqlite_cursor.execute(sql_query)
            rows_count_sqlite = self.sqlite_cursor.fetchone()[0]

            self.postgres_cursor.execute(sql_query)
            rows_count_postgres = self.postgres_cursor.fetchone()[0]
            self.assertEqual(rows_count_sqlite, rows_count_postgres)

    def test_table_data_consistency(self):
        """Test data consistency between source and target databases."""
        for table in self.tables:
            column_names_mapping = dict(self.config.items(table))
            column_names_sqlite = ','.join(column_names_mapping.keys())
            column_names_postgres = ','.join(column_names_mapping.values())

            self.sqlite_cursor.execute(
                f"""
                SELECT
                    {column_names_sqlite}
                FROM 
                    {table}
                ORDER BY
                    id ASC
                """)

            rows_data_sqlite = self.sqlite_cursor.fetchall()

            self.postgres_cursor.execute(
                f"""
                SELECT
                    {column_names_postgres}
                FROM 
                    {table}
                ORDER BY
                    id ASC
                """)

            rows_data_postgres = self.postgres_cursor.fetchall()

            self.assertListEqual(rows_data_sqlite, rows_data_postgres)


if __name__ == '__main__':
    unittest.main()
