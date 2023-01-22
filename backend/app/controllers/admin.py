from datetime import timedelta
from typing import List
from urllib.parse import quote_plus

from starlite import (
    HTTPException,
    NotAuthorizedException,
    Redirect,
    Request,
    Response,
    Router,
    delete,
    get,
    post,
)
from starlite.contrib.jwt import Token

from app.env import (
    AUTH_REDIRECT_URL,
    CLIENT_ID_DISCORD,
    CLIENT_SECRET_DISCORD,
    TOKEN_URL_DISCORD,
    USER_URL_DISCORD,
)
from app.jwt import jwt_cookie_auth
from app.models.admin import AdminModel, CreateAdminModel, ListAdminsModel, StatsModel
from app.resources import Sessions


@post("/auth", tags=["admin"])
async def auth(code: str) -> Response[AdminModel]:
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

    user = await resp.json()

    admin = await Sessions.mongo.approvers.find_one({"_id": user["id"]})
    if not admin:
        raise NotAuthorizedException()

    return jwt_cookie_auth.login(
        identifier=str(user["id"]),
        token_expiration=timedelta(days=24),
        response_body=AdminModel(**admin),
    )


@get("/list", tags=["admin"])
async def list_admins(request: Request[AdminModel, Token]) -> ListAdminsModel:
    if not request.user.is_root:
        raise NotAuthorizedException()

    admins: List[AdminModel] = []

    async for admin in Sessions.mongo.approvers.find():
        admins.append(AdminModel(**admin))

    return ListAdminsModel(admins=admins)


@post("/add", tags=["admin"])
async def add_admin(
    request: Request[AdminModel, Token], data: CreateAdminModel
) -> Response:
    if not request.user.is_root:
        raise NotAuthorizedException()

    if await Sessions.mongo.approvers.count_documents({"_id": data.id}) > 0:
        raise HTTPException(detail="Id already added", status_code=400)

    await Sessions.mongo.approvers.insert_one(
        {"_id": data.id, "username": data.username, "is_root": False}
    )

    return Response(content=None)


@delete("/remove/{admin_id:str}", tags=["admin"])
async def remove_admin(request: Request[AdminModel, Token], admin_id: str) -> None:
    if not request.user.is_root:
        raise NotAuthorizedException()

    await Sessions.mongo.approvers.delete_one({"_id": admin_id})


@delete("/logout", status_code=200, tags=["admin"])
async def logout() -> Response:
    response = Response(content=None)
    response.delete_cookie(jwt_cookie_auth.key)
    return response


@get("/login", include_in_schema=False, name="login", status_code=307)
async def login() -> Redirect:
    return Redirect(
        path=f"https://discord.com/api/oauth2/authorize?client_id={CLIENT_ID_DISCORD}&redirect_uri={quote_plus(AUTH_REDIRECT_URL)}&response_type=code&scope=identify"
    )


@get("/stats", tags=["admin"])
async def stats() -> StatsModel:
    return StatsModel(
        remaining=await Sessions.mongo.capybara.count_documents(
            {"used": None, "approved": True}
        ),
        total=await Sessions.mongo.capybara.count_documents({"approved": True}),
    )


router = Router(
    path="/admin",
    route_handlers=[auth, login, stats, logout, add_admin, remove_admin, list_admins],
)
