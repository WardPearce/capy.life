from dataclasses import dataclass


@dataclass
class AdminModel:
    _id: str
    username: str
    password: str
    otp: str
    otp_completed: bool
    is_root: bool
