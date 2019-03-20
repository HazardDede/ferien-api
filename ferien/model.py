"""Contains data models to convert result json to our business object model"""

from datetime import datetime

import attr


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
    )
    end = attr.ib(
        type=datetime,
        validator=attr.validators.instance_of(datetime)
    )
    year = attr.ib(
        type=int,
        converter=int
    )
    state_code = attr.ib(
        type=str,
        converter=str
    )
    name = attr.ib(
        type=str,
        converter=str
    )
    slug = attr.ib(
        type=str,
        converter=str
    )

    @classmethod
    def from_dict(cls, dct):
        """Initializes the Vacation model from a dictionary instance."""
        return cls(
            start=datetime.strptime(dct.get('start'), '%Y-%m-%dT%H:%M'),
            end=datetime.strptime(dct.get('end'), '%Y-%m-%dT%H:%M'),
            year=dct.get('year'),
            state_code=dct.get('stateCode'),
            name=dct.get('name'),
            slug=dct.get('slug')
        )
