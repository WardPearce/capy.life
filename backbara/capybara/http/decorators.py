from functools import wraps
from typing import Callable
from starlette.requests import Request

from ..errors import CaptchaError
from ..helpers.captcha import validate_captcha


def require_captcha(func: Callable) -> Callable:
    @wraps(func)
    async def _validate(*args, **kwargs) -> Callable:
        request: Request = args[1]
        if ("captchaId" not in request.query_params or
                "captchaCode" not in request.query_params):
            raise CaptchaError()

        await validate_captcha(
            request.query_params["captchaId"],
            request.query_params["captchaCode"]
        )

        return await func(*args, **kwargs)

    return _validate
