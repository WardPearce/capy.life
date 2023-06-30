import mimetypes
from typing import Optional

from app.env import SETTINGS
from app.models.submit import RelationshipEnum
from pydantic import BaseModel, Field


class CapybaraModel(BaseModel):
    name: str
    image: str = ""
    id: str = Field(..., alias="_id")
    muncher_lvl: int
    weapon: str
    class_: str = Field(..., alias="class")
    used: Optional[str] = None
    relationship_status: RelationshipEnum
    days_ago: int

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if "img_ext" in kwargs:
            image_ext = kwargs["img_ext"]
        else:
            image_ext = mimetypes.guess_extension(kwargs["content_type"])
            if not image_ext:
                image_ext = ".webp"

        self.image = SETTINGS.s3.download_url + f"/{self.id + image_ext}"
