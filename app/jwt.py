import secrets
from typing import Optional

import tldextract
from starlite.contrib.jwt import JWTCookieAuth, Token

from .env import FRONTEND
from .models.admin import AdminModel
from .resources import Sessions


async def retrieve_user_handler(token: Token, connection) -> Optional[AdminModel]:
    # Currently no caching, not many admins
    admin = await Sessions.mongo.approvers.find_one({"_id": token.sub})
    if admin:
        return AdminModel(**admin)

    return None


frontend_domain = tldextract.extract(FRONTEND)

jwt_cookie_auth = JWTCookieAuth[None](
    retrieve_user_handler=retrieve_user_handler,
    token_secret=secrets.token_urlsafe(128),
    domain=f".{frontend_domain.domain}.{frontend_domain.suffix}",
    exclude=["/admin/login", "/admin/auth", "/submit", "/capybara", "/schema"],
)
