"""
MongoDB connection management for the dungeon crawler research database.

Establishes secure connection to MongoDB Atlas using environment variables
for credentials. Provides centralized database access for all game modules
to store and retrieve encounter data, loot items, room descriptions,
player performance data, and experimental results.

Requires MONGO_VANDAL_DB_USER and MONGO_VANDAL_DB_PASSWORD environment
variables to be set in .env file for authentication.

Connection is shared across all database operations in the system.
"""

import os
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from dotenv import load_dotenv

load_dotenv()
username = os.getenv("MONGO_VANDAL_DB_USER")
password = os.getenv("MONGO_VANDAL_DB_PASSWORD")
uri = f"mongodb+srv://{username}:{password}@dungeoncrawler.aukk89z.mongodb.net/?retryWrites=true&w=majority&appName=DungeonCrawler&tlsAllowInvalidCertificates=true"

# Create a new client and connect to the server
client = MongoClient(uri, server_api=ServerApi('1'))

def get_connection_details():
    return client
