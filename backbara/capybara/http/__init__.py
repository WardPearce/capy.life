# -*- coding: utf-8 -*-

"""
GNU AFFERO GENERAL PUBLIC LICENSE
Version 3, 19 November 2007
"""

from starlette.routing import Mount, Route

from slowapi import _rate_limit_exceeded_handler  # type: ignore
from slowapi.errors import RateLimitExceeded

from .routes.captcha import CaptchaResource
from .routes.admin import (
    AdminApprovalResource, AdminApproveResource, AdminCapyRemaining,
    AdminLogin, AdminOtp
)

from .routes.capy.image import CapyImageResource
from .routes.capy.submit import SubmitCapyResource
from .routes.capy.get import CapyDateResource

from .errors import capy_error_handle, CapyError


ROUTES = [Mount("/api", routes=[
    Route("/captcha", CaptchaResource),
    Route("/capy", SubmitCapyResource),
    Route("/capy/{_id}", CapyImageResource),
    Mount("/admin", routes=[
        Route("/approval", AdminApprovalResource),
        Route("/approval/{_id}", AdminApproveResource),
        Route("/remaining", AdminCapyRemaining),
        Route("/login", AdminLogin),
        Route("/login/otp", AdminOtp)
    ]),
    Route("/", CapyDateResource)
])]


ERRORS = {
    RateLimitExceeded: _rate_limit_exceeded_handler,
    CapyError: capy_error_handle
}
