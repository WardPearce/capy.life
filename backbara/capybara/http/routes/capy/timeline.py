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
from ....limiter import LIMITER
from ....env import URL_PROXIED


class CapyTimeline(HTTPEndpoint):
    @LIMITER.limit("30/minute")
    async def get(self, request: Request) -> JSONResponse:
        timeline = []

        query = Sessions.mongo.capybara.find({
            "$and": [
                {"used": {"$ne": None}},
                {"used": {"$ne": date.today().isoformat()}}
            ]
        }).sort("used", -1)
        if ("page" in request.query_params and
                request.query_params["page"].isdigit()):
            page = int(request.query_params["page"])
            query.skip(5 * (page - 1)).limit(5)
        else:
            query.limit(5)

        async for record in query:
            timeline.append({
                "name": record["name"],
                "image": f"{URL_PROXIED}/api/capy/{record['_id']}",
                "_id": record["_id"],
                "used": record["used"]
            })

        return JSONResponse(timeline)
