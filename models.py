from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional

class UserCreate(BaseModel):
    """Model for creating a new user"""
    username: str

class UserResponse(BaseModel):  # שינינו מ-User ל-UserResponse
    """Model for user response"""
    id: str
    username: str
    created_at: datetime

class LocationUpdate(BaseModel):
    """Model for updating a user's location"""
    user_id: str
    latitude: float
    longitude: float

class LocationResponse(BaseModel):  # הוספנו מודל תגובה למיקום
    """Model for location response"""
    user_id: str
    latitude: float
    longitude: float
    last_updated: datetime