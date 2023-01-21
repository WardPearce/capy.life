from starlite import HTTPException, Response, get

from app.env import BUCKET
from app.lib.s3 import format_path, s3_create_client
from app.resources import Sessions


@get(path="/capy/{capy_id:str}")
async def capy_image(capy_id: str) -> Response:
    record = await Sessions.mongo.capybara.find_one({"_id": capy_id})
    if not record:
        raise HTTPException(detail="No capybara with that Id", status_code=400)

    # Legacy format support, otherwise should use CDN.
    async with s3_create_client() as client:
        data = await (
            (await client.get_object(Bucket=BUCKET, Key=format_path(record["_id"])))[
                "Body"
            ].read()
        )

    return Response(content=data, media_type=record["content_type"])
