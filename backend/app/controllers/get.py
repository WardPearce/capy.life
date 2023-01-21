from datetime import date, datetime
from typing import Optional

from starlite import NotFoundException, get

from app.env import BACKEND
from app.lib.stats import generate_stats
from app.models.get import CapybaraModel
from app.models.submit import RelationshipEnum
from app.resources import Sessions


@get(path="/")
async def get_today_capybara(on_date: Optional[datetime] = None) -> CapybaraModel:
    when = date.today().isoformat() if not on_date else on_date.isoformat()

    record = await Sessions.mongo.capybara.find_one({"used": when})
    if not record:
        if on_date:
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
    )
