from datetime import date, timedelta
from typing import Optional

from starlite import NotFoundException, get

from app.env import BACKEND
from app.lib.stats import generate_stats
from app.models.get import CapybaraModel
from app.models.submit import RelationshipEnum
from app.resources import Sessions


@get(path="/")
async def get_today_capybara(days_ago: Optional[int] = None) -> CapybaraModel:
    when = (
        date.today().isoformat()
        if days_ago is None
        else (date.today() - timedelta(days=days_ago)).isoformat()
    )

    record = await Sessions.mongo.capybara.find_one({"used": when})
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

    return CapybaraModel(
        **record,
        image=f"{BACKEND}/api/capy/{record['_id']}",
        days_ago=days_ago if days_ago is not None else 0,
    )
