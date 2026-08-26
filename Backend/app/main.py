from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.routes.auth import router as auth_router
from app.api.routes.users import router as users_router
from app.api.routes.applications import router as applications_router
from app.api.routes.jobs import router as jobs_router
from app.api.routes.applications_public import router as apply_router
from app.api.routes.candidates import router as candidates_router
from app.core.config import settings

app = FastAPI(
    title="Hirely API",
    description="Agentic AI Recruitment System",
    version="0.1.0",
)

# Frontend (Next.js dev server / deployed origin) needs to call this API from a
# different origin — added alongside the frontend integration.
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.frontend_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router)
app.include_router(users_router)
app.include_router(applications_router)
app.include_router(jobs_router)
app.include_router(apply_router)
app.include_router(candidates_router)


@app.get("/")
def root():
    return {
        "name": "Hirely",
        "status": "running",
        "version": "0.1.0",
    }


@app.get("/health")
def health():
    return {
        "status": "healthy"
    }