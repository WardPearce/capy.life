# -*- coding: utf-8 -*-

"""
GNU AFFERO GENERAL PUBLIC LICENSE
Version 3, 19 November 2007
"""

import socketio


class AdminWebsocket(socketio.AsyncNamespace):
    async def on_connect(self, sid, environ):
        self.enter_room(sid, "admin_approval")

    async def on_disconnect(self, sid):
        self.leave_room(sid, "admin_approval")
