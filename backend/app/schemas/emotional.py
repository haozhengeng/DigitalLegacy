from datetime import datetime
from typing import Optional
from pydantic import BaseModel


class EmotionalFileCreate(BaseModel):
    title: str
    file_type: str
    encrypted_content: str = ""
    mime_type: str = ""
    recipient_beneficiary_id: Optional[str] = None

class EmotionalFileUpdate(BaseModel):
    title: Optional[str] = None
    recipient_beneficiary_id: Optional[str] = None

class EmotionalFileResponse(BaseModel):
    id: str
    user_id: str
    title: str
    file_type: str
    file_path: str
    encrypted_content: str
    mime_type: str
    recipient_beneficiary_id: Optional[str] = None
    is_delivered: bool
    delivered_at: Optional[datetime] = None
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}
