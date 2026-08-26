from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.deps import get_current_user, require_role
from app.core.database import get_db
from app.models.application import Application, ApplicationStatus
from app.models.ats_evaluation import ATSEvaluation
from app.models.audit_log import AuditLog
from app.models.human_review import HumanReview, ReviewDecision
from app.models.user import User, UserRole
from app.schemas.human_review import ApplicationReviewOut, HumanReviewOut, HumanReviewRequest
from orchestrator.engine import advance_application

router = APIRouter(prefix="/applications", tags=["applications"])


@router.post("/{application_id}/advance")
def advance(
    application_id: int,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    application = db.get(Application, application_id)
    if not application:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Application not found")
    application = advance_application(db, application)
    return {"id": application.id, "status": application.status}


@router.get("/{application_id}/review", response_model=ApplicationReviewOut)
def get_review(
    application_id: int,
    db: Session = Depends(get_db),
    user: User = Depends(require_role(UserRole.ADMIN, UserRole.RECRUITER)),
):
    """
    Human Review gate (FR-8): shows the recruiter the AI's match score,
    per-dimension evidence, strengths, and gaps — never a bare percentage.
    """
    application = db.get(Application, application_id)
    if not application:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Application not found")

    evaluation = (
        db.query(ATSEvaluation)
        .filter(ATSEvaluation.application_id == application_id)
        .first()
    )

    return ApplicationReviewOut(
        application_id=application.id,
        application_status=application.status.value,
        candidate_id=application.candidate_id,
        overall_score=evaluation.overall_score if evaluation else None,
        dimension_scores=evaluation.dimension_scores_json if evaluation else None,
        strengths=evaluation.strengths if evaluation else None,
        gaps=evaluation.gaps if evaluation else None,
    )


@router.post("/{application_id}/review", response_model=HumanReviewOut)
def submit_review(
    application_id: int,
    payload: HumanReviewRequest,
    db: Session = Depends(get_db),
    user: User = Depends(require_role(UserRole.ADMIN, UserRole.RECRUITER)),
):
    """
    The only way an application can leave HUMAN_REVIEW (see orchestrator/engine.py —
    HUMAN_REVIEW is deliberately absent from TRANSITIONS). Every decision is
    logged with a reviewer_id and timestamp per NFR: Auditability, and no
    candidate reaches REJECTED without this logged human action (NFR).
    """
    application = db.get(Application, application_id)
    if not application:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Application not found")
    if application.status != ApplicationStatus.HUMAN_REVIEW:
        raise HTTPException(
            status.HTTP_400_BAD_REQUEST,
            f"Application is in {application.status.value}, not awaiting human review",
        )

    review = HumanReview(
        application_id=application.id,
        reviewer_id=user.id,
        decision=payload.decision,
        notes=payload.notes,
    )
    db.add(review)

    if payload.decision in (ReviewDecision.APPROVE, ReviewDecision.ADVANCE):
        application.status = ApplicationStatus.AI_INTERVIEW
    elif payload.decision == ReviewDecision.REJECT:
        application.status = ApplicationStatus.REJECTED
    # REQUEST_INFO: stays in HUMAN_REVIEW; the decision is just logged.

    db.add(AuditLog(
        actor_type="human",
        actor_id=user.id,
        action=f"human_review:{payload.decision.value}",
        entity="application",
        entity_id=application.id,
    ))

    db.commit()
    db.refresh(review)
    return review