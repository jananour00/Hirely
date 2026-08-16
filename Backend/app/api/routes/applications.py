from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.models.application import Application
from app.orchestrator.engine import advance_application

router = APIRouter(prefix="/applications", tags=["applications"])


@router.post("/{application_id}/advance")
def advance(application_id: int, db: Session = Depends(get_db)):
    application = db.get(Application, application_id)
    if not application:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Application not found")
    application = advance_application(db, application)
    return {"id": application.id, "status": application.status}