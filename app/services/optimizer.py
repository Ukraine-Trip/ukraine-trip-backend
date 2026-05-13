import requests
from typing import List

def get_optimal_order(coordinates: List[dict]) -> List[int]:
    """
    Приймає [{"lat": ..., "lon": ...}, ...]
    Повертає список індексів в оптимізованому порядку.
    """
    # Форматуємо координати для OSRM: lon,lat;lon,lat...
    coords_str = ";".join([f"{c['lon']},{c['lat']}" for c in coordinates])
    
    # Використовуємо сервіс 'trip' для задачі комівояжера
    url = f"http://router.project-osrm.org/trip/v1/driving/{coords_str}"
    
    try:
        # roundtrip=false означає, що нам не треба повертатися в початкову точку
        response = requests.get(url, params={"roundtrip": "false", "source": "first"})
        data = response.json()
        
        if data.get("code") != "Ok":
            return list(range(len(coordinates))) # повертаємо як було, якщо API впало
            
        # Дістаємо оригінальні індекси в новому порядку
        waypoints = data.get("waypoints", [])
        # Сортуємо по waypoint_index (яким він став у маршруті)
        waypoints_sorted = sorted(waypoints, key=lambda x: x["waypoint_index"])
        return [wp["original_index"] for wp in waypoints_sorted]
        
    except Exception:
        return list(range(len(coordinates)))