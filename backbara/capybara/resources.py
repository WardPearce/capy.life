# -*- coding: utf-8 -*-

"""
GNU AFFERO GENERAL PUBLIC LICENSE
Version 3, 19 November 2007
"""

import socketio
from motor import motor_asyncio


from .env import CORS_ORIGINS


class Sessions:
    mongo: motor_asyncio.AsyncIOMotorCollection
    ws = socketio.AsyncServer(
        async_mode="asgi",
        cors_allowed_origins=CORS_ORIGINS
    )
