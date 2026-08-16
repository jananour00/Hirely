from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.agents.jd_generator import generate_jd
from app.agents.requirement_extraction import extract_requirements
from app.api.deps import get_current_user
from app.core.database import get_db
from app.models.job import Job, JobStatus
from app.models.user import User
from app.schemas.job import JobApproveRequest, JobCreateRequest, JobOut

router = APIRouter(prefix="/jobs", tags=["jobs"])


@router.post("/", response_model=JobOut)
def create_job(
    payload: JobCreateRequest,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    requirements = extract_requirements(payload.raw_description)
    jd_text = generate_jd(requirements)

    job = Job(
        org_id=user.org_id,
        created_by=user.id,
        title=requirements["title"],
        status=JobStatus.PENDING_APPROVAL,
        requirements_json=requirements,
        jd_text=jd_text,
    )
    db.add(job)
    db.commit()
    db.refresh(job)
    return job


@router.post("/{job_id}/approve", response_model=JobOut)
def approve_job(
    job_id: int,
    payload: JobApproveRequest,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    job = db.get(Job, job_id)
    if not job or job.org_id != user.org_id:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Job not found")

    job.jd_text = payload.jd_text  # recruiter's edited version wins
    job.status = JobStatus.OPEN  # publish to internal portal (FR-3, V1 scope)
    db.commit()
    db.refresh(job)
    return job


@router.get("/", response_model=list[JobOut])
def list_jobs(db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    return db.query(Job).filter(Job.org_id == user.org_id).all()