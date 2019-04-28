"""Asynchronous implementation using aiohttp"""
import asyncio
from typing import List, Optional, cast

from .const import (API_ALL_URL, API_STATE_URL,
                    API_STATE_YEAR_URL)
from .model import Vacation
from .types import APIUrl, APIResponse, StateCode
from .util import parse_state_code, parse_year


async def _make_api_request(api_url: APIUrl) -> APIResponse:
    import aiohttp
    async with aiohttp.ClientSession() as session:
        async with session.get(api_url) as resp:
            if resp.status != 200:
                raise RuntimeError(
                    "ferien-api.de failed with http code = '{}'\n"
                    "Error: {}".format(
                        resp.status,
                        await resp.text()
                    ))
            res = await resp.json()
            return cast(APIResponse, res)


async def _convert_json(resp: APIResponse) -> List[Vacation]:
    res = []
    for entry in resp:
        res.append(Vacation.from_dict(entry))
        # Give back control to the event loop after each converted element
        await asyncio.sleep(0.0)
    return res


async def all_vacations_async() -> List[Vacation]:
    """Makes an async request to the ferien-api.de retrieving all
    vacations for all states at once"""
    return await _convert_json(await _make_api_request(API_ALL_URL))


async def state_vacations_async(state_code: StateCode,
                                year: Optional[int] = None) -> List[Vacation]:
    """Makes an async request to the ferien-api.de using the given
    state_code and - optionally - the specified year."""
    state_code = parse_state_code(state_code)
    year = year and parse_year(year)

    if year is None:
        resp = await _make_api_request(
            API_STATE_URL.format(state_code=state_code)
        )
    else:
        resp = await _make_api_request(
            API_STATE_YEAR_URL.format(state_code=state_code, year=str(year))
        )

    return await _convert_json(resp)
