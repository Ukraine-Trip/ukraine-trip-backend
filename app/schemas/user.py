from typing import Optional
from pydantic import BaseModel, EmailStr, ConfigDict, field_validator


ALLOWED_DOMAINS = ["gmail.com"]

# Тільки email
class UserBase(BaseModel):
    email: EmailStr
    full_name: str

    @field_validator('email')
    @classmethod
    def validate_email_domain(cls, v: str) -> str:
        domain = v.split('@')[-1]
        if domain not in ALLOWED_DOMAINS:
            raise ValueError(f"Дозволені тільки наступні поштові домени: {', '.join(ALLOWED_DOMAINS)}")
        return v

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