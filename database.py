from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv
import os
import certifi

# Load environment variables
load_dotenv()

# Get configuration
MONGODB_URL = os.getenv("MONGODB_URL")
DB_NAME = os.getenv("DB_NAME", "location_tracking")

# Initialize database connection
client = AsyncIOMotorClient(
    MONGODB_URL,
    tlsCAFile=certifi.where()
)
db = client[DB_NAME]

# Export collections
users_collection = db.users
locations_collection = db.locations