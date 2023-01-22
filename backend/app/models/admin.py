from pydantic import BaseModel, Field


class AdminModel(BaseModel):
    id: str = Field(..., alias="_id")
    username: str
    is_root: bool = False


class StatsModel(BaseModel):
    remaining: int
    total: int
