"""Contains utility functions used by sync and async code"""
from datetime import datetime
from typing import Iterable, Any, Optional, cast

from .const import ALL_STATE_CODES
from .model import Vacation


def parse_state_code(candidate: Any) -> str:
    """Parses the given candidate as a state code. Raises a ValueError
    when the candidate is not a valid state code."""
    state_code = str(candidate)
    if state_code not in ALL_STATE_CODES:
        raise ValueError("Argument state_code (current: '{}') is expected "
                         "to be one of {}".format(state_code, ALL_STATE_CODES))
    return state_code


def parse_year(candidate: Any) -> int:
    """Parses the given candidate as a year literal. Raises a ValueError
    when the candidate is not a valid year."""
    if candidate is not None and not isinstance(candidate, int):
        raise TypeError("Argument year is expected to be an int, "
                        "but is {}".format(type(candidate)))
    return cast(int, candidate)


def is_iterable_but_no_str(candidate: Any) -> bool:
    """Tests if the given candidate is an iterable (list, tuple, ...)
    but not a string."""
    return (
        hasattr(candidate, '__iter__')
        and not isinstance(candidate, (str, bytes))
    )


def check_vac_list(vacs: Iterable[Vacation]) -> None:
    """Checks if the given list is an actual list of vacations."""
    if not is_iterable_but_no_str(vacs):
        raise TypeError("Argument 'vacs' is expected to an iterable, "
                        "but is {}".format(type(vacs)))
    for i, val in enumerate(vacs):
        if not isinstance(val, Vacation):
            raise TypeError("Item {} of argument 'vacs' is expected to be of "
                            "type 'Vacation', but is {}".format(i, type(val)))


def check_datetime(dt: Any) -> None:
    """Checks if the argment dt is a valid datetime."""
    if dt and not isinstance(dt, datetime):
        raise TypeError("Argument 'dt' is expected to be of type 'datetime', "
                        "but is {}".format(type(dt)))


def find_current(vacs: Iterable[Vacation],
                 dt: Optional[datetime] = None) -> Optional[Vacation]:
    """Returns the current vacation based on the given dt.
    Returns None if no vacation surrounds (start, end) the
    given dt."""
    check_vac_list(vacs)
    check_datetime(dt)

    dt = dt or datetime.now()
    res = [i for i in vacs if i.start <= dt <= i.end][-1:]
    if not res:
        return None
    return res[0]


def find_next(vacs: Iterable[Vacation],
              dt: Optional[datetime] = None) -> Optional[Vacation]:
    """Returns the next vacation based on the given dt.
    Returns None if no vacation is left."""
    check_vac_list(vacs)
    check_datetime(dt)

    dt = dt or datetime.now()
    res = sorted([i for i in vacs if i.start >= dt], key=lambda i: i.start)
    if not res:
        return None
    return res[0]
