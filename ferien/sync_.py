"""Synchronous implementation using requests."""

from .util import parse_state_code, parse_year, find_current, find_next
from .const import (ALL_STATE_CODES, API_ALL_URL,
                    API_STATE_URL, API_STATE_YEAR_URL)
from .model import Vacation


def _make_api_request(api_url):
    import requests
    resp = requests.get(api_url)
    if resp.status_code != 200:
        raise RuntimeError("ferien-api.de failed with http code = '{}'\n"
                           "Error: {}".format(resp.status_code, resp.text))
    return resp.json()


def _convert_json(resp):
    return [Vacation.from_dict(entry) for entry in resp]


def state_codes():
    """Returns all known and valid state codes."""
    import copy
    return copy.copy(ALL_STATE_CODES)


def all_vacations():
    """Makes a request to the ferien-api.de retrieving all
    vacations for all states at once"""
    return _convert_json(_make_api_request(API_ALL_URL))


def state_vacations(state_code, year=None):
    """Makes a request to the ferien-api.de using the given
    state_code and - optionally - the specified year."""
    state_code = parse_state_code(state_code)
    year = year and parse_year(year)

    if year is None:
        resp = _make_api_request(
            API_STATE_URL.format(state_code=state_code)
        )
    else:
        resp = _make_api_request(
            API_STATE_YEAR_URL.format(state_code=state_code, year=str(year))
        )

    return _convert_json(resp)


def current_vacation(state_code=None, vacs=None, dt=None):
    """Returns the current vacation based on the given dt.
    Returns None if no vacation surrounds (start, end) the
    given dt."""
    return _apply_fun(find_current, state_code, vacs, dt)


def next_vacation(state_code=None, vacs=None, dt=None):
    """Returns the next vacation based on the given dt.
    Returns None if no vacation is left."""
    return _apply_fun(find_next, state_code, vacs, dt)


def _apply_fun(fun, state_code=None, vacs=None, dt=None):
    assert fun is not None

    if vacs:
        return fun(vacs, dt)
    if state_code:
        return fun(state_vacations(state_code), dt)

    raise ValueError("You have to either specify argument 'state_code' "
                     "or argument 'vacs'")
