import mimetypes
from datetime import datetime
from io import BytesIO

import dhash
import names
import nanoid
from PIL import Image
from starlite import Body, HTTPException, RequestEncodingType, Response, post

from app.env import BUCKET, MAX_FILE_SIZE_BYTES, NANO_ID_LEN, SUPPORTED_IMAGE_TYPES
from app.lib.s3 import format_path, s3_create_client
from app.lib.stats import generate_stats
from app.models.submit import SubmitModal
from app.resources import Sessions

dhash.force_pil()


@post(path="/submit")
async def capy(
    data: SubmitModal = Body(media_type=RequestEncodingType.MULTI_PART),
) -> Response:
    img_ext = mimetypes.guess_extension(data.image.content_type)

    if data.image.content_type not in SUPPORTED_IMAGE_TYPES or not img_ext:
        raise HTTPException(detail="Content type not supported", status_code=400)

    read_size = MAX_FILE_SIZE_BYTES + 1
    image_bytes = await data.image.read()

    if len(image_bytes) == read_size:
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
    _id = nanoid.generate(size=NANO_ID_LEN)
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
            Bucket=BUCKET,
            Key=format_path(_id, img_ext),
            Body=image_bytes,
        )

    return Response(content=None)
