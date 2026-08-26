from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.agents.jd_generator import generate_jd
from app.agents.requirement_extraction import extract_requirements
from app.api.deps import require_role
from app.core.database import get_db
from app.models.application import Application
from app.models.candidate import Candidate
from app.models.job import Job, JobStatus
from app.models.user import User, UserRole
from app.schemas.job import (
    JobApplicationSummaryOut,
    JobApproveRequest,
    JobCreateRequest,
    JobOut,
    JobPublicOut,
)

router = APIRouter(prefix="/jobs", tags=["jobs"])


# NOTE: "/public" must be declared before "/{job_id}" — Starlette matches routes
# in registration order, so a param route declared first would swallow this path.
@router.get("/public", response_model=list[JobPublicOut])
def list_public_jobs(db: Session = Depends(get_db)):
    """Open jobs for the candidate-facing careers site. No auth — added for the
    frontend's /careers listing, which has nothing else to read published jobs from."""
    return db.query(Job).filter(Job.status == JobStatus.OPEN).order_by(Job.created_at.desc()).all()


@router.get("/{job_id}/public", response_model=JobPublicOut)
def get_public_job(job_id: int, db: Session = Depends(get_db)):
    """Single open job for the careers detail/apply page. No auth."""
    job = db.get(Job, job_id)
    if not job or job.status != JobStatus.OPEN:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Job not found")
    return job


@router.post("/", response_model=JobOut)
def create_job(
    payload: JobCreateRequest,
    db: Session = Depends(get_db),
    user: User = Depends(require_role(UserRole.ADMIN, UserRole.RECRUITER)),
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
    user: User = Depends(require_role(UserRole.ADMIN, UserRole.RECRUITER)),
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
def list_jobs(
    db: Session = Depends(get_db),
    user: User = Depends(require_role(UserRole.ADMIN, UserRole.RECRUITER)),
):
    return db.query(Job).filter(Job.org_id == user.org_id).order_by(Job.created_at.desc()).all()


@router.get("/{job_id}", response_model=JobOut)
def get_job(
    job_id: int,
    db: Session = Depends(get_db),
    user: User = Depends(require_role(UserRole.ADMIN, UserRole.RECRUITER)),
):
    job = db.get(Job, job_id)
    if not job or job.org_id != user.org_id:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Job not found")
    return job


@router.get("/{job_id}/applications", response_model=list[JobApplicationSummaryOut])
def list_job_applications(
    job_id: int,
    db: Session = Depends(get_db),
    user: User = Depends(require_role(UserRole.ADMIN, UserRole.RECRUITER)),
):
    """Review queue for a job — added for the recruiter dashboard, which has no
    other way to see which candidates applied to a given job."""
    job = db.get(Job, job_id)
    if not job or job.org_id != user.org_id:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Job not found")

    rows = (
        db.query(Application, Candidate)
        .join(Candidate, Application.candidate_id == Candidate.id)
        .filter(Application.job_id == job_id)
        .order_by(Application.submitted_at.desc())
        .all()
    )

    results = []
    for application, candidate in rows:
        results.append(
            JobApplicationSummaryOut(
                application_id=application.id,
                candidate_id=candidate.id,
                candidate_name=candidate.name,
                candidate_email=candidate.email,
                status=application.status,
                submitted_at=application.submitted_at,
                overall_score=application.ats_evaluation.overall_score
                if application.ats_evaluation
                else None,
            )
        )
    return results