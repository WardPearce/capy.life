from starlette.endpoints import HTTPEndpoint
from starlette.requests import Request
from starlette.responses import Response

from multicolorcaptcha import CaptchaGenerator
from io import BytesIO


generator = CaptchaGenerator(captcha_size_num=1)


class CaptchaResource(HTTPEndpoint):
    async def get(self, request: Request) -> Response:
        captcha = generator.gen_captcha_image(
            margin=False,
            difficult_level=2
        )

        buffer = BytesIO()
        captcha.image.save(buffer, format="PNG")

        return Response(
            buffer.getvalue(),
            media_type="image/png"
        )
