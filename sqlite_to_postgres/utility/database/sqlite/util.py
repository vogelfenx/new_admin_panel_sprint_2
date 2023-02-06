import iso8601
import datetime


def convert_datetime(date):
    """Convert ISO 8601 datetime to datetime.datetime object."""
    return iso8601.parse_date(date.decode())
