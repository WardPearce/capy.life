# -*- coding: utf-8 -*-

"""
GNU AFFERO GENERAL PUBLIC LICENSE
Version 3, 19 November 2007
"""

from starlette.endpoints import HTTPEndpoint
from starlette.requests import Request
from starlette.responses import JSONResponse

from datetime import date

from ....resources import Sessions
from ....env import BACKEND_PROXIED


class CapyDateResource(HTTPEndpoint):
    async def get(self, request: Request) -> JSONResponse:
        current_date = date.today().isoformat()

        record = await Sessions.mongo.capybara.find_one({
            "used": current_date
        })
        if not record:
            async for result in Sessions.mongo.capybara.aggregate([
                {"$match": {"approved": True, "used": None}},
                {"$sample": {"size": 1}}
            ]):
                record = result

            await Sessions.mongo.capybara.update_one({
                "_id": record["_id"]
            }, {"$set": {"used": current_date}})

        return JSONResponse({
            "name": record["name"],
            "image": f"{BACKEND_PROXIED}/api/capy/{record['_id']}",
            "_id": record["_id"],
        })
