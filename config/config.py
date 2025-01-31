from dotenv import load_dotenv
import os

load_dotenv()

MONGODB_URI = os.getenv('MONGODB_URI')
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
DB_NAME = "web_scraper_db"
COLLECTION_NAME = "scraped_data"

# database/mongodb.py
from pymongo import MongoClient
from config.config import MONGODB_URI, DB_NAME, COLLECTION_NAME

class MongoDB:
    def __init__(self):
        self.client = MongoClient(MONGODB_URI)
        self.db = self.client[DB_NAME]
        self.collection = self.db[COLLECTION_NAME]

    def insert_data(self, data):
        return self.collection.insert_one(data)

    def get_all_data(self):
        return list(self.collection.find({}, {'_id': 0}))