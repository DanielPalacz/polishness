
DEFAULT_MONUMENTS_DATABASE = "monuments.sqlite"
"""Default Database name."""

DEFAULT_MONUMENTS_INPUT_FILE = "monuments.csv"
"""Default input file name."""


DEF_SQLLITE_SCHEMA = """CREATE TABLE IF NOT EXISTS zabytki (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  inspire_id TEXT NOT NULL,
  forma_ochrony TEXT NOT NULL,
  dokladnosc_polozenia TEXT NOT NULL,
  nazwa TEXT NOT NULL,
  chronologia TEXT,
  funkcja TEXT NOT NULL,
  wykaz_dokumentow TEXT NOT NULL,
  data_wpisu TEXT NOT NULL,
  wojewodztwo TEXT NOT NULL,
  powiat TEXT NOT NULL,
  gmina TEXT NOT NULL,
  miejscowosc TEXT NOT NULL,
  ulica TEXT ,
  nr_adresowy TEXT,
  szerokosc_geogr TEXT,
  dlugosc_geogr TEXT
);
"""


SQL_ZABYTKI_INSERT = "INSERT INTO zabytki VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)"


ZABYTKI_INFO = (
 "id",
 "inspire_id",
 "forma_ochrony",
 "dokladnosc_polozenia",
 "nazwa",
 "chronologia",
 "funkcja",
 "wykaz_dokumentow",
 "data_wpisu",
 "wojewodztwo",
 "powiat",
 "gmina",
 "miejscowosc",
 "ulica",
 "nr_adresowy",
 "szerokosc_geogr",
 "dlugosc_geogr"
)
