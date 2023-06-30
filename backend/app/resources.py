from aiohttp import ClientSession
from motor import motor_asyncio


class Sessions:
    mongo: motor_asyncio.AsyncIOMotorDatabase
    request: ClientSession
