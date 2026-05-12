from datetime import datetime
from typing import Optional
from pydantic import BaseModel


class TriggerConfigUpdate(BaseModel):
    """更新生命开关配置请求（所有字段可选）"""
    is_enabled: Optional[bool] = None
    inactivity_days: Optional[int] = None
    check_in_interval_days: Optional[int] = None
    alert_t0_push: Optional[bool] = None
    alert_t3_sms: Optional[bool] = None
    alert_t7_contact: Optional[bool] = None

class TriggerConfigResponse(BaseModel):
    """生命开关配置响应"""
    id: str
    user_id: str
    is_enabled: bool
    inactivity_days: int
    check_in_interval_days: int
    alert_t0_push: bool
    alert_t3_sms: bool
    alert_t7_contact: bool
    last_check_in: Optional[datetime] = None
    trigger_started_at: Optional[datetime] = None
    trigger_completed_at: Optional[datetime] = None
    is_triggered: bool
    is_emergency_recalled: bool
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}

class CheckInResponse(BaseModel):
    """安全打卡响应"""
    message: str
    last_check_in: datetime

class TriggerLogResponse(BaseModel):
    """触发事件日志响应"""
    id: str
    user_id: str
    event_type: str
    description: str
    metadata_json: str
    created_at: datetime

    model_config = {"from_attributes": True}

class EmergencyRecallResponse(BaseModel):
    """紧急撤回响应"""
    message: str
    is_emergency_recalled: bool

class TriggerStatusResponse(BaseModel):
    """生命开关状态响应"""
    is_triggered: bool
    is_emergency_recalled: bool
    days_since_last_checkin: int
    inactivity_days: int
    trigger_stage: str
    next_alert_at: Optional[str] = None
