from datetime import datetime
from typing import Optional
from pydantic import BaseModel, EmailStr


class UserCreate(BaseModel):
    """用户注册请求"""
    email: EmailStr
    username: str
    password: str
    display_name: str = ""

class UserLogin(BaseModel):
    """用户登录请求"""
    email: EmailStr
    password: str

class MFAEnable(BaseModel):
    """开启 MFA 请求"""
    secret: str
    code: str

class MFAVerify(BaseModel):
    """MFA 验证码校验请求"""
    code: str

class UserUpdate(BaseModel):
    """用户资料更新请求"""
    display_name: Optional[str] = None
    phone: Optional[str] = None
    avatar_url: Optional[str] = None
    inactivity_grace_days: Optional[int] = None
    emergency_contact_name: Optional[str] = None
    emergency_contact_phone: Optional[str] = None

class UserResponse(BaseModel):
    """用户信息响应"""
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
    """JWT 令牌响应"""
    access_token: str
    token_type: str = "bearer"
    user: UserResponse
