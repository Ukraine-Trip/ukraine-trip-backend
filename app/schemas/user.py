from typing import Optional
from pydantic import BaseModel, EmailStr, ConfigDict


# Тільки email
class UserBase(BaseModel):
    email: EmailStr
    full_name: str

# Для реєстрації додаємо тільки пароль
class UserCreate(UserBase):
    password: str

# Для оновлення даних користувача
class UserUpdate(BaseModel):
    full_name: Optional[str] = None
    password: Optional[str] = None

# Для відповіді (що бачить клієнт)
class UserResponse(UserBase):
    id: int
    
    model_config = ConfigDict(from_attributes=True)