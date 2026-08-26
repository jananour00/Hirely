from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.deps import require_role
from app.core.database import get_db
from app.models.candidate_profile import CandidateProfile
from app.models.user import User, UserRole
from app.schemas.candidate_profile import CandidateProfileOut

router = APIRouter(prefix="/candidates", tags=["candidates"])


@router.get("/{candidate_id}/profile", response_model=CandidateProfileOut)
def get_candidate_profile(
    candidate_id: int,
    db: Session = Depends(get_db),
    user: User = Depends(require_role(UserRole.ADMIN, UserRole.RECRUITER)),  # recruiter-only view
):
    profile = db.query(CandidateProfile).filter(CandidateProfile.candidate_id == candidate_id).first()
    if not profile:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "No profile parsed yet for this candidate")
    return profile