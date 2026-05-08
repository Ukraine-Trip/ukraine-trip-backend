import logging
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import text
from typing import List

from app.db.session import get_db
from app.schemas.city import CityResponse

router = APIRouter()
logger = logging.getLogger(__name__)


@router.get("/", response_model=List[CityResponse])
def get_cities(db: Session = Depends(get_db)):
    col_names: List[str] = db.execute(text(
        "SELECT column_name FROM information_schema.columns "
        "WHERE table_name = 'cities' ORDER BY ordinal_position"
    )).scalars().all()

    logger.warning("cities table columns: %s", col_names)

    lat_col = next((c for c in col_names if "lat" in c.lower()), None)
    lng_col = next((c for c in col_names if "lon" in c.lower() or "lng" in c.lower()), None)

    select_parts = ["id", "name", "region"]
    if lat_col:
        select_parts.append(f"{lat_col} AS lat")
    if lng_col:
        select_parts.append(f"{lng_col} AS lng")

    rows = db.execute(
        text(f"SELECT {', '.join(select_parts)} FROM cities ORDER BY region, name")
    ).mappings().all()

    return [
        CityResponse(
            id=row["id"],
            name=row["name"],
            region=row["region"],
            lat=float(row.get("lat") or 0.0),
            lng=float(row.get("lng") or 0.0),
        )
        for row in rows
    ]