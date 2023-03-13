from pydantic import BaseModel, Extra


class Schema(BaseModel):
    roll_id: int
    name: str
    phone: str
    major: str

    class Config:
        orm_mode = True
        extra = Extra.forbid
