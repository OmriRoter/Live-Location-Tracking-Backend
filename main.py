"""
Live Location API - Main Application Module

A FastAPI application for handling real-time location tracking.
Provides endpoints for user management and location updates with CORS support
for cross-platform accessibility.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes.users import router as users_router
from routes.locations import router as locations_router

# Initialize FastAPI application
app = FastAPI(title="Live Location API")

# Configure CORS middleware to enable cross-origin requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],      # Allow requests from any origin
    allow_credentials=True,   # Allow credentials (cookies, authorization headers)
    allow_methods=["*"],      # Allow all HTTP methods
    allow_headers=["*"],      # Allow all HTTP headers
)

# Register route handlers
app.include_router(users_router, prefix="/api/users", tags=["users"])
app.include_router(locations_router, prefix="/api/locations", tags=["locations"])

@app.get("/")
async def root():
    """
    Health check endpoint to verify API availability.
    
    Returns:
        dict: A message indicating the server status
    """
    return {"message": "Server is up!"}