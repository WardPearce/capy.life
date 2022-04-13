# -*- coding: utf-8 -*-

"""
GNU AFFERO GENERAL PUBLIC LICENSE
Version 3, 19 November 2007
"""

from starlette.endpoints import HTTPEndpoint
from starlette.requests import Request
from starlette.responses import JSONResponse, Response

from ....resources import Sessions
from ....helpers.invite import generate_invite, delete_invite
from ....modals import AdminModel

from ...decorators import validate_admin


class AdminInvites(HTTPEndpoint):
    @validate_admin(require_otp=True, is_root=True)
    async def get(self, request: Request, admin: AdminModel) -> JSONResponse:
        invites = []
        async for record in Sessions.mongo.invite.find({}):
            invites.append(record["_id"])
        return JSONResponse(invites)

    @validate_admin(require_otp=True, is_root=True)
    async def post(self, request: Request, admin: AdminModel) -> JSONResponse:
        return JSONResponse({
            "inviteCode": await generate_invite()
        })

    @validate_admin(require_otp=True, is_root=True)
    async def delete(self, request: Request, admin: AdminModel) -> Response:
        if "inviteId" not in request.query_params:
            return Response(status_code=400)

        await delete_invite(request.query_params["inviteId"])

        return Response()
