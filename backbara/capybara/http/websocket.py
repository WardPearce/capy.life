# -*- coding: utf-8 -*-

"""
GNU AFFERO GENERAL PUBLIC LICENSE
Version 3, 19 November 2007
"""

import jwt
import socketio
from http import cookies

from ..env import JWT_SECRET
from ..resources import Sessions


class AdminWebsocket(socketio.AsyncNamespace):
    async def on_connect(self, sid, environ):
        raw_cookies = None
        for header in environ["asgi.scope"]["headers"]:
            if header[0] == b"cookie":
                raw_cookies = header[1].decode()
                break

        if raw_cookies:
            loaded_cookies = cookies.SimpleCookie()
            loaded_cookies.load(raw_cookies)

            if "jwt-token" in loaded_cookies:
                try:
                    payload = jwt.decode(
                        loaded_cookies["jwt-token"].value,
                        JWT_SECRET,
                        algorithms=["HS256"]
                    )
                except jwt.InvalidTokenError:
                    pass
                else:
                    if await Sessions.mongo.admin.count_documents({
                        "_id": payload["sub"]
                    }) > 0:
                        self.enter_room(sid, "admin_approval")

    async def on_disconnect(self, sid):
        self.leave_room(sid, "admin_approval")
