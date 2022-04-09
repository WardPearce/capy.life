# -*- coding: utf-8 -*-

"""
GNU AFFERO GENERAL PUBLIC LICENSE
Version 3, 19 November 2007
"""

import aiofiles.os
import jwt
import bcrypt
import hashlib
import pyotp

from starlette.endpoints import HTTPEndpoint
from starlette.requests import Request
from starlette.responses import JSONResponse, Response

from os import path
from datetime import datetime, timedelta
from json import JSONDecodeError

from ...resources import Sessions
from ...env import (
    URL_PROXIED, SAVE_PATH, JWT_SECRET,
    JWT_EXPIRES_DAYS
)
from ...helpers.capy import get_capy
from ...helpers.invite import validate_invite, generate_invite, delete_invite
from ...helpers.admin import create_admin
from ...errors import (
    LoginError, FormMissingFields, PayloadDecodeError,
    InvalidInvite, OptError, OptSetupRequired
)
from ...limiter import LIMITER
from ...modals import AdminModel

from ..decorators import validate_admin


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
    @LIMITER.limit("10/minute")
    async def post(self, request: Request) -> JSONResponse:
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
            create_invites = False
            otp_completed = False

            await delete_invite(json["inviteCode"])
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
            create_invites = record["create_invites"]

        response = JSONResponse({
            "createInvites": create_invites,
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


class AdminInvites(HTTPEndpoint):
    @validate_admin(require_otp=True, can_create_invites=True)
    async def get(self, request: Request, admin: AdminModel) -> JSONResponse:
        invites = []
        async for record in Sessions.mongo.invite.find({}):
            invites.append(record["_id"])
        return JSONResponse(invites)

    @validate_admin(require_otp=True, can_create_invites=True)
    async def post(self, request: Request, admin: AdminModel) -> JSONResponse:
        return JSONResponse({
            "inviteCode": await generate_invite()
        })

    @validate_admin(require_otp=True, can_create_invites=True)
    async def delete(self, request: Request, admin: AdminModel) -> Response:
        if "inviteId" not in request.query_params:
            return Response(status_code=400)

        await delete_invite(request.query_params["inviteId"])

        return Response()


class AdminCapyRemaining(HTTPEndpoint):
    @validate_admin(require_otp=True)
    async def get(self, request: Request, admin: AdminModel) -> JSONResponse:
        return JSONResponse({
            "remaining": await Sessions.mongo.capybara.count_documents({
                "used": None,
                "approved": True
            }),
            "total": await Sessions.mongo.capybara.count_documents({
                "approved": True
            })
        })


class AdminApprovalResource(HTTPEndpoint):
    @validate_admin(require_otp=True)
    async def get(self, request: Request, admin: AdminModel) -> JSONResponse:
        to_approve = []

        async for record in Sessions.mongo.capybara.find({"approved": False}):
            to_approve.append({
                "name": record["name"],
                "image": f"{URL_PROXIED}/api/capy/{record['_id']}",
                "_id": record["_id"]
            })

        return JSONResponse(to_approve)


class AdminApproveResource(HTTPEndpoint):
    @validate_admin(require_otp=True)
    async def post(self, request: Request, admin: AdminModel) -> Response:
        # Add logic to email if exists & remove from db.
        record = await get_capy(request.path_params["_id"])
        await Sessions.mongo.capybara.update_one({
            "_id": record["_id"]
        }, {"$set": {"approved": True}})

        return Response()

    async def delete(self, request: Request, admin: AdminModel) -> Response:
        # Add logic to email if exists & remove from db.
        record = await get_capy(request.path_params["_id"])
        await Sessions.mongo.capybara.delete_many({
            "_id": record["_id"]
        })

        try:
            await aiofiles.os.remove(path.join(
                SAVE_PATH, f"{record['_id']}.capy"
            ))
        except FileNotFoundError:
            pass

        return Response()
