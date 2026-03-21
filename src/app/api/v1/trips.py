from fastapi import APIRouter

router = APIRouter()

#для розробника (Logic):
# 1. Створити схеми Trip та Location у папці schemas/
# 2. Зробити мок-дані (фейкові списки) для тестування фронтендом

@router.get("/")
async def get_all_trips():
    """Отримати список всіх маршрутів"""
    return [
        {"id": 1, "name": "Вікенд у Львові", "days": 2},
        {"id": 2, "name": "Замки Закарпаття", "days": 3}
    ]

@router.get("/{trip_id}")
async def get_trip_details(trip_id: int):
    """Отримати деталі конкретного маршруту по ID"""
    return {"id": trip_id, "name": "Тестовий тур", "description": "Опис..."}