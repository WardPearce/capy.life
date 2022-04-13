# -*- coding: utf-8 -*-

"""
GNU AFFERO GENERAL PUBLIC LICENSE
Version 3, 19 November 2007
"""

import socketio

from starlette.routing import Mount, Route

from slowapi import _rate_limit_exceeded_handler  # type: ignore
from slowapi.errors import RateLimitExceeded

from .routes.captcha import CaptchaResource

from .routes.admin.approve import AdminApproveResource, AdminApprovalResource
from .routes.admin.login import AdminLogin, AdminOtp
from .routes.admin.invites import AdminInvites
from .routes.admin.misc import AdminCapyRemaining

from .routes.capy.image import CapyImageResource
from .routes.capy.submit import SubmitCapyResource
from .routes.capy.get import CapyDateResource
from .routes.capy.timeline import CapyTimeline

from .errors import capy_error_handle, CapyError

from .websocket import AdminWebsocket

from ..resources import Sessions


Sessions.ws.register_namespace(AdminWebsocket())


ROUTES = [
    Mount("/api", routes=[
        Route("/captcha", CaptchaResource),
        Route("/capy", SubmitCapyResource),
        Route("/capy/timeline", CapyTimeline),
        Route("/capy/{_id}", CapyImageResource),
        Mount("/admin", routes=[
            Route("/approval", AdminApprovalResource),
            Route("/approval/{_id}", AdminApproveResource),
            Route("/remaining", AdminCapyRemaining),
            Route("/login", AdminLogin),
            Route("/login/otp", AdminOtp),
            Route("/invite", AdminInvites)
        ]),
        Route("/", CapyDateResource)
    ]),
    Mount("/socket.io", socketio.ASGIApp(Sessions.ws, socketio_path=""))
]


ERRORS = {
    RateLimitExceeded: _rate_limit_exceeded_handler,
    CapyError: capy_error_handle
}
