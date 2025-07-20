import os
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from dotenv import load_dotenv

load_dotenv()
username = os.getenv("MONGO_VANDAL_DB_USER")
password = os.getenv("MONGO_VANDAL_DB_PASSWORD")
uri = f"mongodb+srv://{username}:{password}@dungeoncrawlertrainingd.om3ug.mongodb.net/?retryWrites=true&w=majority&appName=DungeonCrawlerTrainingData"

# Create a new client and connect to the server
client = MongoClient(uri, server_api=ServerApi('1'))

def get_connection_details():
    return client
