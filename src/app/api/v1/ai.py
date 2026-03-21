from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List
from src.app.services.ai_service import generate_trip_plan

router = APIRouter()

# Описуємо, що чекаємо від фронтенда
class TripRequest(BaseModel):
    city: str
    days: int
    budget: str
    interests: List[str]

@router.post("/generate-route")
async def create_ai_route(request: TripRequest):
    try:
        trip_data = await generate_trip_plan(
            city=request.city,
            days=request.days,
            budget=request.budget,
            interests=request.interests
        )
        return {"status": "success", "data": trip_data}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"AI Error: {str(e)}")