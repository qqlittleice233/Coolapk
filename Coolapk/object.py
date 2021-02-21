from pydantic.main import BaseModel


class Account(BaseModel):
    uid: int
    username: str
    token: str
