import uuid
from datetime import datetime
from sqlalchemy import String, DateTime, Text, ForeignKey, Integer, Boolean
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class VaultItem(Base):
    __tablename__ = "vault_items"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id: Mapped[str] = mapped_column(String(36), ForeignKey("users.id"), nullable=False, index=True)

    title: Mapped[str] = mapped_column(String(200), nullable=False)
    category: Mapped[str] = mapped_column(String(50), nullable=False, index=True)
    sub_category: Mapped[str] = mapped_column(String(50), default="")

    encrypted_content: Mapped[str] = mapped_column(Text, default="")
    encrypted_note: Mapped[str] = mapped_column(Text, default="")

    platform_name: Mapped[str] = mapped_column(String(200), default="")
    platform_url: Mapped[str] = mapped_column(String(500), default="")
    account_name: Mapped[str] = mapped_column(String(200), default="")

    importance: Mapped[int] = mapped_column(Integer, default=1)
    is_legacy: Mapped[bool] = mapped_column(Boolean, default=False)

    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    user = relationship("User", back_populates="vault_items")
