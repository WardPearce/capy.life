from typing import List

from app.models.get import CapybaraModel
from pydantic import BaseModel, Field


class CreateAdminModel(BaseModel):
    username: str
    id: str = Field(..., alias="_id")


class AdminModel(CreateAdminModel):
    is_root: bool = False


class ListAdminsModel(BaseModel):
    admins: List[AdminModel]


class StatsModel(BaseModel):
    remaining: int
    total: int


class ToApproveModel(BaseModel):
    to_approve: List[CapybaraModel]
