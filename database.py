from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv
import os
import certifi

# Load environment variables
load_dotenv()

# Get configuration
MONGODB_URL = os.getenv("MONGODB_URL")
DB_NAME = os.getenv("DB_NAME", "location_tracking")

def get_database():
    """Get a fresh database connection for each request"""
    client = AsyncIOMotorClient(
        MONGODB_URL,
        tlsCAFile=certifi.where(),
        serverSelectionTimeoutMS=5000
    )
    return client[DB_NAME]

# Helper functions to get fresh collection instances
def get_users_collection():
    return get_database().users

def get_locations_collection():
    return get_database().locations