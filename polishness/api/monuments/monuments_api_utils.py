from marshmallow import Schema, fields as marshmallow_fields
from flask import request
from flask import current_app

from polishness.api.monuments.monuments_constants import DEFAULT_MONUMENTS_DATABASE
from polishness.libs.sql.sqlite import open_sqlite


def search_monuments(city: str = "", parish: str = "", county: str = "", keyword="", voivodeship="", quantity=None) -> list[tuple]:
    print("generate_trip 1...")

    with current_app.app_context():
        db_location = current_app.static_folder + '/' + DEFAULT_MONUMENTS_DATABASE

    with (open_sqlite(db_location) as db_conn):
        sql_query = _create_search_sql_query(
            city=city, parish=parish, county=county, keyword=keyword, voivodeship=voivodeship, rownum=quantity)
        output = db_conn.execute(sql_query).fetchall()
        return [tuple([id_temp + 1]) + tuple(item) for id_temp, item in enumerate(output)]


def generate_trip(city: str = "", parish: str = "", county: str = "", keyword="", voivodeship="", quantity=None) -> list[tuple]:

    print("generate_trip ...")

    with current_app.app_context():
        db_location = current_app.static_folder + '/' + DEFAULT_MONUMENTS_DATABASE

    with (open_sqlite(db_location) as db_conn):
        sql_query = _create_trip_gen_sql_query(
            city=city, parish=parish, county=county, keyword=keyword, voivodeship=voivodeship, rownum=quantity)
        output = db_conn.execute(sql_query).fetchall()

        monuments = [tuple([id_temp + 1]) + tuple(item) for id_temp, item in enumerate(output)]

    print("_create_trip_gen_sql_query")
    return monuments


def _create_search_sql_query(*, city="", parish="", county="", keyword="", voivodeship="", rownum=10) -> str:
    if city or parish or county or keyword or voivodeship:
        sql_query = "SELECT * from zabytki where"
    else:
        return ""
    if city:
        sql_query += " miejscowosc='" + city + "'" + "COLLATE NOCASE"
    if parish:
        if city:
            sql_query += " and"
        sql_query += " gmina like '%" + parish + "%'"
    if county:
        if city or parish:
            sql_query += " and"
        sql_query += " powiat='" + county + "'"
    if voivodeship:
        if city or parish or county:
            sql_query += " and"
        sql_query += " wojewodztwo='" + voivodeship + "'"
    if keyword:
        if city or parish or county or voivodeship:
            sql_query += " and"
        sql_query += " ( nazwa like '%" + keyword + "%'" + " or funkcja like '%" + keyword + "%'" \
                     " or wojewodztwo like '%" + keyword + "%'" + " or chronologia like '%" + keyword + "%'" \
                     " or ulica like '%" + keyword + "%' )"

    sql_query += f" limit {rownum}"

    # TODO Sortowanie należałoby dopiero zdefiniować:
    # sql_query += " order by powiat, gmina, miejscowosc, ulica"

    return sql_query


def _create_trip_gen_sql_query(*, city="", parish="", county="", keyword="", voivodeship="", rownum=10) -> str:
    if city or parish or county or keyword or voivodeship:
        sql_query = "SELECT * from zabytki where"
    else:
        return ""

    if city:
        sql_query += " miejscowosc='" + city + "'" + "COLLATE NOCASE"
    if parish:
        if city:
            sql_query += " and"
        sql_query += " gmina like '%" + parish + "%'"
    if county:
        if city or parish:
            sql_query += " and"
        sql_query += " powiat='" + county + "'"
    if voivodeship:
        if city or parish or county:
            sql_query += " and"
        sql_query += " wojewodztwo='" + voivodeship + "'"

    if keyword:
        if city or parish or county or voivodeship:
            sql_query += " and"
        sql_query += " ( nazwa like '%" + keyword + "%'" + " or funkcja like '%" + keyword + "%'" \
                     " or wojewodztwo like '%" + keyword + "%'" + " or chronologia like '%" + keyword + "%'" \
                     " or ulica like '%" + keyword + "%' )"

    # sql_query += f" and nr_adresowy is not NULL limit {rownum}"
    sql_query += f" and szerokosc_geogr is not NULL and dlugosc_geogr is not NULL and nr_adresowy is not NULL limit {rownum}"

    return sql_query


def get_query_params() -> dict:
    city = request.args.get("miasto", "").replace("'", "")
    parish = request.args.get("gmina", "").replace("'", "")
    county = request.args.get("powiat", "").replace("'", "")
    voivodeship = request.args.get("wojewodztwo", "").replace("'", "")
    keyword = request.args.get("dowolneslowo", "").replace("'", "")
    quantity = request.args.get("quantity", "").replace("'", "")
    return {
        "city": city,
        "parish": parish,
        "county": county,
        "keyword": keyword,
        "voivodeship": voivodeship,
        "quantity": quantity,
    }


class MonumentInfoSchema(Schema):

    identifier = marshmallow_fields.Integer()
    name = marshmallow_fields.String()          # park dworski
    chronology = marshmallow_fields.String()    # np. XIX w.
    function = marshmallow_fields.String()      # np. park
    voivodeship = marshmallow_fields.String()   # województwo
    county = marshmallow_fields.String()        # powiat
    parish = marshmallow_fields.String()        # gmina
    locality = marshmallow_fields.String()      # miejscowość
    address = marshmallow_fields.String()       # ulica + nr domu, lub puste


class MonumentsSearchResponse:

    # noinspection PyTypeChecker
    data = marshmallow_fields.Nested(MonumentInfoSchema)
