import json
from groq import AsyncGroq
from src.app.core.config import settings

# Ініціалізуємо клієнта Groq
client = AsyncGroq(api_key=settings.GROQ_API_KEY)

SYSTEM_PROMPT = """
Ти професійний туристичний гід по Україні. 
Твоя задача — скласти детальний маршрут на основі побажань користувача.
Ти ПОВИНЕН повернути відповідь ВИКЛЮЧНО у форматі JSON. 
Структура JSON:
{
  "title": "Назва маршруту",
  "description": "Короткий опис",
  "days": [
    {
      "day_number": 1,
      "locations": [
        {"name": "Назва місця", "description": "Чому варто відвідати", "estimated_time_hours": 2}
      ]
    }
  ]
}
"""

async def generate_trip_plan(city: str, days: int, budget: str, interests: list[str]) -> dict:
    user_prompt = f"Склади маршрут в {city} на {days} днів. Бюджет: {budget}. Інтереси: {', '.join(interests)}."
    
    response = await client.chat.completions.create(
        model="llama-3.3-70b-versatile", # Найпотужніша і найшвидша модель зараз
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_prompt}
        ],
        response_format={"type": "json_object"}, # Змушуємо віддати чистий JSON
        temperature=0.7
    )
    
    return json.loads(response.choices[0].message.content)