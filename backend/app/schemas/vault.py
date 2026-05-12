from datetime import datetime
from typing import Optional
from pydantic import BaseModel

CATEGORY_CHOICES = [
    "bank", "crypto", "insurance", "social",
    "email", "cloud", "subscription", "instruction", "other",
]

class VaultItemCreate(BaseModel):
    """创建保险箱条目请求"""
    title: str
    category: str = "other"
    sub_category: str = ""
    encrypted_content: str = ""
    encrypted_note: str = ""
    platform_name: str = ""
    platform_url: str = ""
    account_name: str = ""
    importance: int = 1
    is_legacy: bool = False

class VaultItemUpdate(BaseModel):
    """更新保险箱条目请求（所有字段可选）"""
    title: Optional[str] = None
    category: Optional[str] = None
    sub_category: Optional[str] = None
    encrypted_content: Optional[str] = None
    encrypted_note: Optional[str] = None
    platform_name: Optional[str] = None
    platform_url: Optional[str] = None
    account_name: Optional[str] = None
    importance: Optional[int] = None
    is_legacy: Optional[bool] = None

class VaultItemResponse(BaseModel):
    """保险箱条目响应"""
    id: str
    user_id: str
    title: str
    category: str
    sub_category: str
    encrypted_content: str
    encrypted_note: str
    platform_name: str
    platform_url: str
    account_name: str
    importance: int
    is_legacy: bool
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}
