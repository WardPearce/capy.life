# -*- coding: utf-8 -*-

"""
GNU AFFERO GENERAL PUBLIC LICENSE
Version 3, 19 November 2007
"""

import secrets

from starlette.applications import Starlette
from starlette.middleware import Middleware
from starlette.middleware.cors import CORSMiddleware

from slowapi.middleware import SlowAPIMiddleware

from motor import motor_asyncio

from .env import (
    MONGO_HOST, MONGO_PORT, MONGO_DB,
    URL_PROXIED, ROOT_ADMIN_NAME
)
from .limiter import LIMITER
from .resources import Sessions
from .http import ROUTES, ERRORS
from .logs import LOGGER
from .errors import UsernameTaken

from .helpers.admin import create_admin


async def on_start() -> None:
    mongo = motor_asyncio.AsyncIOMotorClient(
        MONGO_HOST, MONGO_PORT
    )

    await mongo.server_info()

    Sessions.mongo = mongo[MONGO_DB]

    try:
        password = secrets.token_urlsafe(32)
        await create_admin(ROOT_ADMIN_NAME, password)
    except UsernameTaken:
        pass
    else:
        LOGGER.info((
            "Your root login\n"
            f"Username: {ROOT_ADMIN_NAME}\n"
            f"Password: {password}"
        ))


cors_origins = [URL_PROXIED.lower()]
if cors_origins[0].startswith("https"):
    cors_origins.append(cors_origins[0].replace("https", "http", 1))

app = Starlette(
    routes=ROUTES,
    exception_handlers=ERRORS,  # type: ignore
    middleware=[
        Middleware(CORSMiddleware,
                   allow_origins=cors_origins,
                   allow_methods=["GET", "DELETE", "POST"]),
        Middleware(SlowAPIMiddleware),
    ],
    on_startup=[on_start]
)

app.state.limiter = LIMITER
