from datetime import datetime, timezone

from sqlalchemy.orm import Session

from app.agents.cv_parser import parse_cv
from app.core.text_extraction import extract_text_from_file
from app.models.agent import AgentExecution
from app.models.application import Application, ApplicationStatus
from app.models.audit_log import AuditLog
from app.models.candidate_profile import CandidateProfile
from app.models.resume import Resume

TRANSITIONS = {
    ApplicationStatus.APPLIED: ApplicationStatus.CV_PROCESSING,
    ApplicationStatus.CV_PROCESSING: ApplicationStatus.ATS_SCREENING,
    ApplicationStatus.ATS_SCREENING: ApplicationStatus.HUMAN_REVIEW,
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


# Stage-specific agents run when LEAVING that status. Falls back to the generic stub.
STAGE_AGENTS = {
    ApplicationStatus.CV_PROCESSING: cv_processing_agent,
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