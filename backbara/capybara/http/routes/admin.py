# -*- coding: utf-8 -*-

"""
GNU AFFERO GENERAL PUBLIC LICENSE
Version 3, 19 November 2007
"""

import aiofiles.os

from starlette.endpoints import HTTPEndpoint
from starlette.requests import Request
from starlette.responses import JSONResponse, Response

from os import path

from ...resources import Sessions
from ...env import BACKEND_PROXIED, SAVE_PATH
from ...helpers.capy import get_capy


# ToDo auth admin
class AdminCapyRemaining(HTTPEndpoint):
    async def get(self, request: Request) -> JSONResponse:
        return JSONResponse({
            "remaining": await Sessions.mongo.capybara.count_documents({
                "used": None
            }),
            "total": await Sessions.mongo.capybara.count_documents({})
        })


# ToDo auth admin
class AdminApprovalResource(HTTPEndpoint):
    async def get(self, request: Request) -> JSONResponse:
        to_approve = []

        async for record in Sessions.mongo.capybara.find({"approved": False}):
            to_approve.append({
                "name": record["name"],
                "image": f"{BACKEND_PROXIED}/api/capy/{record['_id']}",
                "_id": record["_id"]
            })

        return JSONResponse(to_approve)


# ToDo auth admin
class AdminApproveResource(HTTPEndpoint):
    async def post(self, request: Request) -> Response:
        record = await get_capy(request.path_params["_id"])
        await Sessions.mongo.capybara.update_one({
            "_id": record["_id"]
        }, {"$set": {"approved": True}})

        return Response()

    async def delete(self, request: Request) -> Response:
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
