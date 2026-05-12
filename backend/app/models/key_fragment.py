import uuid
from datetime import datetime
from sqlalchemy import String, DateTime, Text, ForeignKey, Boolean, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class KeyFragment(Base):
    __tablename__ = "key_fragments"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id: Mapped[str] = mapped_column(String(36), ForeignKey("users.id"), nullable=False, index=True)

    title: Mapped[str] = mapped_column(String(200), nullable=False)
    fragment_type: Mapped[str] = mapped_column(String(20), nullable=False)
    fragment_index: Mapped[int] = mapped_column(Integer, default=1)
    total_fragments: Mapped[int] = mapped_column(Integer, default=2)
    encrypted_data: Mapped[str] = mapped_column(Text, default="")
    storage_location: Mapped[str] = mapped_column(String(200), default="")

    is_physical_copy: Mapped[bool] = mapped_column(Boolean, default=False)
    is_delivered: Mapped[bool] = mapped_column(Boolean, default=False)

    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    user = relationship("User", back_populates="key_fragments")
