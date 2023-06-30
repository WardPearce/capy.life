import secrets
from typing import Optional

from app.env import SETTINGS
from app.models.admin import AdminModel
from app.resources import Sessions
from starlite.contrib.jwt import JWTCookieAuth, Token


async def retrieve_user_handler(token: Token, connection) -> Optional[AdminModel]:
    # Currently no caching, not many admins
    admin = await Sessions.mongo.approvers.find_one({"_id": token.sub})
    if admin:
        return AdminModel(**admin)

    return None


jwt_cookie_auth = JWTCookieAuth[None](
    retrieve_user_handler=retrieve_user_handler,
    token_secret=SETTINGS.jtw_secret,
    samesite="strict",
    secure=True,
    exclude=["/admin/login", "/admin/auth", "/submit", "/capybara", "/schema"],
)
