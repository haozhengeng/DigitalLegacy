import uuid
from datetime import datetime
from sqlalchemy import String, DateTime, ForeignKey, Boolean, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class TriggerConfig(Base):
    """生命开关配置模型：管理安全打卡周期、预警通知策略和触发状态"""
    __tablename__ = "trigger_configs"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id: Mapped[str] = mapped_column(String(36), ForeignKey("users.id"), unique=True, nullable=False, index=True)

    is_enabled: Mapped[bool] = mapped_column(Boolean, default=True)
    inactivity_days: Mapped[int] = mapped_column(Integer, default=90)
    check_in_interval_days: Mapped[int] = mapped_column(Integer, default=90)

    alert_t0_push: Mapped[bool] = mapped_column(Boolean, default=True)
    alert_t3_sms: Mapped[bool] = mapped_column(Boolean, default=True)
    alert_t7_contact: Mapped[bool] = mapped_column(Boolean, default=True)

    last_check_in: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    trigger_started_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    trigger_completed_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)

    is_triggered: Mapped[bool] = mapped_column(Boolean, default=False)
    is_emergency_recalled: Mapped[bool] = mapped_column(Boolean, default=False)

    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    user = relationship("User", back_populates="trigger_config")
