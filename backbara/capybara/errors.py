class CapyError(Exception):
    def __init__(self, msg: str = "Internal error", status: int = 500,
                 *args: object) -> None:
        self.status = status
        super().__init__(msg, *args)


class CaptchaError(CapyError):
    def __init__(self, msg: str = "Invalid captcha code.", status: int = 400,
                 *args: object) -> None:
        super().__init__(msg, status, *args)
