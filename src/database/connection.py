from os import getenv

from dotenv import load_dotenv

from pymongo import MongoClient

load_dotenv()

mongo_client = MongoClient(getenv('MONGO_URL', 'mongodb://mongodb:27017/'))