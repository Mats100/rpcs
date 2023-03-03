from pydantic import BaseModel, Extra


class test_schema(BaseModel):
    roll_id: int
    name: str
    phone: str
    major: str


class config:
    orm_mode = True
    extra = Extra.forbid
