from starlette.requests import Request
from starlette.responses import JSONResponse

from ..http.errors import capy_error_handle
from ..errors import LoginError


def remove_jwt_response(request: Request) -> JSONResponse:
    response = capy_error_handle(request, LoginError())
    response.delete_cookie("jwt-token", httponly=True, samesite="strict")
    return response
