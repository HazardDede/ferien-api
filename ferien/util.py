"""Contains utility functions used by sync and async code"""

from .const import ALL_STATE_CODES


def parse_state_code(candidate):
    state_code = str(candidate)
    if state_code not in ALL_STATE_CODES:
        raise ValueError("Argument state_code (current: '{}') is expected "
                         "to be one of {}".format(state_code, ALL_STATE_CODES))
    return state_code


def parse_year(candidate):
    if candidate is not None and not isinstance(candidate, int):
        raise TypeError("Argument year is expected to be an int, "
                        "but is {}".format(type(candidate)))
    return candidate
