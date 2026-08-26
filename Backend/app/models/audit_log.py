from datetime import datetime, timezone

from sqlalchemy import DateTime, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base


class AuditLog(Base):
    __tablename__ = "audit_logs"

    id: Mapped[int] = mapped_column(primary_key=True)
    actor_type: Mapped[str] = mapped_column(String(50))  # "human" | "agent"
    actor_id: Mapped[int] = mapped_column(Integer)
    action: Mapped[str] = mapped_column(String(255))
    entity: Mapped[str] = mapped_column(String(100))
    entity_id: Mapped[int] = mapped_column(Integer)
    timestamp: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(timezone.utc)
    )
