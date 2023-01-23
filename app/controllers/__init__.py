from starlite import Router

from . import admin, get, submit

__all__ = ["router"]


router = Router(
    path="/", route_handlers=[get.get_today_capybara, submit.capy, admin.router]
)
