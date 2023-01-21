from os import environ

from dotenv import load_dotenv

load_dotenv()

MONGO_HOST = environ.get("MONGO_HOST", "localhost")
MONGO_PORT = int(environ.get("MONGO_PORT", 27017))
MONGO_COLLECTION = environ.get("MONGO_COLLECTION", "capybara")

BACKEND = environ.get("BACKEND", "http://capylife.localhost/api")
FRONTEND = environ.get("FRONTEND", "http://capylife.localhost")

API_TITLE = environ.get("API_TITLE", "Capy.life")
API_VERSION = environ.get("API_VERSION", "0.0.0")

SUPPORTED_IMAGE_TYPES = environ.get(
    "SUPPORTED_IMAGE_TYPES", "image/webp,image/jpeg,image/jpg,image/png"
).split(",")

MAX_FILE_SIZE_BYTES = int(environ.get("MAX_FILE_SIZE_BYTES", 4194000))

NANO_ID_LEN = int(environ.get("NANO_ID_LEN", 21))

REGION_NAME = environ["REGION_NAME"]
SECRET_ACCESS_KEY = environ["SECRET_ACCESS_KEY"]
ACCESS_KEY_ID = environ["ACCESS_KEY_ID"]
BUCKET = environ["BUCKET"]
FOLDER = environ.get("FOLDER", None)
ENDPOINT_URL = environ.get("ENDPOINT_URL", None)
