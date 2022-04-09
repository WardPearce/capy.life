from enum import Enum

from .env import SUPPORTED_IMAGE_TYPES


class ErrorCode(Enum):
    INTERNAL_ERROR = 1000
    CAPTCHA_CODE_INVALID = 1001
    FORM_MISSING_FIELDS = 1002
    SIMILAR_IMAGE = 1003
    CAPY_ID_INVALID = 1004
    NO_CAPY_TODAY = 1005
    INVALID_LOGIN = 1006
    PAYLOAD_DECODE_ERROR = 1007
    INVALID_INVITE = 1008
    USERNAME_TAKEN = 1009
    OTP_ERROR = 1010
    OTP_SETUP_REQUIRED = 1011
    FILE_TYPE_NOT_SUPPORT = 1012
    FILE_TOO_LARGE = 1013


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


class LoginError(CapyError):
    def __init__(self, msg: str = "Username or password is incorrect",
                 status: int = 401,
                 *args: object) -> None:
        super().__init__(msg, status, ErrorCode.INVALID_LOGIN, *args)


class PayloadDecodeError(CapyError):
    def __init__(self, msg: str = "Payload could not decode",
                 status: int = 400,
                 *args: object) -> None:
        super().__init__(msg, status, ErrorCode.PAYLOAD_DECODE_ERROR, *args)


class InvalidInvite(CapyError):
    def __init__(self, msg: str = "Invite code is not valid",
                 status: int = 400,
                 *args: object) -> None:
        super().__init__(msg, status, ErrorCode.INVALID_INVITE, *args)


class UsernameTaken(CapyError):
    def __init__(self, msg: str = "Username taken", status: int = 400,
                 *args: object) -> None:
        super().__init__(msg, status, ErrorCode.USERNAME_TAKEN, *args)


class OptError(CapyError):
    def __init__(self, msg: str = "OTP is not correct",
                 status: int = 401, *args: object) -> None:
        super().__init__(msg, status, ErrorCode.OTP_ERROR, *args)


class OptSetupRequired(CapyError):
    def __init__(self, msg: str = "OTP setup is required",
                 status: int = 400, *args: object) -> None:
        super().__init__(msg, status, ErrorCode.OTP_SETUP_REQUIRED, *args)


class FileTypeNotSupported(CapyError):
    def __init__(self, msg: str = f"File type not supported, only {','.join(SUPPORTED_IMAGE_TYPES)} is supported",  # noqa: E501
                 status: int = 400, *args: object) -> None:
        super().__init__(msg, status, ErrorCode.FILE_TYPE_NOT_SUPPORT, *args)


class FileTooLarge(CapyError):
    def __init__(self, msg: str = "File is too large",
                 status: int = 400, *args: object) -> None:
        super().__init__(msg, status, ErrorCode.FILE_TOO_LARGE, *args)
