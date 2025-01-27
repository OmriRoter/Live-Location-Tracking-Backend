from fastapi import APIRouter, HTTPException
from datetime import datetime
from bson import ObjectId
import logging
from models import UserCreate, UserResponse, UserStatusUpdate, UserVerify
from database import get_users_collection, get_locations_collection

logger = logging.getLogger(__name__)
router = APIRouter()

@router.post("/create", response_model=UserResponse)
async def create_user(user: UserCreate):
    """Create a new user"""
    try:
        users_collection = get_users_collection()
        locations_collection = get_locations_collection()
        
        if await users_collection.find_one({"username": user.username}):
            raise HTTPException(status_code=400, detail="Username already exists")
        
        user_data = {
            "username": user.username,
            "created_at": datetime.utcnow(),
            "is_active": True
        }
        
        result = await users_collection.insert_one(user_data)
        
        default_location = {
            "user_id": str(result.inserted_id),
            "latitude": 0.0,
            "longitude": 0.0,
            "last_updated": datetime.utcnow()
        }
        
        await locations_collection.insert_one(default_location)
        
        return UserResponse(
            id=str(result.inserted_id),
            username=user.username,
            created_at=user_data["created_at"],
            is_active=user_data["is_active"]
        )
    except Exception as e:
        logger.error(f"Error creating user: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/verify", response_model=UserResponse)
async def verify_user(user: UserVerify):
    """Verify user exists"""
    try:
        users_collection = get_users_collection()
        
        try:
            user_id_obj = ObjectId(user.user_id)
        except:
            raise HTTPException(status_code=400, detail="Invalid user ID format")
        
        user_data = await users_collection.find_one({"_id": user_id_obj})
        if not user_data:
            raise HTTPException(status_code=404, detail="User not found")
        
        return UserResponse(
            id=str(user_data["_id"]),
            username=user_data["username"],
            created_at=user_data["created_at"],
            is_active=user_data["is_active"]
        )
    except HTTPException as he:
        raise he
    except Exception as e:
        logger.error(f"Error verifying user: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.patch("/{user_id}/status", response_model=UserResponse)
async def update_user_status(user_id: str, status_update: UserStatusUpdate):
    """Update user's active status"""
    try:
        users_collection = get_users_collection()
        
        try:
            user_id_obj = ObjectId(user_id)
        except:
            raise HTTPException(status_code=400, detail="Invalid user ID format")
        
        user = await users_collection.find_one({"_id": user_id_obj})
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        
        await users_collection.update_one(
            {"_id": user_id_obj},
            {"$set": {"is_active": status_update.is_active}}
        )
        
        updated_user = await users_collection.find_one({"_id": user_id_obj})
        
        return UserResponse(
            id=str(updated_user["_id"]),
            username=updated_user["username"],
            created_at=updated_user["created_at"],
            is_active=updated_user["is_active"]
        )
    except HTTPException as he:
        raise he
    except Exception as e:
        logger.error(f"Error updating user status: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))