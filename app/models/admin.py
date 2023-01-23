from typing import List

from pydantic import BaseModel, Field

from ..models.get import CapybaraModel


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
