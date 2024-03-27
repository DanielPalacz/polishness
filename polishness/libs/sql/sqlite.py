import sqlite3
from typing import TypeVar
from contextlib import contextmanager


SqliteConn = TypeVar("SqliteConn", bound="sqlite3.Connection")


def get_db_connection(location: str) -> SqliteConn:

    db_conn = sqlite3.connect(
        location,
        detect_types=sqlite3.PARSE_DECLTYPES
    )
    db_conn.row_factory = sqlite3.Row
    return db_conn


def close_db(db_conn):
    db_conn.close()


@contextmanager
def open_sqlite(location: str):

    db_conn = sqlite3.connect(
        location,
        detect_types=sqlite3.PARSE_DECLTYPES
    )
    try:
        yield db_conn
    finally:
        close_db(db_conn)
