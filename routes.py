# from fastapi import APIRouter, HTTPException
# from datetime import datetime
# from models import LocationUpdate, LocationResponse, UserCreate, UserResponse
# from database import locations_collection, users_collection
# from bson import ObjectId

# router = APIRouter()

# @router.post("/user", response_model=UserResponse)
# async def create_user(user: UserCreate):
#     """
#     Create a new user
#     """
#     # בדיקה אם המשתמש קיים
#     existing_user = await users_collection.find_one({"username": user.username})
#     if existing_user:
#         raise HTTPException(status_code=400, detail="Username already exists")
    
#     user_data = {
#         "username": user.username,
#         "created_at": datetime.utcnow()
#     }
    
#     # הכנסת המשתמש לדאטהבייס
#     result = await users_collection.insert_one(user_data)
    
#     # החזרת התשובה עם ה-ID
#     return UserResponse(
#         id=str(result.inserted_id),  # המרה ל-string של ה-ObjectID
#         username=user.username,
#         created_at=user_data["created_at"]
#     )

# @router.post("/update", response_model=LocationResponse)
# async def update_location(location: LocationUpdate):
#     """
#     Update user location
#     """
#     # בדיקה אם המשתמש קיים
#     user = await users_collection.find_one({"_id": ObjectId(location.user_id)})
#     if not user:
#         raise HTTPException(status_code=404, detail="User not found")

#     location_data = {
#         "user_id": location.user_id,
#         "latitude": location.latitude,
#         "longitude": location.longitude,
#         "last_updated": datetime.utcnow()
#     }
    
#     await locations_collection.insert_one(location_data)
    
#     return LocationResponse(
#         user_id=location_data["user_id"],
#         latitude=location_data["latitude"],
#         longitude=location_data["longitude"],
#         last_updated=location_data["last_updated"],
#         delay_ms=0
#     )