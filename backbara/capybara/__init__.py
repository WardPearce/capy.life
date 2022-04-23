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
    ROOT_ADMIN_NAME, CORS_ORIGINS
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

    await Sessions.mongo.captcha.create_index("expire", expireAfterSeconds=0)

    try:
        password = secrets.token_urlsafe(32)
        await create_admin(ROOT_ADMIN_NAME, password, is_root=True)
    except UsernameTaken:
        pass
    else:
        LOGGER.info(f"""Your root login:
Username: {ROOT_ADMIN_NAME}
Password: {password}
Once you login, you'll be prompted to setup Two-factor.""")


app = Starlette(
    routes=ROUTES,
    exception_handlers=ERRORS,  # type: ignore
    middleware=[
        Middleware(CORSMiddleware,
                   allow_origins=CORS_ORIGINS,
                   allow_methods=["GET", "DELETE", "POST"]),
        Middleware(SlowAPIMiddleware),
    ],
    on_startup=[on_start]
)

app.state.limiter = LIMITER
