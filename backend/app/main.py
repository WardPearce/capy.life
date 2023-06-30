from aiohttp import ClientSession
from app.controllers import router
from app.env import SETTINGS
from app.jwt import jwt_cookie_auth
from app.resources import Sessions
from motor import motor_asyncio
from pydantic import BaseModel
from pydantic_openapi_schema.v3_1_0 import Contact, Server
from starlite import CORSConfig, OpenAPIConfig, Starlite


async def check_root_admin(_) -> None:
    if (
        await Sessions.mongo.approvers.count_documents({"_id": SETTINGS.root_admin_id})
        == 0
    ):
        await Sessions.mongo.approvers.insert_one(
            {
                "_id": SETTINGS.root_admin_id,
                "is_root": True,
                "username": "Root admin",
            }
        )


async def start_motor() -> None:
    # Connect mongodb.
    mongo = motor_asyncio.AsyncIOMotorClient(SETTINGS.mongo.host, SETTINGS.mongo.port)
    await mongo.server_info()
    Sessions.mongo = mongo[SETTINGS.mongo.collection]


async def start_aiohttp() -> None:
    Sessions.request = ClientSession()


async def close_aiohttp() -> None:
    await Sessions.request.close()


app = Starlite(
    route_handlers=[router],
    on_startup=[start_motor, start_aiohttp],
    after_startup=[check_root_admin],
    on_shutdown=[close_aiohttp],
    on_app_init=[jwt_cookie_auth.on_app_init],
    cors_config=CORSConfig(
        allow_origins=[SETTINGS.proxies.frontend, SETTINGS.proxies.backend],
        allow_credentials=True,
    ),
    openapi_config=OpenAPIConfig(
        title=SETTINGS.openapi.title,
        version=SETTINGS.openapi.version,
        root_schema_site="redoc",
        servers=[Server(url=SETTINGS.proxies.backend)],
        by_alias=True,
        contact=Contact(
            name="Capy.life team",
            email="capylife@pm.me",
            url="https://github.com/capylife/",  # type: ignore
        ),
    ),
    debug=SETTINGS.proxies.frontend == "http://localhost",
    type_encoders={BaseModel: lambda m: m.dict(by_alias=True)},
)
