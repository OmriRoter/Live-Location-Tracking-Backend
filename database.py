from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv
import os
import certifi

# Load environment variables
load_dotenv()

# Get configuration
MONGODB_URL = os.getenv("MONGODB_URL")
DB_NAME = os.getenv("DB_NAME", "location_tracking")

# Create MongoDB client
client = AsyncIOMotorClient(
    MONGODB_URL,
    tlsCAFile=certifi.where(),
    serverSelectionTimeoutMS=5000
)

# Get database instance
db = client[DB_NAME]

# Export collections
users_collection = db.users
locations_collection = db.locations

# Test connection on startup
async def connect_and_check():
    try:
        await client.admin.command('ping')
    except Exception as e:
        print(f"Failed to connect to MongoDB: {e}")
        raise e