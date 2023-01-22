from aiohttp import ClientSession
from motor import motor_asyncio
from pydantic import AnyUrl, BaseModel
from pydantic_openapi_schema.v3_1_0 import Contact, Server
from starlite import CORSConfig, OpenAPIConfig, Starlite

from app.controllers import router
from app.env import (
    API_TITLE,
    API_VERSION,
    BACKEND,
    FRONTEND,
    MONGO_COLLECTION,
    MONGO_HOST,
    MONGO_PORT,
    ROOT_ADMIN_DISCORD_ID,
)
from app.resources import Sessions


async def check_root_admin(_) -> None:
    await Sessions.mongo.approvers.delete_many({"is_root": True})
    await Sessions.mongo.approvers.insert_one(
        {"_id": ROOT_ADMIN_DISCORD_ID, "is_root": True, "username": "Root admin"}
    )


async def start_motor() -> None:
    # Connect mongodb.
    mongo = motor_asyncio.AsyncIOMotorClient(MONGO_HOST, MONGO_PORT)
    await mongo.server_info()
    Sessions.mongo = mongo[MONGO_COLLECTION]


async def start_aiohttp() -> None:
    Sessions.request = ClientSession()


async def close_aiohttp() -> None:
    await Sessions.request.close()


app = Starlite(
    route_handlers=[router],
    on_startup=[start_motor, start_aiohttp],
    after_startup=[check_root_admin],
    on_shutdown=[close_aiohttp],
    cors_config=CORSConfig(allow_origins=[BACKEND, FRONTEND]),
    openapi_config=OpenAPIConfig(
        title=API_TITLE,
        version=API_VERSION,
        root_schema_site="redoc",
        servers=[Server(url=BACKEND)],
        by_alias=True,
        contact=Contact(
            name="Capy.life team",
            email="capylife@pm.me",
            url=AnyUrl("https://github.com/capylife/", scheme="https"),
        ),
    ),
    debug=FRONTEND.endswith("localhost"),
    type_encoders={BaseModel: lambda m: m.dict(by_alias=True)},
)
