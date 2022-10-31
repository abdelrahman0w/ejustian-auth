from pydantic import BaseModel


class User(BaseModel):
    uid: str
    pwd: str
