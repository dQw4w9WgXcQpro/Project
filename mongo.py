from pymongo import MongoClient
from bson import ObjectId

from config import MONGO_URL

botdb = MongoClient(MONGO_URL)
botdb = botdb.get_database('ctfbot')
