# -*- coding: utf-8 -*-

"""
GNU AFFERO GENERAL PUBLIC LICENSE
Version 3, 19 November 2007
"""

import jwt

from functools import wraps
from typing import Callable
from starlette.requests import Request

from ..errors import (
    CaptchaError, OptSetupRequired, LoginError,
    OptError, AdminNotRoot
)
from ..helpers.captcha import validate_captcha
from ..helpers.jwt_ import remove_jwt_response
from ..env import JWT_SECRET
from ..resources import Sessions
from ..modals import AdminModel


def require_captcha(func: Callable) -> Callable:
    @wraps(func)
    async def _validate(*args, **kwargs) -> Callable:
        request: Request = args[1]

        # Admin bypass captcha
        if "jwt-token" in request.cookies:
            try:
                payload = jwt.decode(
                    request.cookies["jwt-token"],
                    JWT_SECRET,
                    algorithms=["HS256"]
                )
            except jwt.InvalidTokenError:
                pass
            else:
                record = await Sessions.mongo.admin.find_one({
                    "_id": payload["sub"]
                })
                if record:
                    return await func(
                        *args, **kwargs,
                        admin=AdminModel(**record)
                    )

        if ("captchaId" not in request.query_params or
                "captchaCode" not in request.query_params):
            raise CaptchaError()

        await validate_captcha(
            request.query_params["captchaId"],
            request.query_params["captchaCode"]
        )

        return await func(*args, **kwargs, admin=None)

    return _validate


def validate_admin(require_otp: bool = True,
                   is_root: bool = False) -> Callable:
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
                return remove_jwt_response(request)

            record = await Sessions.mongo.admin.find_one({
                "_id": payload["sub"]
            })
            if not record:
                return remove_jwt_response(request)

            if is_root and not record["is_root"]:
                raise AdminNotRoot()

            if require_otp:
                if not record["otp_completed"]:
                    raise OptSetupRequired()
            else:
                # Don't allow non OTP routes
                # if OTP completed
                if record["otp_completed"]:
                    raise OptError()

            return await func(
                *args, **kwargs,
                admin=AdminModel(**record)
            )

        return _validate

    return _call
