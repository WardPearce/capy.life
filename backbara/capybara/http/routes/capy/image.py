# -*- coding: utf-8 -*-

"""
GNU AFFERO GENERAL PUBLIC LICENSE
Version 3, 19 November 2007
"""

import aiofiles

from starlette.endpoints import HTTPEndpoint
from starlette.requests import Request
from starlette.responses import Response

from os import path

from ....env import SAVE_PATH
from ....errors import InvalidCapyId
from ....helpers.capy import get_capy
from ....limiter import LIMITER


class CapyImageResource(HTTPEndpoint):
    @LIMITER.limit("60/minute")
    async def get(self, request: Request) -> Response:
        record = await get_capy(request.path_params["_id"])

        try:
            async with aiofiles.open(
                    path.join(SAVE_PATH, f"{record['_id']}.capy"),
                    "rb") as f_:
                content = await f_.read()
        except FileNotFoundError:
            raise InvalidCapyId()

        return Response(
            content,
            media_type=record["content_type"]
        )
