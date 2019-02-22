# ferien-api

[![PyPI version](https://badge.fury.io/py/ferien-api.svg)](https://badge.fury.io/py/ferien-api)
[![Build Status](https://travis-ci.org/HazardDede/ferien-api.svg?branch=master)](https://travis-ci.org/HazardDede/ferien-api)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

> Python client library for ferien-api.de

## Installation

`ferien-api` needs python 3.4 or higher to function properly

```
pip install ferien-api
```

## Usage

```python
import ferien


# Get all vacations for all time and states
print("All vacations:", ferien.all_vacations())

# Get all vacations for a specific state (in this case Hamburg - HH) ...
print("All vacations for HH:", ferien.state_vacations('HH'))

# ... and optionally for a specific year
print("All vacations for HH in 2019:", ferien.state_vacations('HH', 2019))

# Fetch all valid states
print("Valid state codes:", ferien.state_codes())

```

Both functions `all_vacations` and `state_vacations` will return a list of `Vacation` data objects.
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

## Changelog

**0.1.0**
* Initial version