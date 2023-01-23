import os

from aiobotocore.session import get_session

from app.env import ACCESS_KEY_ID, ENDPOINT_URL, FOLDER, REGION_NAME, SECRET_ACCESS_KEY


def s3_create_client():
    session = get_session()
    return session.create_client(
        "s3",
        region_name=REGION_NAME,
        aws_secret_access_key=SECRET_ACCESS_KEY,
        aws_access_key_id=ACCESS_KEY_ID,
        endpoint_url=ENDPOINT_URL,
    )


def format_path(capy_id: str, ext: str) -> str:
    path = []
    if FOLDER:
        path.append(FOLDER)

    path.append(capy_id + ext)

    return os.path.join(*path)
