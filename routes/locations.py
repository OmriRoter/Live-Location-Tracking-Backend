from fastapi import APIRouter, HTTPException, status
from datetime import datetime
from bson import ObjectId
import logging

from models import LocationUpdate, LocationResponse
from database import get_locations_collection, get_users_collection

router = APIRouter()
logger = logging.getLogger(__name__)

@router.post("/update", response_model=LocationResponse)
async def update_user_location(location: LocationUpdate):
    """
    Update the current location of a user in the database.
    
    Args:
        location (LocationUpdate): Object containing user_id, latitude, and longitude
        
    Returns:
        LocationResponse: Object containing updated location information including:
            - user_id: The ID of the user
            - latitude: Updated latitude
            - longitude: Updated longitude
            - last_updated: Timestamp of the update
            
    Raises:
        HTTPException 400: If the user ID format is invalid
        HTTPException 404: If the user is not found
        HTTPException 500: If there's an internal server error during the update
    """
    try:
        # Validate ObjectId format
        try:
            user_id_obj = ObjectId(location.user_id)
        except:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid ID format"
            )

        # Verify user exists
        users_collection = get_users_collection()
        user_data = await users_collection.find_one({"_id": user_id_obj})
        if not user_data:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )

        # Update or create location
        locations_collection = get_locations_collection()
        filter_query = {"user_id": location.user_id}
        update_values = {
            "$set": {
                "latitude": location.latitude,
                "longitude": location.longitude,
                "last_updated": datetime.utcnow()
            }
        }
        await locations_collection.update_one(filter_query, update_values, upsert=True)

        # Retrieve updated data
        updated_doc = await locations_collection.find_one({"user_id": location.user_id})
        if not updated_doc:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to retrieve updated location"
            )

        return LocationResponse(
            user_id=updated_doc["user_id"],
            latitude=updated_doc["latitude"],
            longitude=updated_doc["longitude"],
            last_updated=updated_doc["last_updated"]
        )

    except HTTPException as http_ex:
        raise http_ex
    except Exception as e:
        logger.error(f"Error updating location: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


@router.get("/user/{user_id}", response_model=LocationResponse)
async def get_user_location(user_id: str):
    """
    Retrieve the latest location information for a specific user.
    
    Args:
        user_id (str): The ID of the user whose location is being requested
        
    Returns:
        LocationResponse: Object containing the user's location information including:
            - user_id: The ID of the user
            - latitude: Current latitude
            - longitude: Current longitude
            - last_updated: Timestamp of the last update
            
    Raises:
        HTTPException 400: If the user ID format is invalid
        HTTPException 404: If the user or their location is not found
        HTTPException 500: If there's an internal server error during retrieval
    """
    try:
        try:
            user_id_obj = ObjectId(user_id)
        except:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid ID format"
            )

        # Verify user exists
        users_collection = get_users_collection()
        user_data = await users_collection.find_one({"_id": user_id_obj})
        if not user_data:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )

        # Retrieve location
        locations_collection = get_locations_collection()
        location_doc = await locations_collection.find_one({"user_id": user_id})
        if not location_doc:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Location not found"
            )

        return LocationResponse(
            user_id=location_doc["user_id"],
            latitude=location_doc["latitude"],
            longitude=location_doc["longitude"],
            last_updated=location_doc["last_updated"]
        )

    except HTTPException as http_ex:
        raise http_ex
    except Exception as e:
        logger.error(f"Error fetching user location: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )