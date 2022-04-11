from starlette.requests import Request
from starlette.responses import JSONResponse

from ..errors import CapyError


def capy_error_handle(request: Request, exc: CapyError) -> JSONResponse:
    response = JSONResponse({
        "error": str(exc),
        "code": exc.error
    }, status_code=exc.status)
    if exc.status == 401:
        response.delete_cookie(
            "jwt-token",
            httponly=True, samesite="strict"
        )
    return response
