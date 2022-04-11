# -*- coding: utf-8 -*-

"""
GNU AFFERO GENERAL PUBLIC LICENSE
Version 3, 19 November 2007
"""

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

    if not captcha:
        raise CaptchaError()

    await Sessions.mongo.captcha.delete_many({
        "_id": captcha["_id"]
    })

    if captcha["code"] != given_code:
        raise CaptchaError()
