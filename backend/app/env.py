import secrets
from os import environ
from typing import Optional

from pydantic import BaseModel, BaseSettings, Field


class MongoDB(BaseModel):
    host: str = "localhost"
    port: int = 27017
    collection: str = "capybara"


class ProxiedUrls(BaseModel):
    frontend: str = "http://localhost"
    backend: str = "http://localhost/api"


class S3(BaseModel):
    region_name: str
    secret_access_key: str
    access_key_id: str
    bucket: str
    download_url: str
    endpoint_url: Optional[str] = None


class OpenAPI(BaseModel):
    title: str = "capy.life"
    version: str = "2.0.0"


class FileUpload(BaseModel):
    max_size = 4194000
    supported_types = [".png", ".jpg", ".jpeg", ".webp"]


class Discord(BaseModel):
    client_id: str
    client_secret: str
    redirect_uri: str
    token_url: str = "https://discord.com/api/oauth2/token"
    user_url: str = "https://discord.com/api/users/@me"


class Settings(BaseSettings):
    file: FileUpload = FileUpload()
    s3: S3
    discord: Discord
    mongo: MongoDB
    proxies: ProxiedUrls = ProxiedUrls()
    openapi: OpenAPI = OpenAPI()

    root_admin_id: str
    jtw_secret: str = Field(secrets.token_urlsafe(32), min_length=32)

    class Config:
        env_prefix = "capy_"


SETTINGS = Settings()  # type: ignore
