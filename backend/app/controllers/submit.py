from datetime import datetime
from io import BytesIO
from pathlib import Path

import dhash
import names
import nanoid
from app.env import SETTINGS
from app.lib.s3 import format_path, s3_create_client
from app.lib.stats import generate_stats
from app.models.submit import SubmitModal
from app.resources import Sessions
from PIL import Image
from starlite import Body, HTTPException, RequestEncodingType, Response, post

dhash.force_pil()


@post(path="/submit")
async def capy(
    data: SubmitModal = Body(media_type=RequestEncodingType.MULTI_PART),
) -> Response:
    img_ext = Path(data.image.filename).suffix

    if img_ext not in SETTINGS.file.supported_types:
        raise HTTPException(detail="Content type not supported", status_code=400)

    image_bytes = await data.image.read(SETTINGS.file.max_size + 24)

    if len(image_bytes) > SETTINGS.file.max_size:
        raise HTTPException(detail="Image too large", status_code=400)

    with Image.open(BytesIO(image_bytes)) as img_loaded:
        p_row, p_col = dhash.dhash_row_col(img_loaded)
        phash = dhash.format_hex(p_row, p_col)

    similar_image = await Sessions.mongo.capybara.count_documents({"phash": phash})
    if similar_image > 0:
        raise HTTPException(
            detail="Image too similar to existing image in our database",
            status_code=400,
        )

    name = data.name if data.name else names.get_first_name()

    # Legacy ID system
    _id = nanoid.generate(size=21)
    now = datetime.now()

    insert = {
        "_id": _id,
        "created": now,
        "used": None,
        "name": name,
        "phash": phash,
        "img_ext": img_ext,
        "approved": False,
        "approved_by": None,
        "approved_at": None,
        "relationship_status": data.relationship_status.value,
        **generate_stats(),
    }

    await Sessions.mongo.capybara.insert_one(insert)

    async with s3_create_client() as client:
        await client.put_object(
            Bucket=SETTINGS.s3.bucket,
            Key=format_path(_id, img_ext),
            Body=image_bytes,
        )

    return Response(content=None)
