from urllib.parse import quote_plus

from starlite import HTTPException, Redirect, Request, Router, get

from app.env import (
    AUTH_REDIRECT_URL,
    CLIENT_ID_DISCORD,
    CLIENT_SECRET_DISCORD,
    TOKEN_URL_DISCORD,
    USER_URL_DISCORD,
)
from app.resources import Sessions


@get("/auth", include_in_schema=False, status_code=307)
async def discord_auth(code: str) -> Redirect:
    resp = await Sessions.request.post(
        url=TOKEN_URL_DISCORD,
        data={
            "client_id": CLIENT_ID_DISCORD,
            "client_secret": CLIENT_SECRET_DISCORD,
            "grant_type": "authorization_code",
            "code": code,
            "redirect_uri": AUTH_REDIRECT_URL,
        },
        headers={"Content-Type": "application/x-www-form-urlencoded"},
    )

    if resp.status != 200:
        raise HTTPException(detail="Bad auth", status_code=400)

    access_token = (await resp.json())["access_token"]

    resp = await Sessions.request.get(
        url=USER_URL_DISCORD, headers={"Authorization": f"Bearer {access_token}"}
    )
    if resp.status != 200:
        raise HTTPException(detail="Bad auth", status_code=400)

    return Redirect(path="/")


@get("/login", include_in_schema=False, name="login", status_code=307)
async def discord_login() -> Redirect:
    return Redirect(
        path=f"https://discord.com/api/oauth2/authorize?client_id={CLIENT_ID_DISCORD}&redirect_uri={quote_plus(AUTH_REDIRECT_URL)}&response_type=code&scope=identify"
    )


router = Router(path="/discord", route_handlers=[discord_auth, discord_login])
