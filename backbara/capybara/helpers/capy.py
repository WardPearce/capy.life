# -*- coding: utf-8 -*-

"""
GNU AFFERO GENERAL PUBLIC LICENSE
Version 3, 19 November 2007
"""


from ..resources import Sessions
from ..errors import InvalidCapyId


async def get_capy(id_: str) -> dict:
    """Get a CAPY record by id.

    Parameters
    ----------
    id_ : str

    Returns
    -------
    dict

    Raises
    ------
    InvalidCapyId
    """

    record = await Sessions.mongo.capybara.find_one({
        "_id": id_
    })
    if not record:
        raise InvalidCapyId()

    return record
