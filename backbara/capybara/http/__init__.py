from starlette.routing import Mount, Route

from slowapi import _rate_limit_exceeded_handler  # type: ignore
from slowapi.errors import RateLimitExceeded

from .routes.captcha import CaptchaResource
from .routes.submit_capy import SubmitCapyResource

from .errors import capy_error_handle, CapyError


ROUTES = [Mount("/api", routes=[
    Route("/captcha", CaptchaResource),
    Route("/capy", SubmitCapyResource)
])]


ERRORS = {
    RateLimitExceeded: _rate_limit_exceeded_handler,
    CapyError: capy_error_handle
}
