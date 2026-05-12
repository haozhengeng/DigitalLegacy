from datetime import datetime
from typing import Optional
from pydantic import BaseModel, EmailStr


class BeneficiaryCreate(BaseModel):
    """创建受益人请求"""
    name: str
    email: EmailStr
    phone: str = ""
    relation: str = ""
    permission_vault: bool = False
    permission_emotional: bool = False
    permission_key_fragments: bool = False
    notes: str = ""

class BeneficiaryUpdate(BaseModel):
    """更新受益人请求（所有字段可选）"""
    name: Optional[str] = None
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    relation: Optional[str] = None
    permission_vault: Optional[bool] = None
    permission_emotional: Optional[bool] = None
    permission_key_fragments: Optional[bool] = None
    notes: Optional[str] = None

class BeneficiaryVerify(BaseModel):
    """受益人实名认证请求"""
    id_number: str

class BeneficiaryResponse(BaseModel):
    """受益人信息响应"""
    id: str
    user_id: str
    name: str
    email: str
    phone: str
    relation: str
    id_number: str
    is_identity_verified: bool
    permission_vault: bool
    permission_emotional: bool
    permission_key_fragments: bool
    is_notified: bool
    notified_at: Optional[datetime] = None
    notes: str
    created_at: datetime

    model_config = {"from_attributes": True}
