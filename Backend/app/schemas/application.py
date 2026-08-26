from datetime import datetime

from pydantic import BaseModel

from app.models.application import ApplicationStatus


class ApplicationOut(BaseModel):
    id: int
    job_id: int
    candidate_id: int
    status: ApplicationStatus
    submitted_at: datetime

    model_config = {"from_attributes": True}
