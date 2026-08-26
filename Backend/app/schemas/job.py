from datetime import datetime

from pydantic import BaseModel

from app.models.application import ApplicationStatus
from app.models.job import JobStatus


class JobCreateRequest(BaseModel):
    raw_description: str  # free-text HR input, e.g. "Senior backend engineer, 5+ yrs, Python/FastAPI..."


class JobOut(BaseModel):
    id: int
    title: str
    status: JobStatus
    requirements_json: dict | None
    jd_text: str | None

    model_config = {"from_attributes": True}


class JobApproveRequest(BaseModel):
    jd_text: str  # recruiter-edited final JD before publish


class JobPublicOut(BaseModel):
    """What a candidate sees on the careers site — no org internals."""

    id: int
    title: str
    jd_text: str | None

    model_config = {"from_attributes": True}


class JobApplicationSummaryOut(BaseModel):
    """One row in a recruiter's review queue for a job."""

    application_id: int
    candidate_id: int
    candidate_name: str
    candidate_email: str
    status: ApplicationStatus
    submitted_at: datetime
    overall_score: float | None