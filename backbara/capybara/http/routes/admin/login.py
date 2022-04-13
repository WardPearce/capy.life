# -*- coding: utf-8 -*-

"""
GNU AFFERO GENERAL PUBLIC LICENSE
Version 3, 19 November 2007
"""

import jwt
import bcrypt
import hashlib
import pyotp

from starlette.endpoints import HTTPEndpoint
from starlette.requests import Request
from starlette.responses import JSONResponse, Response

from datetime import datetime, timedelta
from json import JSONDecodeError

from ....resources import Sessions
from ....env import (
    JWT_SECRET,
    JWT_EXPIRES_DAYS
)
from ....helpers.invite import validate_invite, delete_invite
from ....helpers.admin import create_admin
from ....errors import (
    LoginError, FormMissingFields, PayloadDecodeError,
    InvalidInvite, OptError, OptSetupRequired
)
from ....limiter import LIMITER
from ....modals import AdminModel

from ...decorators import validate_admin, require_captcha


class AdminOtp(HTTPEndpoint):
    @validate_admin(require_otp=False)
    @LIMITER.limit("10/minute")
    async def get(self, request: Request, admin: AdminModel) -> JSONResponse:
        otp_secret = pyotp.random_base32()
        await Sessions.mongo.admin.update_one({
            "_id": admin._id,
        }, {"$set": {"otp": otp_secret, "otp_completed": False}})

        return JSONResponse({
            "provisioningUri": pyotp.TOTP(otp_secret).provisioning_uri(
                name=admin.username, issuer_name="capy.life"
            )
        })

    @validate_admin(require_otp=False)
    @LIMITER.limit("10/minute")
    async def post(self, request: Request, admin: AdminModel) -> Response:
        try:
            json = await request.json()
        except JSONDecodeError:
            raise PayloadDecodeError()

        if "otpCode" not in json or not isinstance(json["otpCode"], str):
            raise FormMissingFields("`otpCode` is a required field")

        record = await Sessions.mongo.admin.find_one({
            "_id": admin._id
        })
        if not record:
            raise LoginError()  # should never happen

        if record["otp"] is None:
            raise OptSetupRequired()

        if not pyotp.TOTP(record["otp"]).verify(json["otpCode"]):
            raise OptError()

        await Sessions.mongo.admin.update_one({
            "_id": record["_id"],
        }, {"$set": {"otp_completed": True}})

        return Response()


class AdminLogin(HTTPEndpoint):
    @require_captcha
    @LIMITER.limit("10/minute")
    async def post(self, request: Request,
                   captcha_admin_bypass: bool) -> JSONResponse:
        try:
            json = await request.json()
        except JSONDecodeError:
            raise PayloadDecodeError()

        if "username" not in json or not isinstance(json["username"], str):
            raise FormMissingFields("`username` is a required field")

        if "password" not in json or not isinstance(json["password"], str):
            raise FormMissingFields("`username` is a required field")

        if "inviteCode" in json:
            if not isinstance(json["inviteCode"], str):
                raise FormMissingFields("`inviteCode` is not a string")

            try:
                await validate_invite(json["inviteCode"])
            except InvalidInvite:
                raise

            _id = await create_admin(json["username"], json["password"])
            is_root = False
            otp_completed = False

            try:
                invite_code, _ = json["inviteCode"].split("/")
            except ValueError:
                pass
            else:
                await delete_invite(invite_code)
        else:
            record = await Sessions.mongo.admin.find_one({
                "username": json["username"]
            })
            if not record:
                raise LoginError()

            if not bcrypt.checkpw(
                hashlib.sha256(json["password"].encode()).digest(),
                record["password"]
            ):
                raise LoginError()

            if record["otp_completed"]:
                if ("otpCode" not in json or
                        not isinstance(json["otpCode"], str)):
                    raise FormMissingFields("`otpCode` is a required field")

                otp = pyotp.TOTP(record["otp"])
                if not otp.verify(json["otpCode"]):
                    raise OptError()

            otp_completed = record["otp_completed"]

            _id = record["_id"]
            is_root = record["is_root"]

        response = JSONResponse({
            "isRoot": is_root,
            "otpCompleted": otp_completed
        })
        response.set_cookie(
            "jwt-token",
            jwt.encode({
                "exp": (
                    datetime.now() + timedelta(days=JWT_EXPIRES_DAYS)
                ).timestamp(),
                "sub": _id
            }, JWT_SECRET, algorithm="HS256"),
            httponly=True, samesite="strict"
        )

        return response

    async def delete(self, request: Request) -> Response:
        response = Response()
        response.delete_cookie(
            "jwt-token",
            httponly=True, samesite="strict"
        )
        return response
