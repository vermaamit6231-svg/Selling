from pymongo import MongoClient
from config import MONGO_URI

client = MongoClient(MONGO_URI)

db = client["telegram_store"]

users = db["users"]
numbers = db["numbers"]
orders = db["orders"]
