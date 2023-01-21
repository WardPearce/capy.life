from enum import Enum
from typing import Optional

from pydantic import BaseConfig, BaseModel, Field
from starlite import UploadFile

WEAPONS = [
    "watermelon",
    "sitting",
    "cuddles",
    "pulling up",
    "cement",
    "convicted felon",
    "peace & vibes",
    "idk im chill man",
]

CLASSES = [
    "chill dude",
    "Barbarian",
    "Bard",
    "Cleric",
    "Fighter",
    "Druid",
    "Monk",
    "Paladin",
    "Ranger",
    "Rogue",
    "Sorcerer",
    "Warlock",
    "Wizard",
]


class RelationshipEnum(Enum):
    taken = "taken"
    single = "single"
    not_looking = "not looking"


class SubmitModal(BaseModel):
    image: UploadFile
    name: Optional[str] = Field(None, max_length=24, regex="^[a-zA-Z_ ]*$")
    relationship_status: RelationshipEnum = RelationshipEnum.single

    class Config(BaseConfig):
        arbitrary_types_allowed = True
