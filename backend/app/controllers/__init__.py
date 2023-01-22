from starlite import Router

from app.controllers import get, image, submit

__all__ = ["router"]


router = Router(
    path="/", route_handlers=[get.get_today_capybara, image.capy, submit.capy]
)
