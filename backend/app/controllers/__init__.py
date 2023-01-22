from starlite import Router

from app.controllers import admin, get, submit

__all__ = ["router"]


router = Router(
    path="/", route_handlers=[get.get_today_capybara, submit.capy, admin.router]
)
