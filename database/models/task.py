from pydantic import BaseModel, Field
from bson import ObjectId
from mongo import botdb
from .PydanticObjectId import PydanticObjectId


class Task(BaseModel):
    id: PydanticObjectId = Field(alias='_id')
    name: str
    text: str = Field(default='')
    cost: int
    theme: str
    flag: str
    file: list[str] = Field(default=[])
    url: str = Field(default='')
    lesson: str = Field(default='')

tasks_collection = botdb['tasks']
