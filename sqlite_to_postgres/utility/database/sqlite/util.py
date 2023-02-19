from datetime import datetime

import iso8601


def convert_datetime(date: bytes):
    """Convert ISO 8601 datetime to datetime.datetime object.

    Args:
        date (bytes): date to convert

    Returns:
        datetime: datetime.datetime object
    """
    return iso8601.parse_date(date.decode())
