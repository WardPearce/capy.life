from dataclasses import fields
from typing import Optional

from pydantic import BaseModel, Field

from app.models.submit import RelationshipEnum


class CapybaraModel(BaseModel):
    name: str
    image: str
    id: str = Field(..., alias="_id")
    muncher_lvl: int
    weapon: str
    class_: str = Field(..., alias="class")
    used: Optional[str] = None
    relationship_status: RelationshipEnum
    days_ago: int
