from pydantic import BaseModel, EmailStr, ConfigDict


# Тільки email
class UserBase(BaseModel):
    email: EmailStr

# Для реєстрації додаємо тільки пароль
class UserCreate(UserBase):
    password: str

# Для відповіді (що бачить клієнт)
class UserResponse(UserBase):
    id: int
    

    model_config = ConfigDict(from_attributes=True)