import pytest
from aioresponses import aioresponses

import ferien.async_ as dut
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


@pytest.mark.asyncio
async def test_get_all_vacations():
    with aioresponses() as m:
        m.get('https://ferien-api.de/api/v1/holidays', payload=DUMMY_RESP)

        res = await dut.all_vacations_async()
        assert res == EXPECTED


@pytest.mark.asyncio
async def test_get_all_vacations_bad_status_code():
    with aioresponses() as m:
        m.get('https://ferien-api.de/api/v1/holidays', status=500)

        with pytest.raises(RuntimeError, match="ferien-api.de failed with http code = '500'") as e:
            await dut.all_vacations_async()


@pytest.mark.asyncio
async def test_get_state_vacations_by_state():
    with aioresponses() as m:
        m.get('https://ferien-api.de/api/v1/holidays/HB', payload=DUMMY_RESP)

        res = await dut.state_vacations_async('HB')
        assert res == EXPECTED


@pytest.mark.asyncio
async def test_get_state_vacations_by_state_year():
    with aioresponses() as m:
        m.get('https://ferien-api.de/api/v1/holidays/HB/2017', payload=DUMMY_RESP)

        res = await dut.state_vacations_async('HB', 2017)
        assert res == EXPECTED
