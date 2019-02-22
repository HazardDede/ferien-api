from unittest.mock import patch

import pytest

import ferien.client as dut
from ferien.const import ALL_STATE_CODES
from ferien.model import Vacation


DUMMY_RESP = [
    {
      "start": "2017-01-29T23:00",
      "end": "2017-01-31T23:00",
      "year": 2017,
      "stateCode": "HB",
      "name": "winterferien",
      "slug": "winterferien-2017-HB"
    },
    {
      "start": "2017-04-09T22:00",
      "end": "2017-04-22T22:00",
      "year": 2017,
      "stateCode": "HB",
      "name": "osterferien",
      "slug": "osterferien-2017-HB"
    }
]


EXPECTED = [Vacation.from_dict(entry) for entry in DUMMY_RESP]


def _configure_mock(m, status_code=200, response=DUMMY_RESP):
    m.return_value.status_code = status_code
    m.return_value.json.return_value = response
    m.return_value.text = response
    return m


def test_state_codes():
    assert dut.state_codes() == ALL_STATE_CODES


@patch('requests.get')
def test_get_all_vacations(mock_requests):
    _configure_mock(mock_requests)

    res = dut.all_vacations()
    assert res == EXPECTED


@patch('requests.get')
def test_get_all_vacations_bad_status_code(mock_requests):
    _configure_mock(mock_requests, 500, response="Not a teapot")

    with pytest.raises(RuntimeError) as e:
        dut.all_vacations()
    assert "RuntimeError: ferien-api.de failed with http code = '500'" in str(e)


@patch('requests.get')
def test_get_state_vacations_by_state(mock_requests):
    _configure_mock(mock_requests)

    res = dut.state_vacations('HB')
    assert res == EXPECTED


@patch('requests.get')
def test_get_state_vacations_by_state_year(mock_requests):
    _configure_mock(mock_requests)

    res = dut.state_vacations('HB', 2017)
    assert res == EXPECTED


def test_get_state_vacations_unknown_state():
    with pytest.raises(ValueError) as e:
        dut.state_vacations('UKW')
    assert "ValueError: Argument state_code (current: 'UKW') is expected to be one of " in str(e)


def test_get_state_vacations_with_bad_year():
    with pytest.raises(TypeError) as e:
        dut.state_vacations('HH', 'abc')
    assert "TypeError: Argument year is expected to be an int, but is <class 'str'>" in str(e)
