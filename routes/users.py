from fastapi import APIRouter, HTTPException
from datetime import datetime
from bson import ObjectId
import logging
from models import UserCreate, UserResponse
from database import users_collection  # נחזור להשתמש ב-users_collection

logger = logging.getLogger(__name__)
router = APIRouter()

@router.post("/create", response_model=UserResponse)
async def create_user(user: UserCreate):
    """Create a new user"""
    try:
        # Check if username already exists
        if await users_collection.find_one({"username": user.username}):
            raise HTTPException(status_code=400, detail="Username already exists")
        
        # Create new user
        user_data = {
            "username": user.username,
            "created_at": datetime.utcnow()
        }
        
        result = await users_collection.insert_one(user_data)
        
        return UserResponse(
            id=str(result.inserted_id),
            username=user.username,
            created_at=user_data["created_at"]
        )
    except Exception as e:
        logger.error(f"Error creating user: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))