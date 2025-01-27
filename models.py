from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional

class UserCreate(BaseModel):
    """Model for creating a new user"""
    username: str

class UserVerify(BaseModel):
    """Model for verifying user"""
    user_id: str

class UserStatusUpdate(BaseModel):
    """Model for updating user status"""
    is_active: bool

class UserResponse(BaseModel):
    """Model for user response"""
    id: str
    username: str
    created_at: datetime
    is_active: bool = True

class LocationUpdate(BaseModel):
    """Model for updating a user's location"""
    user_id: str
    latitude: float
    longitude: float

class LocationResponse(BaseModel):
    """Model for location response"""
    user_id: str
    latitude: float
    longitude: float
    last_updated: datetime