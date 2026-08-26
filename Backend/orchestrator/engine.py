from datetime import datetime, timezone

from sqlalchemy.orm import Session

from app.agents.ats_matcher import score_candidate
from app.agents.cv_parser import parse_cv
from app.core.text_extraction import extract_text_from_file
from app.models.agent import AgentExecution
from app.models.application import Application, ApplicationStatus
from app.models.ats_evaluation import ATSEvaluation
from app.models.audit_log import AuditLog
from app.models.candidate_profile import CandidateProfile
from app.models.job import Job
from app.models.resume import Resume
from app.services.ranking import recompute_rankings

TRANSITIONS = {
    ApplicationStatus.APPLIED: ApplicationStatus.CV_PROCESSING,
    ApplicationStatus.CV_PROCESSING: ApplicationStatus.ATS_SCREENING,
    ApplicationStatus.ATS_SCREENING: ApplicationStatus.HUMAN_REVIEW,
    # HUMAN_REVIEW deliberately has no auto-transition here — a candidate can
    # only leave this stage via a logged HumanReview decision
    # (see app/api/routes/applications.py: POST /applications/{id}/review),
    # per NFR: no agent may move a candidate past this gate on its own.
    #
    # Everything below is real FSM shape from the SRS (2.7.3) but still runs
    # on the generic stub agent (run_stub_agent) until the interview /
    # scheduling / offer agents are built (FR-9, FR-10, FR-12) — wired here so
    # the pipeline shape is demoable end-to-end, upgrade agents one at a time.
    ApplicationStatus.AI_INTERVIEW: ApplicationStatus.INTERVIEW_EVALUATION,
    ApplicationStatus.INTERVIEW_EVALUATION: ApplicationStatus.HR_SCHEDULING,
    ApplicationStatus.HR_SCHEDULING: ApplicationStatus.HR_INTERVIEW,
    ApplicationStatus.HR_INTERVIEW: ApplicationStatus.OFFER,
    ApplicationStatus.OFFER: ApplicationStatus.HIRED,
}


def run_stub_agent(db: Session, application: Application, agent_name: str) -> dict:
    execution = AgentExecution(
        agent_id=1,
        application_id=application.id,
        input_ref=f"application:{application.id}",
        output_ref="stub-output",
        status="SUCCESS",
        duration_ms=0,
        started_at=datetime.now(timezone.utc),
    )
    db.add(execution)
    return {"stub": True, "agent": agent_name}


def cv_processing_agent(db: Session, application: Application) -> dict:
    """Runs when an application LEAVES CV_PROCESSING — parses the resume into a CandidateProfile."""
    resume = (
        db.query(Resume)
        .filter(Resume.candidate_id == application.candidate_id)
        .order_by(Resume.uploaded_at.desc())
        .first()
    )
    if not resume:
        raise ValueError(f"No resume found for candidate {application.candidate_id}")

    started = datetime.now(timezone.utc)
    try:
        raw_text = extract_text_from_file(resume.file_url)
        structured = parse_cv(raw_text)
        status_result = "SUCCESS"
    except ValueError as e:
        # Fail safely (NFR: never silently drop) — log it, let HUMAN_REVIEW surface the error
        structured = None
        status_result = f"FAILED: {e}"

    execution = AgentExecution(
        agent_id=1,
        application_id=application.id,
        input_ref=f"resume:{resume.id}",
        output_ref=f"candidate_profile:{application.candidate_id}" if structured else None,
        status=status_result,
        duration_ms=int((datetime.now(timezone.utc) - started).total_seconds() * 1000),
        started_at=started,
    )
    db.add(execution)

    if structured is None:
        raise RuntimeError(status_result)  # bubble up so advance_application halts the transition

    profile = (
        db.query(CandidateProfile)
        .filter(CandidateProfile.candidate_id == application.candidate_id)
        .first()
    )
    if not profile:
        profile = CandidateProfile(candidate_id=application.candidate_id)
        db.add(profile)

    for field in ["education", "experience", "skills", "projects", "certifications", "languages", "links", "low_confidence_fields"]:
        setattr(profile, field, structured[field])
    profile.parsed_at = datetime.now(timezone.utc)

    resume.parsed_at = datetime.now(timezone.utc)

    return {"profile_id": profile.id}


def ats_screening_agent(db: Session, application: Application) -> dict:
    """
    Runs when an application LEAVES ATS_SCREENING (FR-6, FR-7).
    Scores the candidate profile against the job's requirements, stores the
    evidence-bearing ATSEvaluation, and recomputes the job's ranking so the
    Human Review gate (FR-8) has something to show the recruiter.
    """
    job = db.get(Job, application.job_id)
    profile = (
        db.query(CandidateProfile)
        .filter(CandidateProfile.candidate_id == application.candidate_id)
        .first()
    )
    if not profile:
        raise ValueError(f"No parsed profile found for candidate {application.candidate_id}")

    started = datetime.now(timezone.utc)
    profile_dict = {
        field: getattr(profile, field)
        for field in ["education", "experience", "skills", "projects", "certifications", "languages", "links"]
    }
    result = score_candidate(job.requirements_json or {}, profile_dict)

    execution = AgentExecution(
        agent_id=1,
        application_id=application.id,
        input_ref=f"candidate_profile:{profile.id}",
        output_ref=f"ats_evaluation:pending",
        status="SUCCESS",
        duration_ms=int((datetime.now(timezone.utc) - started).total_seconds() * 1000),
        started_at=started,
    )
    db.add(execution)

    evaluation = (
        db.query(ATSEvaluation)
        .filter(ATSEvaluation.application_id == application.id)
        .first()
    )
    if not evaluation:
        evaluation = ATSEvaluation(application_id=application.id)
        db.add(evaluation)

    evaluation.overall_score = result["overall_score"]
    evaluation.dimension_scores_json = result["dimension_scores"]
    evaluation.strengths = result["strengths"]
    evaluation.gaps = result["gaps"]
    evaluation.computed_at = datetime.now(timezone.utc)
    db.flush()

    execution.output_ref = f"ats_evaluation:{evaluation.id}"

    recompute_rankings(db, application.job_id)

    return {"evaluation_id": evaluation.id, "overall_score": evaluation.overall_score}


# Stage-specific agents run when LEAVING that status. Falls back to the generic stub.
STAGE_AGENTS = {
    ApplicationStatus.CV_PROCESSING: cv_processing_agent,
    ApplicationStatus.ATS_SCREENING: ats_screening_agent,
}


def advance_application(db: Session, application: Application) -> Application:
    next_status = TRANSITIONS.get(application.status)
    if next_status is None:
        return application

    old_status = application.status
    agent_fn = STAGE_AGENTS.get(old_status)

    if agent_fn:
        try:
            agent_fn(db, application)
        except (ValueError, RuntimeError) as e:
            # Fail safely: park it in HUMAN_REVIEW with a visible error, never drop it (NFR: Reliability)
            application.status = ApplicationStatus.HUMAN_REVIEW
            db.add(AuditLog(
                actor_type="agent",
                actor_id=1,
                action=f"failed:{old_status.value} error={e}",
                entity="application",
                entity_id=application.id,
            ))
            db.commit()
            db.refresh(application)
            return application
    else:
        run_stub_agent(db, application, agent_name=f"{old_status.value}_agent")

    application.status = next_status
    db.add(AuditLog(
        actor_type="agent",
        actor_id=1,
        action=f"transition:{old_status.value}->{next_status.value}",
        entity="application",
        entity_id=application.id,
    ))

    db.commit()
    db.refresh(application)
    return application