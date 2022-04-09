import secrets
import nanoid
import bcrypt

from datetime import datetime, timedelta

from ..resources import Sessions
from ..env import NANO_ID_LEN
from ..errors import InvalidInvite


async def generate_invite() -> str:
    """Generate a new invitation code for admins.

    Returns
    -------
    str
    """

    _id = nanoid.generate(size=NANO_ID_LEN)
    password = secrets.token_urlsafe(20)

    await Sessions.mongo.invite.insert_one({
        "_id": _id,
        "password": bcrypt.hashpw(password.encode(), bcrypt.gensalt(16)),
        "expires": datetime.now() + timedelta(hours=36)
    })

    return f"{_id}/{password}"


async def validate_invite(code: str) -> None:
    """Validate a invite code.

    Parameters
    ----------
    code : str

    Raises
    ------
    InvalidInvite
    """

    try:
        _id, password = code.split("/")
    except ValueError:
        raise InvalidInvite()

    record = await Sessions.mongo.invite.find_one({
        "_id": _id
    })
    if not bcrypt.checkpw(password.encode(), record["password"]):
        raise InvalidInvite()
