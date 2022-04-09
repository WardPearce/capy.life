# -*- coding: utf-8 -*-

"""
GNU AFFERO GENERAL PUBLIC LICENSE
Version 3, 19 November 2007
"""

import jwt

from functools import wraps
from typing import Callable
from starlette.requests import Request
from starlette.responses import JSONResponse

from ..errors import CaptchaError, OptSetupRequired, LoginError, OptError
from ..helpers.captcha import validate_captcha
from ..env import JWT_SECRET
from ..resources import Sessions

from .errors import capy_error_handle


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


def __remove_jwt_reponse(request: Request) -> JSONResponse:
    response = capy_error_handle(request, LoginError())
    response.delete_cookie("jwt-token", httponly=True, samesite="strict")
    return response


def validate_admin(require_otp: bool = True) -> Callable:
    def _call(func: Callable) -> Callable:
        @wraps(func)
        async def _validate(*args, **kwargs) -> Callable:
            request: Request = args[1]

            if "jwt-token" not in request.cookies:
                raise LoginError()

            try:
                payload = jwt.decode(
                    request.cookies["jwt-token"],
                    JWT_SECRET,
                    algorithms=["HS256"]
                )
            except jwt.InvalidTokenError:
                return __remove_jwt_reponse(request)

            record = await Sessions.mongo.admin.find_one({
                "_id": payload["sub"]
            })
            if not record:
                return __remove_jwt_reponse(request)

            if require_otp:
                if record["otp"] is None:
                    raise OptSetupRequired()
            else:
                if record["otp"] is not None:
                    raise OptError()

            return await func(*args, **kwargs)

        return _validate

    return _call
