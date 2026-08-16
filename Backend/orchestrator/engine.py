from datetime import datetime, timezone

from sqlalchemy.orm import Session

from app.models.agent import AgentExecution
from app.models.application import Application, ApplicationStatus
from app.models.audit_log import AuditLog

# Defines which status follows which — the spine of the FSM.
TRANSITIONS = {
    ApplicationStatus.APPLIED: ApplicationStatus.CV_PROCESSING,
    ApplicationStatus.CV_PROCESSING: ApplicationStatus.ATS_SCREENING,
    ApplicationStatus.ATS_SCREENING: ApplicationStatus.HUMAN_REVIEW,
    # HUMAN_REVIEW, AI_INTERVIEW, HR_SCHEDULING etc. require an explicit human/agent action,
    # not an automatic transition, so they're not listed here.
}


def run_stub_agent(db: Session, application: Application, agent_name: str) -> dict:
    """Placeholder for a real agent call — just proves the pipeline shape."""
    execution = AgentExecution(
        agent_id=1,  # replace once Agent rows are seeded
        application_id=application.id,
        input_ref=f"application:{application.id}",
        output_ref="stub-output",
        status="SUCCESS",
        duration_ms=0,
        started_at=datetime.now(timezone.utc),
    )
    db.add(execution)
    return {"stub": True, "agent": agent_name}


def advance_application(db: Session, application: Application) -> Application:
    next_status = TRANSITIONS.get(application.status)
    if next_status is None:
        return application  # no automatic transition from here — needs a human/agent action

    run_stub_agent(db, application, agent_name=f"{application.status.value}_agent")

    old_status = application.status
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