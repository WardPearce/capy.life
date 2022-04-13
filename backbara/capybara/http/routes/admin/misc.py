# -*- coding: utf-8 -*-

"""
GNU AFFERO GENERAL PUBLIC LICENSE
Version 3, 19 November 2007
"""

from starlette.endpoints import HTTPEndpoint
from starlette.requests import Request
from starlette.responses import JSONResponse

from ....resources import Sessions

from ....modals import AdminModel

from ...decorators import validate_admin


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
