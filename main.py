from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes.users import router as users_router
from routes.locations import router as locations_router
from database import connect_and_check

app = FastAPI(title="Live Location API")

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Routes
app.include_router(users_router, prefix="/api/users", tags=["users"])
app.include_router(locations_router, prefix="/api/locations", tags=["locations"])

@app.on_event("startup")
async def startup_event():
    await connect_and_check()

@app.get("/")
async def read_root():
    return {"message": "Welcome to Live Location API"}