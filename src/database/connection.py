from os import getenv

from dotenv import load_dotenv

from pymongo import MongoClient

load_dotenv()

mongo_client = MongoClient(
    getenv('MONGO_URL', "mongodb://mongo1:27017,mongo2:27017,mongo3:27017/?replicaSet=rs0"),
    serverSelectionTimeoutMS=5000    
)