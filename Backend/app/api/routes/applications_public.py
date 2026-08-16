from datetime import datetime, timezone

from fastapi import APIRouter, Depends, File, Form, HTTPException, UploadFile, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.storage import save_resume
from app.models.application import Application, ApplicationStatus
from app.models.audit_log import AuditLog
from app.models.candidate import Candidate
from app.models.job import Job, JobStatus
from app.models.resume import Resume
from app.schemas.application import ApplicationOut

router = APIRouter(prefix="/apply", tags=["candidate-application"])


@router.post("/", response_model=ApplicationOut)
def apply_to_job(
    job_id: int = Form(...),
    candidate_name: str = Form(...),
    candidate_email: str = Form(...),
    consent: bool = Form(...),
    resume: UploadFile = File(...),
    db: Session = Depends(get_db),
):
    if not consent:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, "Consent is required to apply")

    job = db.get(Job, job_id)
    if not job or job.status != JobStatus.OPEN:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Job not open for applications")

    candidate = db.query(Candidate).filter(Candidate.email == candidate_email).first()
    if not candidate:
        candidate = Candidate(email=candidate_email, name=candidate_name)
        db.add(candidate)
        db.flush()

    existing = (
        db.query(Application)
        .filter(Application.job_id == job_id, Application.candidate_id == candidate.id)
        .first()
    )
    if existing:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, "Already applied to this job")

    try:
        file_url = save_resume(resume)
    except ValueError as e:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, str(e))

    db.add(Resume(candidate_id=candidate.id, file_url=file_url))

    application = Application(
        job_id=job_id,
        candidate_id=candidate.id,
        status=ApplicationStatus.APPLIED,
        consent_given_at=datetime.now(timezone.utc),
    )
    db.add(application)
    db.flush()

    db.add(AuditLog(
        actor_type="human",
        actor_id=candidate.id,
        action="application_submitted",
        entity="application",
        entity_id=application.id,
    ))

    db.commit()
    db.refresh(application)
    return application