from sqlalchemy.orm import Session

from app.models.ats_evaluation import ATSEvaluation
from app.models.candidate_ranking import CandidateRanking


def recompute_rankings(db: Session, job_id: int) -> list[CandidateRanking]:
    """
    Re-ranks every scored application for a job (FR-7).
    Called whenever a new application finishes ATS_SCREENING.
    """
    evaluations = (
        db.query(ATSEvaluation)
        .join(ATSEvaluation.application)
        .filter_by(job_id=job_id)
        .order_by(ATSEvaluation.overall_score.desc())
        .all()
    )

    # Clear previous ranking rows for this job, recompute fresh
    db.query(CandidateRanking).filter(CandidateRanking.job_id == job_id).delete()

    rankings = []
    for position, evaluation in enumerate(evaluations, start=1):
        ranking = CandidateRanking(
            job_id=job_id,
            application_id=evaluation.application_id,
            rank=position,
        )
        db.add(ranking)
        rankings.append(ranking)

    db.flush()
    return rankings