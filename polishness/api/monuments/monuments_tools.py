import sqlite3
from typing import TypeVar, Optional
from types import MappingProxyType
from os.path import exists
from os import stat

import pandas as pd
import click

from polishness.api.monuments.monuments_constants import DEFAULT_MONUMENTS_DATABASE, DEFAULT_MONUMENTS_INPUT_FILE, DEF_SQLLITE_SCHEMA, \
    SQL_ZABYTKI_INSERT
from polishness.libs.sql.sqlite import get_db_connection, close_db
from polishness.utils import STATIC_DIR

SqliteConn = TypeVar("SqliteConn", bound="sqlite3.Connection")


DEFAULT_PATHS = MappingProxyType(
    {
        "db_location": f'{STATIC_DIR}{DEFAULT_MONUMENTS_DATABASE}',
        "input_file_location": f'{STATIC_DIR}{DEFAULT_MONUMENTS_INPUT_FILE}'
    }
)


def init_db(schema: Optional[str], location: Optional[str]):

    if location is None:
        location = DEFAULT_PATHS["db_location"]
    if exists(location) and bool(stat(location).st_size):
        raise FileExistsError("You re trying to override existing file. It is unaccepted... ")
    db = get_db_connection(location)

    if schema is None:
        db.executescript(DEF_SQLLITE_SCHEMA)
        return None

    with open(schema) as f:
        db.executescript(f.read())


def populate_db(data_file: Optional[str], location: Optional[str]) -> None:
    if location is None:
        location = DEFAULT_PATHS["db_location"]
    db = get_db_connection(location)
    if data_file is None:
        data_file = DEFAULT_PATHS["input_file_location"]
    df_data = pd.read_csv(data_file, dtype=object)
    df_size = len(df_data.index)
    c = db.cursor()
    for number in range(df_size):
        input_data = tuple(df_data.iloc[number])
        input_row = (df_data.index[number], *input_data)
        c.execute(SQL_ZABYTKI_INSERT, input_row)
    db.commit()
    close_db(db)


_help = MappingProxyType({
    "schema": "[optional] - absolute path to schema file (.sql) that will be used to create new Database.",
    "location": "[optional] - absolute path to Database file (.sqlite) that will be created.",
    "file": "[optional] - absolute path to file (.csv) that will act as input data for newly created Database."
})


@click.command('db-setup')
@click.option('-s', '--schema', required=False, help=_help["schema"], type=str)
@click.option('-l', '--location', required=False, help=_help["location"], type=str)
@click.option('-f', '--file', required=False, help=_help["file"], type=str)
def db_setup(schema: str, location: str, file: str):
    """Create new DB with zabytki table if not exists."""

    # By default 'click' makes: schema, location, file equal to None
    try:
        init_db(schema, location)
        populate_db(file, location)
    except sqlite3.IntegrityError:
        click.echo("Initialized the database. "
                   "But due to 'IntegrityError' data population failed.")
    else:
        click.echo("Initialized the database. Data were automatically loaded.")


if __name__ == "__main__":
    db_setup()
