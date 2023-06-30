import mimetypes
from datetime import date, timedelta
from typing import Optional, cast

from app.lib.stats import generate_stats
from app.models.get import CapybaraModel
from app.models.submit import RelationshipEnum
from app.resources import Sessions
from starlite import NotFoundException, get


@get(path="/", opt={"exclude_from_auth": True})
async def get_today_capybara(days_ago: Optional[int] = None) -> CapybaraModel:
    when = (
        date.today().isoformat()
        if days_ago is None
        else (date.today() - timedelta(days=days_ago)).isoformat()
    )

    if days_ago is not None and days_ago < 0:
        raise NotFoundException(detail="Days ago can't be negative")

    record = cast(dict, await Sessions.mongo.capybara.find_one({"used": when}))
    if not record or "muncher_lvl" not in record:
        if not record:
            if days_ago is not None:
                raise NotFoundException(detail="No capybara on that data")

            async for result in Sessions.mongo.capybara.aggregate(
                [{"$match": {"approved": True, "used": None}}, {"$sample": {"size": 1}}]
            ):
                record = result

            if not record:
                raise NotFoundException()

        # Add stats if legacy capy
        if "muncher_lvl" not in record:
            new_stats = {
                **generate_stats(),
                "relationship_status": RelationshipEnum.single.value,
            }
        else:
            new_stats = {}

        record = {**record, **new_stats}

        await Sessions.mongo.capybara.update_one(
            {"_id": record["_id"]}, {"$set": {"used": when, **new_stats}}
        )

    record["used"] = when

    return CapybaraModel(
        **record,
        days_ago=days_ago if days_ago is not None else 0,
    )
