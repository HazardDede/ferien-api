"""Contains data models to convert result json to our business object model"""

from datetime import datetime

import attr

from .const import TZ_GERMANY
from .types import StateCode, APIItem


# pylint: disable=too-few-public-methods
@attr.s
class Vacation:
    """
    Internal representation of a single vacation
    (from .. to, naming, ...)

    A typical result json looks like that one below:
    {
      "start":"2017-01-29T23:00",
      "end":"2017-01-31T23:00",
      "year":2017,
      "stateCode":"HB",
      "name":"winterferien",
      "slug":"winterferien-2017-HB"
    }
    """
    start = attr.ib(
        type=datetime,
        validator=attr.validators.instance_of(datetime)
    )  # type: datetime
    end = attr.ib(
        type=datetime,
        validator=attr.validators.instance_of(datetime)
    )  # type: datetime
    year = attr.ib(
        type=int,
        converter=int
    )  # type: int
    state_code = attr.ib(
        type=str,
        converter=str
    )  # type: StateCode
    name = attr.ib(
        type=str,
        converter=str
    )  # type: str
    slug = attr.ib(
        type=str,
        converter=str
    )  # type: str

    @staticmethod
    def _parse_date(candidate: str) -> datetime:
        # Parse iso format
        dt = datetime.strptime(candidate, '%Y-%m-%dT%H:%M')
        # All dates from the api are Europe/Berlin (CET/CEST)
        return TZ_GERMANY.localize(dt)

    @classmethod
    def from_dict(cls, dct: APIItem) -> 'Vacation':
        """Initializes the Vacation model from a dictionary instance."""

        return cls(
            start=cls._parse_date(dct['start']),
            end=cls._parse_date(dct['end']),
            year=dct['year'],
            state_code=dct['stateCode'],
            name=dct.get('name', 'none'),
            slug=dct.get('slug', 'none')
        )
