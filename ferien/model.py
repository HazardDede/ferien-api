"""Contains data models to convert result json to our business object model"""

from datetime import datetime

import attr

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

    @classmethod
    def from_dict(cls, dct: APIItem) -> 'Vacation':
        """Initializes the Vacation model from a dictionary instance."""
        return cls(
            start=datetime.strptime(dct['start'], '%Y-%m-%dT%H:%M'),
            end=datetime.strptime(dct['end'], '%Y-%m-%dT%H:%M'),
            year=dct['year'],
            state_code=dct['stateCode'],
            name=dct.get('name', 'none'),
            slug=dct.get('slug', 'none')
        )
