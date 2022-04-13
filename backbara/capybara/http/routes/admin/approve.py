# -*- coding: utf-8 -*-

"""
GNU AFFERO GENERAL PUBLIC LICENSE
Version 3, 19 November 2007
"""

import aiofiles.os

from starlette.endpoints import HTTPEndpoint
from starlette.requests import Request
from starlette.responses import Response, JSONResponse
from starlette.background import BackgroundTasks

from os import path
from names import get_first_name
from datetime import datetime

from ....resources import Sessions
from ....env import (
    URL_PROXIED, SAVE_PATH,
    SMTP_DOMAIN
)
from ....limiter import LIMITER
from ....helpers.capy import get_capy
from ....helpers.emailer import send_email
from ....modals import AdminModel

from ...decorators import validate_admin


class AdminApprovalResource(HTTPEndpoint):
    @validate_admin(require_otp=True)
    async def get(self, request: Request, admin: AdminModel) -> JSONResponse:
        to_approve = []

        async for record in Sessions.mongo.capybara.aggregate([
            {"$match": {"approved": False}},
            {"$sample": {"size": 5}}
        ]):
            to_approve.append({
                "name": record["name"],
                "image": f"{URL_PROXIED}/api/capy/{record['_id']}",
                "_id": record["_id"]
            })

        return JSONResponse(to_approve)


class AdminApprovalHistoryResource(HTTPEndpoint):
    @validate_admin(require_otp=True)
    async def get(self, request: Request, admin: AdminModel) -> JSONResponse:
        where = {
            "approved": True
        }

        if not admin.is_root:
            where["approved_by"] = admin._id  # type: ignore

        query = Sessions.mongo.capybara.find(where).sort("approved_at", -1)

        if ("page" in request.query_params and
                request.query_params["page"].isdigit()):
            page = int(request.query_params["page"])
            query.skip(10 * (page - 1)).limit(10)
        else:
            query.limit(10)

        approved_capy = []
        async for record in query:
            approved_capy.append({
                "name": record["name"],
                "image": f"{URL_PROXIED}/api/capy/{record['_id']}",
                "_id": record["_id"]
            })

        return JSONResponse(approved_capy)


class AdminDeleteHistoryResource(HTTPEndpoint):
    @LIMITER.limit("5/minute")
    @validate_admin(require_otp=True)
    async def delete(self, request: Request, admin: AdminModel) -> Response:
        query = {"_id": request.path_params["_id"]}
        if not admin.is_root:
            query["approved_by"] = admin._id  # type: ignore

        await Sessions.mongo.capybara.delete_many(query)

        return Response()


class AdminApproveResource(HTTPEndpoint):
    @validate_admin(require_otp=True)
    async def post(self, request: Request, admin: AdminModel) -> Response:
        record = await get_capy(request.path_params["_id"])
        update_values = {
            "approved": True,
            "approved_by": admin._id,
            "approved_at": datetime.now()
        }

        if ("changeName" in request.query_params and
                request.query_params["changeName"] == "true"):
            update_values["name"] = get_first_name()

        background_tasks = BackgroundTasks()
        background_tasks.add_task(
            Sessions.ws.emit,
            event="approval_update",
            data={"_id": record["_id"]},
            to="admin_approval"
        )

        if record["email"] is not None:
            if SMTP_DOMAIN:
                message = (
                    "Thanks for submitting your capybara,"
                    " we appreciate it!"
                )
                if "name" in update_values:
                    message += (
                        " However our admins flagged "
                        "the name as inappropriate & "
                        f"has been changed to \"{update_values['name']}\""
                    )
                message += (
                    "\n\nYour can view your capybara here:"
                    f"{URL_PROXIED}/api/capy/{record['_id']}"
                )
                background_tasks.add_task(
                    send_email,
                    to=record["email"],
                    subject="Your capybara has been approved!",
                    content=message
                )

            update_values["email"] = None  # type: ignore

        await Sessions.mongo.capybara.update_one({
            "_id": record["_id"]
        }, {"$set": update_values})

        return Response(background=background_tasks)

    async def delete(self, request: Request, admin: AdminModel) -> Response:
        record = await get_capy(request.path_params["_id"])

        background_tasks = BackgroundTasks()
        background_tasks.add_task(
            Sessions.ws.emit,
            event="approval_update",
            data={"_id": record["_id"]},
            to="admin_approval"
        )

        if record["email"] is not None and SMTP_DOMAIN:
            background_tasks.add_task(
                send_email,
                to=record["email"],
                subject="Your image has been denied.",
                content=(
                    "Thank for your for attempting to support us, "
                    "however admins have decided to deny your image."
                )
            )

        await Sessions.mongo.capybara.delete_many({
            "_id": record["_id"]
        })

        try:
            await aiofiles.os.remove(path.join(
                SAVE_PATH, f"{record['_id']}.capy"
            ))
        except FileNotFoundError:
            pass

        return Response(background=background_tasks)
