from typing import TYPE_CHECKING

from aiobotocore.session import get_session
from app.env import SETTINGS

if TYPE_CHECKING:
    from types_aiobotocore_s3 import S3Client


def s3_create_client() -> "S3Client":
    session = get_session()
    return session.create_client(
        "s3",
        region_name=SETTINGS.s3.region_name,
        aws_secret_access_key=SETTINGS.s3.secret_access_key,
        aws_access_key_id=SETTINGS.s3.access_key_id,
        endpoint_url=SETTINGS.s3.endpoint_url,
    )
