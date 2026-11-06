from datetime import datetime
from pydantic import BaseModel, EmailStr,Field,ConfigDict

class RegisterRequest(BaseModel):
    email: EmailStr
    password: str = Field(min_length=8, max_length=128)
    
class UserResponse(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
    
class LoginRequest(BaseModel):
    email: EmailStr
    password: str = Field(min_length=8, max_length=128)
    
class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"