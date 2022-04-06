# -*- coding: utf-8 -*-

"""
GNU AFFERO GENERAL PUBLIC LICENSE
Version 3, 19 November 2007
"""

from datetime import datetime

from ..resources import Sessions
from ..errors import CaptchaError


async def validate_captcha(_id: str, given_code: str) -> None:
    """Validate captcha against given code.

    Parameters
    ----------
    _id : str
    given_code : str

    Raises
    ------
    CaptchaError
    """

    captcha = await Sessions.mongo.captcha.find_one({
        "_id": _id
    })

    await Sessions.mongo.captcha.delete_many({
        "_id": _id
    })

    if (not captcha or datetime.now() > captcha["expires"]
            or given_code != captcha["code"]):
        raise CaptchaError()
