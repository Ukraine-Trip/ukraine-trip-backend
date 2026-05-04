from pydantic import BaseModel

class Token(BaseModel):
    access_token: str
    token_type: str
    user_id: int
    email: str
    full_name: str
    role: str
