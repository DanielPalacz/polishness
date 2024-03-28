""" (c) YYYY Copyright WHO """
from sqlite3 import OperationalError
from typing import Union

from flask import Blueprint
from flask import render_template

from polishness.api.monuments.monuments_api_utils import get_query_params, search_monuments, generate_trip

monuments_bp = Blueprint(
    "monuments",
    __name__
)


@monuments_bp.route('/wyszukaj/')
def wyszukaj():
    query_params = get_query_params()
    city, parish, county, keyword, voivodeship, quantity = query_params.values()

    if not any([city, parish, county, keyword, voivodeship]):
        return render_template('search_main.html')

    params = [": ".join(x) for x in
              [
                  ["miejscowość", city], ["gmina", parish], ["powiat", county],
                  ["klucz", keyword], ["wojewodztwo", voivodeship], ["quantity", quantity]] if x[1]
              ]
    try:
        items = search_monuments(**query_params)
    except OperationalError:
        return "Problem po stronie aplikacji. Właśnie powiadomiono administratora o zdarzeniu.", 200

    _items = [tuple([elem if elem is not None else "" for elem in t_elem]) for t_elem in items]

    return render_template("search.html", city=city, params=params, items=_items, quantity=len(items))


@monuments_bp.route('/wycieczka/')
def wycieczka():
    query_params = get_query_params()
    city, parish, county, keyword, voivodeship, quantity = query_params.values()

    print("1 - wycieczka_endpoint")

    if not any([city, parish, county, keyword, voivodeship]):
        return render_template('generate_main.html')

    print("2 - wycieczka_endpoint")

    params = [": ".join(x) for x in
              [
                  ["miejscowość", city], ["gmina", parish], ["powiat", county],
                  ["klucz", keyword], ["wojewodztwo", voivodeship], ["quantity", quantity]] if x[1]
              ]
    try:
        items = generate_trip(**query_params)
    except OperationalError:
        return "Problem po stronie aplikacji. Właśnie powiadomiono administratora o zdarzeniu.", 200


    #
    print(params)
    print("3 - wycieczka_endpoint")

    return render_template("search.html", city=city, params=params, items=items, quantity=len(items))


def __wyszukaj() -> Union[list[tuple], str, tuple]:
    query_params = get_query_params()
    city, parish, county, keyword, voivodeship, quantity = query_params.values()

    if not any([city, parish, county, keyword, voivodeship]):
        return render_template('search_main.html')

    params = [": ".join(x) for x in
              [
                  ["miejscowość", city], ["gmina", parish], ["powiat", county],
                  ["klucz", keyword], ["wojewodztwo", voivodeship], ["quantity", quantity]] if x[1]
              ]
    try:
        items = search_monuments(**query_params)
    except OperationalError:
        return "Problem po stronie aplikacji. Właśnie powiadomiono administratora o zdarzeniu.", 200
