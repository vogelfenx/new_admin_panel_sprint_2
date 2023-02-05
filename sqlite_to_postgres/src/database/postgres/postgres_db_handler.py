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
