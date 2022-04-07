# -*- coding: utf-8 -*-

"""
GNU AFFERO GENERAL PUBLIC LICENSE
Version 3, 19 November 2007
"""

from starlette.endpoints import HTTPEndpoint
from starlette.requests import Request
from starlette.responses import RedirectResponse

from ...oauth import OAUTH
from ...env import BACKEND_PROXIED, FRONTEND_PROXIED


class LoginResource(HTTPEndpoint):
    async def get(self, request: Request):
        twitter = OAUTH.create_client("twitter")
        redirect_uri = f"{BACKEND_PROXIED}/api/authorize"
        return await twitter.authorize_redirect(request, redirect_uri)


class AuthorizeResource(HTTPEndpoint):
    async def get(self, request: Request):
        twitter = OAUTH.create_client("twitter")
        token = await twitter.authorize_access_token(request)

        if "user_id" in token:
            request.session["user_id"] = token["user_id"]

        return RedirectResponse(FRONTEND_PROXIED)
