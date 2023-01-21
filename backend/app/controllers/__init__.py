from starlite import Router

from app.controllers.get import get_today_capybara
from app.controllers.image import capy_image
from app.controllers.submit import submit_capy

__all__ = ["router"]


router = Router(path="/", route_handlers=[get_today_capybara, capy_image, submit_capy])
