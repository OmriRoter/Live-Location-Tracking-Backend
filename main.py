from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes.users import router as users_router
from routes.locations import router as locations_router

app = FastAPI(title="Live Location API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(users_router, prefix="/api/users", tags=["users"])
app.include_router(locations_router, prefix="/api/locations", tags=["locations"])

@app.get("/")
async def read_root():
    return {"message": "Welcome to Live Location API"}