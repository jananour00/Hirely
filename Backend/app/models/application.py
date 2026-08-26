import enum
from datetime import datetime, timezone

from sqlalchemy import DateTime, Enum, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base


class ApplicationStatus(str, enum.Enum):
    APPLIED = "applied"
    CV_PROCESSING = "cv_processing"
    ATS_SCREENING = "ats_screening"
    HUMAN_REVIEW = "human_review"
    AI_INTERVIEW = "ai_interview"
    INTERVIEW_EVALUATION = "interview_evaluation"
    HR_SCHEDULING = "hr_scheduling"
    HR_INTERVIEW = "hr_interview"
    OFFER = "offer"
    HIRED = "hired"
    REJECTED = "rejected"


class Application(Base):
    __tablename__ = "applications"

    id: Mapped[int] = mapped_column(primary_key=True)
    job_id: Mapped[int] = mapped_column(ForeignKey("jobs.id"))
    candidate_id: Mapped[int] = mapped_column(ForeignKey("candidates.id"))
    status: Mapped[ApplicationStatus] = mapped_column(
        Enum(ApplicationStatus), default=ApplicationStatus.APPLIED
    )
    consent_given_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    submitted_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(timezone.utc)
    )

    job: Mapped["Job"] = relationship(back_populates="applications")  # noqa: F821
    candidate: Mapped["Candidate"] = relationship(back_populates="applications")  # noqa: F821
    ats_evaluation: Mapped["ATSEvaluation"] = relationship(  # noqa: F821
        back_populates="application", uselist=False
    )
