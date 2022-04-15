# -*- coding: utf-8 -*-

"""
GNU AFFERO GENERAL PUBLIC LICENSE
Version 3, 19 November 2007
"""

import os
import secrets

from dotenv import load_dotenv


load_dotenv()

REDIS_HOST = os.getenv("REDIS_HOST", "localhost")
REDIS_PORT = int(os.getenv("REDIS_PORT", 6379))

MONGO_HOST = os.getenv("MONGO_IP", "localhost")
MONGO_PORT = int(os.getenv("MONGO_PORT", 27017))
MONGO_DB = os.getenv("MONGO_DB", "capybara")

URL_PROXIED = os.getenv("URL_PROXIED", "http://localhost")

NANO_ID_LEN = int(os.getenv("NANO_ID_LEN", 21))

SAVE_PATH = os.getenv("SAVE_PATH", "./capybaras")

JWT_SECRET_PATH = os.getenv("JWT_SECRET_PATH", "./jwt.secret")
JWT_EXPIRES_DAYS = int(os.getenv("JWT_EXPIRES_DAYS", 20))

ROOT_ADMIN_NAME = os.getenv("ROOT_ADMIN_NAME", "capy")

SUPPORTED_IMAGE_TYPES = os.getenv(
    "SUPPORTED_IMAGE_TYPES", "image/webp,image/jpeg,image/jpg,image/png"
).split(",")

MAX_FILE_SIZE_BYTES = int(os.getenv("MAX_FILE_SIZE_BYTES", 4194000))

SMTP_DOMAIN = os.getenv("SMTP_DOMAIN", None)
SMTP_MAIN = os.getenv("SMTP_MAIN", "no-reply")
SMTP_HOST = os.getenv("SMTP_HOST", "localhost")
SMTP_USERNAME = os.getenv("SMTP_USERNAME", None)
SMTP_PASSWORD = os.getenv("SMTP_PASSWORD", None)

try:
    os.mkdir(SAVE_PATH)
except Exception:
    pass


if not os.path.exists(JWT_SECRET_PATH):
    JWT_SECRET = secrets.token_urlsafe(32)
    with open(JWT_SECRET_PATH, "w+") as f_:
        f_.write(JWT_SECRET)
else:
    with open(JWT_SECRET_PATH, "r") as f_:
        JWT_SECRET = f_.read()


assert len(JWT_SECRET) == 86
