import mimetypes
from datetime import date, timedelta
from typing import Optional, cast

from starlite import NotFoundException, get

from ..env import DOWNLOAD_URL
from ..lib.s3 import format_path
from ..lib.stats import generate_stats
from ..models.get import CapybaraModel
from ..models.submit import RelationshipEnum
from ..resources import Sessions


@get(path="/", opt={"exclude_from_auth": True})
async def get_today_capybara(days_ago: Optional[int] = None) -> CapybaraModel:
    when = (
        date.today().isoformat()
        if days_ago is None
        else (date.today() - timedelta(days=days_ago)).isoformat()
    )

    record = cast(dict, await Sessions.mongo.capybara.find_one({"used": when}))
    if not record:
        if days_ago:
            raise NotFoundException(detail="No capybara on that data")

        async for result in Sessions.mongo.capybara.aggregate(
            [{"$match": {"approved": True, "used": None}}, {"$sample": {"size": 1}}]
        ):
            record = result

        if not record:
            raise NotFoundException()

        # Add stats if legacy capy
        if "muncher_lvl" not in record:
            stats = generate_stats()
            record = {**record, **stats, "relationship_status": RelationshipEnum.single}
        else:
            stats = {}

        await Sessions.mongo.capybara.update_one(
            {"_id": record["_id"]}, {"$set": {"used": when, **stats}}
        )

    record["used"] = when

    if "content_type" in record:
        ext = cast(str, mimetypes.guess_extension(record["content_type"]))
    else:
        ext = record["img_ext"]

    return CapybaraModel(
        **record,
        image=DOWNLOAD_URL + f"/{format_path(record['_id'], ext)}",
        days_ago=days_ago if days_ago is not None else 0,
    )
