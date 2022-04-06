from starlette.requests import Request
from starlette.responses import JSONResponse

from ..errors import CapyError


async def capy_error_handle(request: Request, exc: CapyError):
    return JSONResponse({
        "error": str(exc),
        "code": exc.error
    }, status_code=exc.status)
