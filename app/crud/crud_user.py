from typing import Optional
from sqlalchemy.orm import Session

from app.models.user import User
from app.schemas.user import UserCreate
from app.core.security import get_password_hash

def get_user_by_email(db: Session, email: str) -> Optional[User]:
    return db.query(User).filter(User.email == email).first()

def create_user(db: Session, user_in: UserCreate) -> User:
    db_user = User(
        email=user_in.email,
        hashed_password=get_password_hash(user_in.password)
        full_name=user_in.full_name
        # база даних автоматично залишить їх порожніми (NULL).
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user