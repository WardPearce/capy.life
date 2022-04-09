import bcrypt
import nanoid
import hashlib

from ..resources import Sessions
from ..env import NANO_ID_LEN
from ..errors import UsernameTaken


async def create_admin(username: str, password: str,
                       create_invites: bool = False) -> str:
    """Create a new admin user.

    Parameters
    ----------
    username : str
    password : str
    create_invites, optional
        If admin can invite other admins, By default False

    Returns
    -------
    str

    Raises
    ------
    UsernameTaken
    """

    if await Sessions.mongo.admin.count_documents({"username": username}) > 0:
        raise UsernameTaken()

    _id = nanoid.generate(size=NANO_ID_LEN)

    await Sessions.mongo.admin.insert_one({
        "_id": _id,
        "username": username,
        "password": bcrypt.hashpw(
            hashlib.sha256(password.encode()).digest(),
            bcrypt.gensalt(16)
        ),
        "otp": None,
        "otp_completed": False,
        "create_invites": create_invites
    })

    return _id
