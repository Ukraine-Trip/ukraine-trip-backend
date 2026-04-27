from fastapi import Depends, HTTPException, status, Path
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from sqlalchemy.orm import Session
from uuid import UUID

from app.db.session import get_db
from app.core import security
from app.models.user import User

# Вказуємо Swagger, куди стукати за токеном
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")

def get_current_user(db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)) -> User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Не вдалося перевірити облікові дані",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, security.SECRET_KEY, algorithms=[security.ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
        
    user = db.query(User).filter(User.email == email).first()
    if user is None:
        raise credentials_exception
    return user

def get_trip_and_check_owner(
    trip_id: UUID = Path(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    # 1. Шукаємо маршрут у базі
    trip = crud_trip.get_trip(db, trip_id=trip_id)
    
    if not trip:
        raise HTTPException(status_code=404, detail="Маршрут не знайдено")
        
    # 2. Перевіряємо, чи юзер є власником
    if trip.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Ви не можете редагувати чужий маршрут")
        
    return trip