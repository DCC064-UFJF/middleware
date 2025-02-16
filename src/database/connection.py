from os import getenv

from dotenv import load_dotenv

from pymongo import MongoClient

load_dotenv()

mongo_client = MongoClient(
    getenv('MONGO_URL', "mongodb+srv://ricardoervilha:password1234@mongo-eh-lixoo.r63p5.mongodb.net/?retryWrites=true&w=majority&appName=MONGO-EH-LIXOO"),
    serverSelectionTimeoutMS=5000    
)