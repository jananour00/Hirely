from pydantic import BaseModel

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