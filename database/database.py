# Подключение базы данных MongoDB:
import pymongo
from data.loader import config
from bson.objectid import ObjectId

client = pymongo.MongoClient(config["DB"], 27017)
db = client.bot
collection = db.botadmin
