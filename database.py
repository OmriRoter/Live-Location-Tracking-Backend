import os
import certifi
from dotenv import load_dotenv
from motor.motor_asyncio import AsyncIOMotorClient

# Load environment variables from .env file
load_dotenv()

# Get MongoDB connection string and database name from environment variables
MONGODB_URL = os.getenv("MONGODB_URL")
DB_NAME = os.getenv("DB_NAME", "location_tracking")

def get_database():
    """
    Create and return an AsyncIOMotorClient connection to MongoDB.
    
    Uses environment variables:
        MONGODB_URL: MongoDB connection string
        DB_NAME: Target database name (defaults to 'location_tracking')
    
    Returns:
        AsyncIOMotorDatabase: Database instance with established connection
        
    Configuration:
        - Uses TLS certificate verification through certifi
        - Server selection timeout set to 5000ms
        - Connects to database specified in DB_NAME environment variable
    """
    client = AsyncIOMotorClient(
        MONGODB_URL,
        tlsCAFile=certifi.where(),
        serverSelectionTimeoutMS=5000
    )
    return client[DB_NAME]

def get_users_collection():
    """
    Get a reference to the users collection in the database.
    
    Returns:
        AsyncIOMotorCollection: Reference to the 'users' collection
    """
    return get_database().users

def get_locations_collection():
    """
    Get a reference to the locations collection in the database.
    
    Returns:
        AsyncIOMotorCollection: Reference to the 'locations' collection
    """
    return get_database().locations