from aiohttp import ClientSession
from motor import motor_asyncio


class Sessions:
    mongo: motor_asyncio.AsyncIOMotorCollection
    request: ClientSession
