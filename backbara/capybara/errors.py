from enum import Enum


class ErrorCode(Enum):
    INTERNAL_ERROR = 1000
    CAPTCHA_CODE_INVALID = 1001
    FORM_MISSING_FIELDS = 1002
    SIMILAR_IMAGE = 1003
    CAPY_ID_INVALID = 1004
    NO_CAPY_TODAY = 1005


class CapyError(Exception):
    def __init__(self, msg: str = "Internal error", status: int = 500,
                 error: ErrorCode = ErrorCode.INTERNAL_ERROR,
                 *args: object) -> None:
        self.status = status
        self.error = error.value
        super().__init__(msg, *args)


class CaptchaError(CapyError):
    def __init__(self, msg: str = "Invalid captcha code", status: int = 400,
                 *args: object) -> None:
        super().__init__(
            msg, status, ErrorCode.CAPTCHA_CODE_INVALID, *args
        )


class FormMissingFields(CapyError):
    def __init__(self, msg: str = "Form missing fields", status: int = 400,
                 *args: object) -> None:
        super().__init__(msg, status, ErrorCode.FORM_MISSING_FIELDS, *args)


class SimilarImageError(CapyError):
    def __init__(self, msg: str =
                 "Image too close to an existing capybara in our database",
                 status: int = 400,
                 *args: object) -> None:
        super().__init__(msg, status, ErrorCode.SIMILAR_IMAGE, *args)


class InvalidCapyId(CapyError):
    def __init__(self, msg: str = "Capy ID not found", status: int = 404,
                 *args: object) -> None:
        super().__init__(msg, status, ErrorCode.CAPY_ID_INVALID, *args)


class NoCapyToday(CapyError):
    def __init__(self, msg: str = "We ran out of capybaras", status: int = 500,
                 *args: object) -> None:
        super().__init__(msg, status, ErrorCode.NO_CAPY_TODAY, *args)
