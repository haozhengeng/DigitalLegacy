import uuid
from datetime import datetime
from sqlalchemy import String, DateTime, Boolean, Text, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class User(Base):
    __tablename__ = "users"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    email: Mapped[str] = mapped_column(String(255), unique=True, index=True, nullable=False)
    username: Mapped[str] = mapped_column(String(100), unique=True, index=True, nullable=False)
    hashed_password: Mapped[str] = mapped_column(String(255), nullable=False)
    display_name: Mapped[str] = mapped_column(String(100), default="")
    phone: Mapped[str] = mapped_column(String(20), default="")
    avatar_url: Mapped[str] = mapped_column(String(500), default="")

    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    is_verified: Mapped[bool] = mapped_column(Boolean, default=False)
    is_mfa_enabled: Mapped[bool] = mapped_column(Boolean, default=False)
    mfa_secret: Mapped[str] = mapped_column(String(100), default="")

    last_login_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    is_alive: Mapped[bool] = mapped_column(Boolean, default=True)
    inactivity_grace_days: Mapped[int] = mapped_column(Integer, default=90)

    emergency_contact_name: Mapped[str] = mapped_column(String(100), default="")
    emergency_contact_phone: Mapped[str] = mapped_column(String(20), default="")

    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    vault_items = relationship("VaultItem", back_populates="user", cascade="all, delete-orphan")
    emotional_files = relationship("EmotionalFile", back_populates="user", cascade="all, delete-orphan")
    key_fragments = relationship("KeyFragment", back_populates="user", cascade="all, delete-orphan")
    beneficiaries = relationship("Beneficiary", back_populates="user", cascade="all, delete-orphan")
    trigger_config = relationship("TriggerConfig", back_populates="user", uselist=False, cascade="all, delete-orphan")
    trigger_logs = relationship("TriggerLog", back_populates="user", cascade="all, delete-orphan")
