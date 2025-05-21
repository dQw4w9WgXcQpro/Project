from pydantic import BaseModel, Field
from bson import ObjectId
from mongo import botdb
from .PydanticObjectId import PydanticObjectId


class Lesson(BaseModel):
    id: PydanticObjectId = Field(alias='_id')
    name: str
    text: str = Field(default='')
    theme: str
    link: str = Field(default='')


lessons_collection = botdb['lessons']
