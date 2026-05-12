from datetime import datetime
from typing import Optional
from pydantic import BaseModel, EmailStr


class UserCreate(BaseModel):
    email: EmailStr
    username: str
    password: str
    display_name: str = ""

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class MFAEnable(BaseModel):
    secret: str
    code: str

class MFAVerify(BaseModel):
    code: str

class UserUpdate(BaseModel):
    display_name: Optional[str] = None
    phone: Optional[str] = None
    avatar_url: Optional[str] = None
    inactivity_grace_days: Optional[int] = None
    emergency_contact_name: Optional[str] = None
    emergency_contact_phone: Optional[str] = None

class UserResponse(BaseModel):
    id: str
    email: str
    username: str
    display_name: str
    phone: str
    avatar_url: str
    is_active: bool
    is_verified: bool
    is_mfa_enabled: bool
    is_alive: bool
    inactivity_grace_days: int
    last_login_at: Optional[datetime] = None
    emergency_contact_name: str
    emergency_contact_phone: str
    created_at: datetime

    model_config = {"from_attributes": True}

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: UserResponse
