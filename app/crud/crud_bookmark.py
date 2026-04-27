from sqlalchemy.orm import Session
from uuid import UUID
from app.models.bookmark import Bookmark

def create_bookmark(db: Session, user_id: int, location_id: UUID):
    # Перевіряємо, чи вже є така закладка у цього юзера
    existing_bookmark = db.query(Bookmark).filter(
        Bookmark.user_id == user_id,
        Bookmark.location_id == location_id
    ).first()
    
    # Якщо вже є - просто повертаємо її (щоб не кидати помилку, якщо юзер клікне двічі)
    if existing_bookmark:
        return existing_bookmark

    # Якщо немає - створюємо нову
    new_bookmark = Bookmark(user_id=user_id, location_id=location_id)
    db.add(new_bookmark)
    db.commit()
    db.refresh(new_bookmark)
    
    return new_bookmark