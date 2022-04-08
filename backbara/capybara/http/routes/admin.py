# -*- coding: utf-8 -*-

"""
GNU AFFERO GENERAL PUBLIC LICENSE
Version 3, 19 November 2007
"""

import aiofiles.os
import jwt
import bcrypt
import hashlib

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
from ...helpers.invite import validate_invite
from ...helpers.admin import create_admin
from ...errors import (
    LoginError, FormMissingFields, PayloadDecodeError,
    InvalidInvite
)


class AdminLogin(HTTPEndpoint):
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
        else:
            record = await Sessions.mongo.admin.find_one({
                "username": json["username"]
            })
            if not record:
                raise LoginError()

            if not bcrypt.checkpw(
                hashlib.sha256(json["password"]).digest(),
                record["password"]
            ):
                raise LoginError()

            _id = record["_id"]

        response = JSONResponse({
            "success": True
        })
        response.set_cookie(
            "jwt-token",
            jwt.encode({
                "ext": (
                    datetime.now() + timedelta(days=JWT_EXPIRES_DAYS)
                ).timestamp(),
                "sub": _id
            }, JWT_SECRET, algorithm="HS256"),
            httponly=True, samesite="strict"
        )

        return response


# ToDo auth admin
class AdminCapyRemaining(HTTPEndpoint):
    async def get(self, request: Request) -> JSONResponse:
        return JSONResponse({
            "remaining": await Sessions.mongo.capybara.count_documents({
                "used": None,
                "approved": True
            }),
            "total": await Sessions.mongo.capybara.count_documents({
                "approved": True
            })
        })


# ToDo auth admin
class AdminApprovalResource(HTTPEndpoint):
    async def get(self, request: Request) -> JSONResponse:
        to_approve = []

        async for record in Sessions.mongo.capybara.find({"approved": False}):
            to_approve.append({
                "name": record["name"],
                "image": f"{URL_PROXIED}/api/capy/{record['_id']}",
                "_id": record["_id"]
            })

        return JSONResponse(to_approve)


# ToDo auth admin
class AdminApproveResource(HTTPEndpoint):
    async def post(self, request: Request) -> Response:
        # Add logic to email if exists & remove from db.
        record = await get_capy(request.path_params["_id"])
        await Sessions.mongo.capybara.update_one({
            "_id": record["_id"]
        }, {"$set": {"approved": True}})

        return Response()

    async def delete(self, request: Request) -> Response:
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
