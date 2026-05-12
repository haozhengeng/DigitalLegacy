import uuid
from datetime import datetime
from sqlalchemy import String, DateTime, Text, ForeignKey, Boolean
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class Beneficiary(Base):
    """受益人模型：存储受益人的身份信息、权限分配及认证状态"""
    __tablename__ = "beneficiaries"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id: Mapped[str] = mapped_column(String(36), ForeignKey("users.id"), nullable=False, index=True)

    name: Mapped[str] = mapped_column(String(100), nullable=False)
    email: Mapped[str] = mapped_column(String(255), nullable=False)
    phone: Mapped[str] = mapped_column(String(20), default="")
    relation: Mapped[str] = mapped_column(String(100), default="")

    id_number: Mapped[str] = mapped_column(String(50), default="")
    is_identity_verified: Mapped[bool] = mapped_column(Boolean, default=False)

    permission_vault: Mapped[bool] = mapped_column(Boolean, default=False)
    permission_emotional: Mapped[bool] = mapped_column(Boolean, default=False)
    permission_key_fragments: Mapped[bool] = mapped_column(Boolean, default=False)

    is_notified: Mapped[bool] = mapped_column(Boolean, default=False)
    notified_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)

    notes: Mapped[str] = mapped_column(Text, default="")
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    user = relationship("User", back_populates="beneficiaries")
