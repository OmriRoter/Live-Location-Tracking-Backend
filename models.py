"""
Pydantic models for the Live Location API.

This module defines the data models used for request/response handling in the API.
All models inherit from Pydantic's BaseModel for automatic validation and serialization.
"""

from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional

class UserCreate(BaseModel):
    """
    Model for user creation requests.
    
    Attributes:
        username (str): Unique username for the new user
    """
    username: str

class UserVerify(BaseModel):
    """
    Model for user verification requests.
    
    Attributes:
        user_id (str): Unique identifier of the user to verify
    """
    user_id: str

class UserStatusUpdate(BaseModel):
    """
    Model for updating user's active status.
    
    Attributes:
        is_active (bool): New status to set for the user
    """
    is_active: bool

class UserResponse(BaseModel):
    """
    Model for user data responses.
    
    Note:
        Uses field aliasing to map internal 'id' to MongoDB's '_id' format
    
    Attributes:
        id (str): User's unique identifier (aliased as '_id' in JSON)
        username (str): User's username
        created_at (datetime): Timestamp of account creation
        is_active (bool): User's current active status, defaults to True
    """
    id: str = Field(alias="_id")
    username: str
    created_at: datetime
    is_active: bool = True

    class Config:
        # Enable population by field name for Pydantic v2
        populate_by_name = True
        json_encoders = {
            datetime: lambda dt: dt.isoformat()
        }

class LocationUpdate(BaseModel):
    """
    Model for location update requests.
    
    Attributes:
        user_id (str): ID of the user whose location is being updated
        latitude (float): User's current latitude coordinate
        longitude (float): User's current longitude coordinate
    """
    user_id: str
    latitude: float
    longitude: float

class LocationResponse(BaseModel):
    """
    Model for location data responses.
    
    Attributes:
        user_id (str): ID of the user
        latitude (float): User's latitude coordinate
        longitude (float): User's longitude coordinate
        last_updated (datetime): Timestamp of the last location update
    """
    user_id: str
    latitude: float
    longitude: float
    last_updated: datetime

    class Config:
        json_encoders = {
            datetime: lambda dt: dt.isoformat()
        }