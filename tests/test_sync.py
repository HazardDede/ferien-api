from datetime import datetime
from unittest.mock import patch

import pytest

import ferien.sync_ as dut
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


@patch('requests.get')
def test_current_vacation(mock_requests):
    _configure_mock(mock_requests)

    res = dut.current_vacation(vacs=EXPECTED, dt=datetime.strptime('2017-01-30', '%Y-%m-%d'))
    assert res == EXPECTED[0]
    res = dut.current_vacation(vacs=EXPECTED, dt=datetime.strptime('2017-04-22', '%Y-%m-%d'))
    assert res == EXPECTED[1]
    res = dut.current_vacation(vacs=EXPECTED, dt=datetime.strptime('2017-01-01', '%Y-%m-%d'))
    assert res is None

    res = dut.current_vacation(state_code='HB', dt=datetime.strptime('2017-01-30', '%Y-%m-%d'))
    assert res == EXPECTED[0]
    res = dut.current_vacation(state_code='HB', dt=datetime.strptime('2017-04-22', '%Y-%m-%d'))
    assert res == EXPECTED[1]
    res = dut.current_vacation(state_code='HB', dt=datetime.strptime('2017-01-01', '%Y-%m-%d'))
    assert res is None


def test_current_vacation_arguments_fail():
    with pytest.raises(ValueError) as e:
        dut.current_vacation()
    assert "ValueError: You have to either specify argument 'state_code' or argument 'vacs'" in str(e)


@patch('requests.get')
def test_next_vacation(mock_requests):
    _configure_mock(mock_requests)

    res = dut.next_vacation(vacs=EXPECTED, dt=datetime.strptime('2017-01-29', '%Y-%m-%d'))
    assert res == EXPECTED[0]
    res = dut.next_vacation(vacs=EXPECTED, dt=datetime.strptime('2017-02-01', '%Y-%m-%d'))
    assert res == EXPECTED[1]
    res = dut.next_vacation(vacs=EXPECTED, dt=datetime.strptime('2017-05-01', '%Y-%m-%d'))
    assert res is None

    res = dut.next_vacation(state_code='HB', dt=datetime.strptime('2017-01-29', '%Y-%m-%d'))
    assert res == EXPECTED[0]
    res = dut.next_vacation(state_code='HB', dt=datetime.strptime('2017-02-01', '%Y-%m-%d'))
    assert res == EXPECTED[1]
    res = dut.next_vacation(state_code='HB', dt=datetime.strptime('2017-05-01', '%Y-%m-%d'))
    assert res is None


def test_next_vacation_arguments_fail():
    with pytest.raises(ValueError) as e:
        dut.next_vacation()
    assert "ValueError: You have to either specify argument 'state_code' or argument 'vacs'" in str(e)

    with pytest.raises(TypeError) as e:
        dut.next_vacation(vacs="abc")
    assert "TypeError: Argument 'vacs' is expected to an iterable, but is <class 'str'>" in str(e)

    with pytest.raises(TypeError) as e:
        dut.next_vacation(vacs=["abc"])
    assert "TypeError: Item 0 of argument 'vacs' is expected to be of type 'Vacation', but is <class 'str'>" in str(e)

    with pytest.raises(TypeError) as e:
        dut.next_vacation(vacs=EXPECTED, dt="abc")
    assert "TypeError: Argument 'dt' is expected to be of type 'datetime', but is <class 'str'>" in str(e)
