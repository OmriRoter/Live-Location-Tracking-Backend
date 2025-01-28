from fastapi import APIRouter, HTTPException, status
from bson import ObjectId
from datetime import datetime
import logging

from models import (
    UserCreate,
    UserResponse,
    UserStatusUpdate,
    UserVerify
)
from database import get_users_collection, get_locations_collection

router = APIRouter()
logger = logging.getLogger(__name__)

@router.post("/create", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def create_user(user: UserCreate):
    """
    Create a new user in the database with a default location.
    
    Args:
        user (UserCreate): Object containing the user creation data including:
            - username: Unique identifier for the user
            
    Returns:
        UserResponse: Object containing the created user's information including:
            - id: Unique identifier (string)
            - username: User's username
            - created_at: Timestamp of creation
            - is_active: User's active status (default True)
            
    Raises:
        HTTPException 400: If the username already exists
        HTTPException 500: If there's an internal server error during creation
    """
    try:
        users_collection = get_users_collection()
        locations_collection = get_locations_collection()

        # Check if username exists
        existing_user = await users_collection.find_one({"username": user.username})
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Username already exists"
            )

        # Prepare user data
        user_data = {
            "username": user.username,
            "created_at": datetime.utcnow(),
            "is_active": True
        }

        result = await users_collection.insert_one(user_data)
        inserted_id = result.inserted_id

        # Create initial location entry
        default_location = {
            "user_id": str(inserted_id),
            "latitude": 0.0,
            "longitude": 0.0,
            "last_updated": datetime.utcnow()
        }
        await locations_collection.insert_one(default_location)

        # Construct and return response
        return UserResponse(
            id=str(inserted_id),
            username=user.username,
            created_at=user_data["created_at"],
            is_active=user_data["is_active"]
        )

    except HTTPException as http_ex:
        raise http_ex
    except Exception as e:
        logger.error(f"Error creating user: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


@router.post("/verify", response_model=UserResponse)
async def verify_user(user: UserVerify):
    """
    Verify a user's existence and retrieve their information.
    
    Args:
        user (UserVerify): Object containing:
            - user_id: The ID of the user to verify
            
    Returns:
        UserResponse: Object containing the user's information including:
            - id: User's unique identifier
            - username: User's username
            - created_at: Account creation timestamp
            - is_active: Current active status
            
    Raises:
        HTTPException 400: If the user ID format is invalid
        HTTPException 404: If the user is not found
        HTTPException 500: If there's an internal server error during verification
    """
    try:
        users_collection = get_users_collection()

        # Validate ObjectId format
        try:
            user_id_obj = ObjectId(user.user_id)
        except:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid user ID format"
            )

        user_data = await users_collection.find_one({"_id": user_id_obj})
        if not user_data:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )

        # Convert ObjectId to string for Pydantic model
        user_data["_id"] = str(user_data["_id"])

        return UserResponse(**user_data)

    except HTTPException as http_ex:
        raise http_ex
    except Exception as e:
        logger.error(f"Error verifying user: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


@router.patch("/{user_id}/status", response_model=UserResponse)
async def update_user_status(user_id: str, status_update: UserStatusUpdate):
    """
    Update a user's active status.
    
    Args:
        user_id (str): The ID of the user to update
        status_update (UserStatusUpdate): Object containing:
            - is_active: New active status for the user
            
    Returns:
        UserResponse: Object containing the updated user information including:
            - id: User's unique identifier
            - username: User's username
            - created_at: Account creation timestamp
            - is_active: Updated active status
            
    Raises:
        HTTPException 400: If the user ID format is invalid
        HTTPException 404: If the user is not found
        HTTPException 500: If there's an internal server error during update
    """
    try:
        users_collection = get_users_collection()

        # Validate ObjectId format
        try:
            user_id_obj = ObjectId(user_id)
        except:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid user ID format"
            )

        user_doc = await users_collection.find_one({"_id": user_id_obj})
        if not user_doc:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )

        # Update is_active field
        await users_collection.update_one(
            {"_id": user_id_obj},
            {"$set": {"is_active": status_update.is_active}}
        )

        updated_user = await users_collection.find_one({"_id": user_id_obj})
        updated_user["_id"] = str(updated_user["_id"])  # Convert ObjectId to string

        return UserResponse(**updated_user)

    except HTTPException as http_ex:
        raise http_ex
    except Exception as e:
        logger.error(f"Error updating user status: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )