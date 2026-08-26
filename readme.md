# Hirely
<p align="center">
<img width="250" alt="ChatGPT Image Aug 26, 2026, 10_23_56 PM" src="https://github.com/user-attachments/assets/d86cd80d-794f-4528-ba75-dcf4de0894bd" />


**Agentic AI recruitment operating system** — a full-stack platform that takes a
job requisition from draft to hire, powered by a multi-agent LLM pipeline for
CV parsing, ATS-style candidate matching, and job description generation.

Built with a **FastAPI** backend and a **Next.js 14** (App Router, TypeScript,
Tailwind) frontend, covering both the recruiter console and a public careers
site. See `Hirly_Project_Description_and_SRS.md` for the full product spec
and data model.

## Screenshots

<img width="1903" height="851" alt="image" src="https://github.com/user-attachments/assets/71a05cf1-ccd2-4467-9933-08082733db95" />

## Features

- **Recruiter console** — register an org, draft and publish job
  requisitions, and work an application queue through a human-review gate.
- **Public careers site** — no-auth job listing and detail pages, resume
  upload application flow, and application-status lookup by reference number.
- **Multi-agent LLM pipeline** — requirement extraction, CV parsing, ATS
  matching, and job description generation, each backed by real LLM calls
  (Groq by default, OpenRouter supported) via a shared agent client.
- **Full candidate pipeline** — `APPLIED → CV_PROCESSING → ATS_SCREENING →
  HUMAN_REVIEW → AI_INTERVIEW → INTERVIEW_EVALUATION → HR_SCHEDULING →
  HR_INTERVIEW → OFFER → HIRED`, with a `REJECTED` branch off human review
  and a full audit-log timeline for either path.
- **JWT auth**, org-scoped access, and CORS-configured API for the frontend.

## Tech Stack

**Backend:** FastAPI, PostgreSQL (`pgvector`), Redis, SQLAlchemy + Alembic,
Docker Compose
**Frontend:** Next.js 14 (App Router), TypeScript, Tailwind CSS
**AI/Agents:** Groq / OpenRouter LLM providers via a shared agent client

## Setup — Docker (recommended)

The whole stack (Postgres, Redis, API) runs via Compose:

1. Copy `.env.example` to `.env` at the project root and fill in real values:
   - `JWT_SECRET` — any long random string for local dev
   - `GROQ_API_KEY` and/or `OPENROUTER_API_KEY` — required; every agent in
     `app/agents/` calls out via `app/core/agent_llm_client.py`
     (`LLM_PROVIDER` picks the backend: `groq` | `openrouter`)
   - `FRONTEND_ORIGINS_RAW` — comma-separated origins allowed to call the API
     (CORS). Defaults to `http://localhost:3000`.

2. Build and start everything:
   ```bash
   docker compose up --build
   ```
   This starts Postgres (`pgvector/pgvector:pg16`) and Redis with health
   checks, then builds the API image and runs `alembic upgrade head`
   automatically before starting `uvicorn`.

3. Docs at `http://localhost:8000/docs`.

## Setup — running the API on the host instead

```bash
cd Backend
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
docker compose up -d db redis
alembic upgrade head
uvicorn app.main:app --reload
```
Docs at `http://localhost:8000/docs`.

## Setup — Frontend

```bash
cd Frontend
npm install
cp .env.example .env.local   # NEXT_PUBLIC_API_URL, defaults to http://localhost:8000
npm run dev
```

Runs at `http://localhost:3000`:

- **`/`, `/login`, `/register`, `/dashboard/**`** — recruiter console.
  Register creates a new org (you become its `admin`); sign in to draft
  requisitions, publish job descriptions, and work the human-review gate.
- **`/careers`, `/careers/[jobId]`, `/apply/status`** — public candidate
  side. Lists open jobs, lets a candidate apply with a resume upload, and
  gives them an application number to check status with.

For a production build: `npm run build && npm start`.

## API Overview

The frontend consumes the API in `Backend/app/api/routes/` using JWT bearer
auth (from `/auth/login` or `/auth/register`). Key endpoints:

- `GET /jobs/public`, `GET /jobs/{id}/public` — unauthenticated job listing
  for the careers site.
- `GET /jobs/{id}`, `GET /jobs/{id}/applications` — recruiter dashboard job
  detail and applicant queue.
- `GET /applications/{id}/review`, `POST /applications/{id}/review` —
  human-review gate, including parsed candidate profile and ATS evidence.
- `POST /applications/{id}/advance` — moves an application through the
  pipeline.
- `/auth/*`, `/jobs/` (create/approve), `/apply/*`, `/candidates/{id}/profile`.

## Database Migrations

```bash
alembic revision --autogenerate -m "describe the change"
alembic upgrade head
```

## Testing

Each agent has a standalone smoke-test script that calls it directly (no DB,
no server) — useful for checking your LLM provider key is wired up:
```bash
python test_requirement_extraction.py
python test_cv_parser.py
python test_ats_matcher.py
python test_jd_generator.py
```

The full candidate lifecycle has been verified end-to-end against a live
server: register org/user → create job → publish → candidate applies →
CV parsing → ATS screening → human review (approve or reject) → interview →
scheduling → offer → hired, with the audit log reconstructing the full
timeline.
