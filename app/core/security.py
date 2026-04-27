import os
from datetime import datetime, timedelta, timezone
from typing import Any, Union, Optional

from jose import jwt, JWTError
from passlib.context import CryptContext
from dotenv import load_dotenv

# Завантажуємо змінні з .env
load_dotenv()

# Налаштування алгоритму хешування паролів
# bcrypt — це стандарт для безпечного збереження паролів
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Налаштування JWT (беруться з .env)
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 30))

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Перевіряє, чи збігається введений пароль із хешем у базі.
    """
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    """
    Перетворює звичайний пароль у безпечний хеш.
    """
    return pwd_context.hash(password)

def create_access_token(subject: Union[str, Any], expires_delta: timedelta = None) -> str:
    """
    Створює підписаний JWT токен для авторизації користувача.
    :param subject: Зазвичай це email або ID користувача (поле 'sub')
    :param expires_delta: Час життя токена (якщо не вказано, береться з налаштувань)
    """
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(
            minutes=ACCESS_TOKEN_EXPIRE_MINUTES
        )
    
    # Дані, які ми "зашиваємо" в токен
    to_encode = {
        "exp": expire, 
        "sub": str(subject),
        "iat": datetime.now(timezone.utc) # дата видачі
    }
    
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def decode_access_token(token: str) -> Optional[str]:
    """
    Декодує токен і повертає 'sub' (email), якщо токен валідний.
    Використовується для перевірки прав доступу.
    """
    try:
        decoded_token = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return decoded_token.get("sub")
    except JWTError:
        return None