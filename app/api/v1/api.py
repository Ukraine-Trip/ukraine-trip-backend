from fastapi import APIRouter
from app.api.v1.endpoints import users, auth, locations, trips, bookmarks, cities

api_router = APIRouter()

api_router.include_router(auth.router, prefix="/auth", tags=["Auth"])
api_router.include_router(users.router, prefix="/users", tags=["Users"])
api_router.include_router(bookmarks.router, prefix="/bookmarks", tags=["Bookmarks"])
api_router.include_router(trips.router, prefix="/trips", tags=["Trips"])
api_router.include_router(locations.router, prefix="/locations", tags=["Locations"])
api_router.include_router(cities.router, prefix="/cities", tags=["Cities"])