from fastapi import APIRouter, HTTPException
from datetime import datetime
from bson import ObjectId
import logging
from models import LocationUpdate, LocationResponse
from database import users_collection, locations_collection  # שימוש בקולקציות ישירות

logger = logging.getLogger(__name__)
router = APIRouter()

@router.post("/update", response_model=LocationResponse)
async def update_location(location: LocationUpdate):
    """Update user location"""
    try:
        # Verify user exists
        try:
            user_id_obj = ObjectId(location.user_id)
        except:
            raise HTTPException(status_code=400, detail="Invalid user ID format")

        user = await users_collection.find_one({"_id": user_id_obj})
        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        # Create location data
        location_data = {
            "user_id": location.user_id,
            "latitude": location.latitude,
            "longitude": location.longitude,
            "last_updated": datetime.utcnow()
        }
        
        # Update in database
        await locations_collection.update_one(
            {"user_id": location.user_id},
            {"$set": location_data},
            upsert=True
        )

        return LocationResponse(
            user_id=location.user_id,
            latitude=location.latitude,
            longitude=location.longitude,
            last_updated=location_data["last_updated"]
        )

    except HTTPException as he:
        raise he
    except Exception as e:
        logger.error(f"Error updating location: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/user/{user_id}", response_model=LocationResponse)
async def get_user_location(user_id: str):
    """Get user's last known location"""
    try:
        # Verify user ID format
        try:
            user_id_obj = ObjectId(user_id)
        except:
            raise HTTPException(status_code=400, detail="Invalid user ID format")

        # Get location
        location = await locations_collection.find_one({"user_id": user_id})
        if not location:
            raise HTTPException(status_code=404, detail="Location not found")
        
        return LocationResponse(
            user_id=location["user_id"],
            latitude=location["latitude"],
            longitude=location["longitude"],
            last_updated=location["last_updated"]
        )
    except HTTPException as he:
        raise he
    except Exception as e:
        logger.error(f"Error retrieving location: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))