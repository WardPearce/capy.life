from starlette.routing import Mount, Route

from .routes.captcha import CaptchaResource


ROUTES = [Mount("/api", routes=[
    Route("/captcha", CaptchaResource)
])]
