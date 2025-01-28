# """
# Live Location API - FastAPI Application

# This module initializes a FastAPI application for tracking user locations in real-time.
# It sets up CORS middleware, includes routers for users and locations endpoints,
# and configures AWS Lambda handler using Mangum.

# Features:
#     - CORS enabled for all origins
#     - Separate route handlers for users and locations
#     - AWS Lambda compatible using Mangum
#     - Health check endpoint at root URL
# """

# from fastapi import FastAPI
# from fastapi.middleware.cors import CORSMiddleware
# from routes.users import router as users_router
# from routes.locations import router as locations_router
# from mangum import Mangum

# # Initialize FastAPI application with title
# app = FastAPI(title="Live Location API")

# # Configure CORS middleware to allow all origins
# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["*"],  # Allows all origins
#     allow_credentials=True,  # Allows credentials (cookies, authorization headers)
#     allow_methods=["*"],  # Allows all methods
#     allow_headers=["*"],  # Allows all headers
# )

# # Include routers with their respective prefixes and tags
# app.include_router(users_router, prefix="/api/users", tags=["users"])
# app.include_router(locations_router, prefix="/api/locations", tags=["locations"])

# @app.get("/")
# async def read_root():
#     """
#     Root endpoint serving as a health check and welcome message.
    
#     Returns:
#         dict: A welcome message indicating the API is operational
#     """
#     return {"message": "Welcome to Live Location API"}

# # Configure Mangum handler for AWS Lambda compatibility
# handler = Mangum(app, lifespan="off")