from pydantic import BaseModel, Field

from mongo import botdb


class User(BaseModel):
    id: int = Field(default_factory=int, alias='_id')
    name: str
    username: str
    isInit: bool = Field(default=False)
    xp: int = Field(default=0)
    solved: list = Field(default=[])


users_collection = botdb['users']
