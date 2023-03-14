from pydantic import BaseModel, Extra
from typing import Optional


class Schema(BaseModel):
    roll_id: int
    name: Optional[str]
    phone: Optional[str]
    major: Optional[str]

    class Config:
        orm_mode = True
        extra = Extra.forbid
