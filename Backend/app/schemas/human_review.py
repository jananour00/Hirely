from datetime import datetime

from pydantic import BaseModel

from app.models.human_review import ReviewDecision


class ApplicationReviewOut(BaseModel):
    """What a recruiter sees at the Human Review gate: the AI's evidence, not just a bare score."""

    application_id: int
    application_status: str
    candidate_id: int
    overall_score: float | None
    dimension_scores: dict | None
    strengths: list | None
    gaps: list | None


class HumanReviewRequest(BaseModel):
    decision: ReviewDecision
    notes: str | None = None


class HumanReviewOut(BaseModel):
    id: int
    application_id: int
    reviewer_id: int
    decision: ReviewDecision
    notes: str | None
    decided_at: datetime

    model_config = {"from_attributes": True}
