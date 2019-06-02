# ferien-api

[![PyPI version](https://badge.fury.io/py/ferien-api.svg)](https://badge.fury.io/py/ferien-api)
[![Build Status](https://travis-ci.org/HazardDede/ferien-api.svg?branch=master)](https://travis-ci.org/HazardDede/ferien-api)
[![Coverage Status](https://coveralls.io/repos/github/HazardDede/ferien-api/badge.svg?branch=master)](https://coveralls.io/github/HazardDede/ferien-api?branch=master)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

> Python client library for ferien-api.de

## Installation

`ferien-api` needs python 3.5+ to function properly

```
pip install ferien-api
```

## Usage

You could use the synchronous implementation which will block until a response arrives from the api
or you could use the async implementation which will be non-blocking your other async stuff.

**Synchronous**:

```python
import ferien


def main():
    # Get all vacations for all time and states
    print("All vacations:", ferien.all_vacations())

    # Get all vacations for a specific state (in this case Hamburg - HH) ...
    print("All vacations for HH:", ferien.state_vacations('HH'))

    # ... and optionally for a specific year
    print("All vacations for HH in 2019:", ferien.state_vacations('HH', 2019))

    # Fetch all valid states
    print("Valid state codes:", ferien.state_codes())

    # Get current vacation (None if there is no vacation)
    print("Current vacation in HH:", ferien.current_vacation('HH'))

    # Get next vacation (None if there is no next vacation)
    print("Next vacation in HH:", ferien.next_vacation('HH'))


if __name__ == '__main__':
    main()

```

**Asynchronous**:

```python
import asyncio

import ferien


async def main():
    # Get all vacations for all time and states
    print("All vacations:", await ferien.all_vacations_async())

    # Get all vacations for a specific state (in this case Hamburg - HH) ...
    print("All vacations for HH:", await ferien.state_vacations_async('HH'))

    # ... and optionally for a specific year
    print("All vacations for HH in 2019:", await ferien.state_vacations_async('HH', 2019))

    # Fetch all valid states. This one is _NOT_ async
    print("Valid state codes:", ferien.state_codes())

    # Get current vacation (None if there is no vacation)
    print("Current vacation in HH:", ferien.current_vacation(vacs=await ferien.state_vacations_async('HH')))

    # Get next vacation (None if there is no next vacation)
    print("Next vacation in HH:", ferien.next_vacation(vacs=await ferien.state_vacations_async('HH')))


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())

```

Both implementations of `all_vacations` and `state_vacations` will return a list of `Vacation` data objects.
See below for the definition of a `Vacation` object.

```python
Vacation(
    start=datetime.datetime(2020, 12, 21, 0, 0),
    end=datetime.datetime(2021, 1, 5, 0, 0),
    year=2020,
    state_code='HH',
    name='weihnachtsferien',
    slug='weihnachtsferien-2020-HH'
)
```

*Please note*: All datetime objects are in the `Europe/Berlin (CET/CEST)` timezone

Using the async version it is easy to make multiple requests in "parallel" (not true... you know that when you are
an asyncio enthusiast) and save a lot of time:

```python
import asyncio

import ferien


async def print_wrapper(state_code):
    print("Fetching {}".format(state_code))
    res = await ferien.state_vacations_async(state_code, 2019)
    print("Fetched {}".format(state_code))
    return res


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    coros = [
        print_wrapper('HH'),
        print_wrapper('SH'),
        print_wrapper('BE'),
        print_wrapper('BB')
    ]
    loop.run_until_complete(asyncio.gather(*coros))

```

## Changelog

**0.3.3**
* Changes all timestamps from naive to 'Europe/Berlin'

**0.3.2**
* Adds type hints to codebase
* Adds mypy as a linter

**0.3.1**
* Adds pylint as a linter and make him happy!

**0.3.0**
* Adds `current_vacation` and `next_vacation` implementations

**0.2.0**
* Adds an async implementation of `all_vacations` and `state_vacations`

**0.1.0**
* Initial version