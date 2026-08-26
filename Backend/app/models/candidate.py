from datetime import datetime, timezone

from sqlalchemy import DateTime, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base


class Candidate(Base):
    __tablename__ = "candidates"

    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(String(255), unique=True, index=True)
    name: Mapped[str] = mapped_column(String(255))
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(timezone.utc)
    )

    resumes: Mapped[list["Resume"]] = relationship(back_populates="candidate")  # noqa: F821
    applications: Mapped[list["Application"]] = relationship(back_populates="candidate")  # noqa: F821
    profile: Mapped["CandidateProfile"] = relationship(  # noqa: F821
        back_populates="candidate", uselist=False
    )
