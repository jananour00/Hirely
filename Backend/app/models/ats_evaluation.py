from datetime import datetime, timezone

from sqlalchemy import JSON, DateTime, Float, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base


class ATSEvaluation(Base):
    __tablename__ = "ats_evaluations"

    id: Mapped[int] = mapped_column(primary_key=True)
    application_id: Mapped[int] = mapped_column(ForeignKey("applications.id"), unique=True)
    overall_score: Mapped[float] = mapped_column(Float)
    dimension_scores_json: Mapped[dict] = mapped_column(JSON, default=dict)
    strengths: Mapped[list] = mapped_column(JSON, default=list)
    gaps: Mapped[list] = mapped_column(JSON, default=list)
    computed_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(timezone.utc)
    )

    application: Mapped["Application"] = relationship(back_populates="ats_evaluation")  # noqa: F821
