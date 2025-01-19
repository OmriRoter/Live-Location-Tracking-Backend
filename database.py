from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv
import os
import certifi
import asyncio

# Load environment variables
load_dotenv()

# Get configuration
MONGODB_URL = os.getenv("MONGODB_URL")
DB_NAME = os.getenv("DB_NAME", "location_tracking")

# Create a new event loop for each request
def get_database():
    client = AsyncIOMotorClient(
        MONGODB_URL,
        tlsCAFile=certifi.where()
    )
    return client[DB_NAME]

# Get database instance
db = get_database()

# Export collections
users_collection = db.users
locations_collection = db.locations