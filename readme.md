# Hirly

Agentic AI recruitment operating system. See `Hirly_Project_Description_and_SRS.md`
for the full product spec, data model, and phased delivery plan. This repo
contains a FastAPI **Backend** and a Next.js **Frontend** (recruiter console +
public careers site) — see "What's not built yet" below for what's still
missing on both sides.

## Status

This is an early-stage build. It runs end-to-end for the V1 candidate
pipeline shape (`APPLIED → CV_PROCESSING → ATS_SCREENING → HUMAN_REVIEW →
AI_INTERVIEW → INTERVIEW_EVALUATION → HR_SCHEDULING → HR_INTERVIEW → OFFER →
HIRED`, with a `REJECTED` branch off `HUMAN_REVIEW`). `requirement_extraction.py`,
`cv_parser.py`, `ats_matcher.py`, and `jd_generator.py` all make real LLM
calls now (via `app/core/agent_llm_client.py`, Groq by default). Everything
past `HUMAN_REVIEW` (AI interview, scheduling, email) is still the generic
stub transition — see "What's not built yet" below.

## Setup — Docker (recommended)

The whole stack (Postgres, Redis, API) runs via Compose:

1. Copy `.env.example` to `.env` at the project root and fill in real values
   — **do not commit this file**:
   - `JWT_SECRET` — any long random string for local dev
   - `GROQ_API_KEY` and/or `OPENROUTER_API_KEY` — required, since every
     agent in `app/agents/` calls out via `app/core/agent_llm_client.py`
     (`LLM_PROVIDER` picks the backend: `groq` | `openrouter`)
   - `ANTHROPIC_API_KEY` — only needed if you switch `app/core/llm_client.py`
     callers to Anthropic directly; unused by the agents today
   - `DATABASE_URL` / `REDIS_URL` in `.env` are for host-based dev (below);
     Compose overrides them to the in-network `db`/`redis` hostnames itself,
     so you don't need to edit those two for Docker.
   - `FRONTEND_ORIGINS_RAW` — comma-separated origins allowed to call the API
     (CORS). Defaults to `http://localhost:3000`, which matches the frontend
     dev server below; add your deployed frontend URL here too once you have one.

   Any key that has ever been pasted into a chat, screenshot, or committed
   file should be treated as burned — revoke and regenerate it with the
   provider before relying on it.

2. Build and start everything:
   ```bash
   docker compose up --build
   ```
   This starts Postgres (`pgvector/pgvector:pg16`) and Redis with health
   checks, then builds the API image and runs `alembic upgrade head`
   automatically before starting `uvicorn` (see `Backend/Dockerfile`).

3. Docs at `http://localhost:8000/docs`. The `backend` service mounts
   `./Backend` as a volume, so code edits reload without a rebuild
   (`uvicorn` isn't started with `--reload` in the container — restart the
   `backend` service after edits, or add `--reload` locally if you want it).

## Setup — running the API on the host instead

If you'd rather not containerize the API itself:

```bash
cd Backend
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
```

1. In `.env`, point `DATABASE_URL`/`REDIS_URL` at `localhost` instead of
   `db`/`redis` (Compose's service hostnames only resolve inside the
   Docker network).
2. Start just the datastores:
   ```bash
   docker compose up -d db redis
   ```
3. Create the schema:
   ```bash
   alembic upgrade head
   ```
4. Run the API:
   ```bash
   uvicorn app.main:app --reload
   ```
   Docs at `http://localhost:8000/docs`.

## Setup — Frontend

The `Frontend/` app is Next.js 14 (App Router, TypeScript, Tailwind). It talks
to the Backend over plain HTTP — start the Backend first (either setup above),
then:

```bash
cd Frontend
npm install
cp .env.example .env.local   # NEXT_PUBLIC_API_URL, defaults to http://localhost:8000
npm run dev
```

Runs at `http://localhost:3000`. Two entry points:

- **`/`, `/login`, `/register`, `/dashboard/**`** — the recruiter console.
  Register creates a new org (you become its `admin`); sign in to draft
  requisitions, publish job descriptions, and work the human-review gate.
- **`/careers`, `/careers/[jobId]`, `/apply/status`** — the public candidate
  side. No auth. Lists jobs with `status = open`, lets a candidate apply with
  a resume upload, and gives them an application number to check status with
  later (there's no status-change email yet — see below).

For a production build: `npm run build && npm start`.

## Frontend ↔ Backend integration notes

The frontend is a plain consumer of the API in `Backend/app/api/routes/` —
same auth model (JWT bearer token from `/auth/login` or `/auth/register`,
stored client-side and attached to authenticated requests), same pipeline
shape. A few endpoints didn't exist yet and were added specifically to make
the frontend functional rather than cosmetic:

- `GET /jobs/public` and `GET /jobs/{id}/public` — unauthenticated, `status =
  open` only. The careers site had no way to list or read a job otherwise.
- `GET /jobs/{id}` and `GET /jobs/{id}/applications` — recruiter-only. The
  dashboard's job detail page and applicant queue read from these.
- `ApplicationReviewOut` (`GET /applications/{id}/review`) now also returns
  `candidate_id`, so the review page can fetch the parsed candidate profile
  alongside the ATS evidence.
- CORS middleware in `app/main.py`, controlled by `FRONTEND_ORIGINS_RAW`
  (see above) — the API previously assumed same-origin callers only.

Everything else — `/auth/*`, `/jobs/` (create/approve), `/apply/*`,
`/applications/{id}/advance`, `/applications/{id}/review` (POST),
`/candidates/{id}/profile` — is unchanged; the frontend just calls it.

## Database migrations

Schema changes go through Alembic, not `Base.metadata.create_all()`:
```bash
alembic revision --autogenerate -m "describe the change"
alembic upgrade head
```

## Smoke tests

Each agent has a standalone script that calls it directly (no DB, no
server) — useful for checking your LLM provider key is wired up correctly:
```bash
python test_requirement_extraction.py
python test_cv_parser.py
python test_ats_matcher.py
python test_jd_generator.py
```

## Verified working end-to-end

The full candidate lifecycle has been run manually against a live server:
register org/user → create job → publish → candidate applies with a resume
→ `/advance` through CV parsing and ATS screening → `HUMAN_REVIEW` (confirmed
`/advance` cannot skip this gate) → recruiter approves via
`POST /applications/{id}/review` → `/advance` continues through interview,
scheduling, offer, to `HIRED`. A separate run confirmed the `REJECTED`
branch off `HUMAN_REVIEW` halts further advancement. The audit log
reconstructs the full timeline for either path. This was the Backend
verification, ahead of the Frontend existing.

The Frontend (`npm run build`) compiles cleanly under strict TypeScript
against the API contracts above, but hasn't yet been click-tested against a
running Backend — do that before treating either side as done.

## What's not built yet

- **AI interview system** (FR-9/10/11) — no models, routes, or agents; the
  `AI_INTERVIEW → INTERVIEW_EVALUATION` transition still runs the generic
  stub agent in `orchestrator/engine.py`. The frontend's application review
  page surfaces this as a manual "Advance pipeline" button past the human
  review gate, since there's nothing else to show yet.
- **Real scheduling & email/notifications** (FR-12/13) — no email provider
  wired up, no notification templates; `HR_SCHEDULING`/`HR_INTERVIEW`/`OFFER`
  are still stub transitions too. The frontend never emails candidates —
  status is pull-only via `/apply/status`.
- **Background workers / queue** — Redis is provisioned but nothing
  consumes it yet; `/applications/{id}/advance` is called synchronously
  (including from the frontend's "Advance pipeline" button).
- **Frontend auth persistence** — the JWT lives in `localStorage`; there's no
  refresh flow, so a token just expires (`ACCESS_TOKEN_EXPIRE_MINUTES`) and
  the user is bounced back to `/login` on the next call.
- **Company dashboard depth** — the SRS's fuller Company dashboard (org
  member management, analytics) isn't built; the frontend currently covers
  job creation/publishing and the human-review queue only, matching what the
  V1 backend actually supports.
- **Automated integration tests** — the four smoke-test scripts above call
  agents directly; there's no pytest suite hitting the API/DB yet
  (`pytest`/`httpx` are already in `requirements.txt` for this). The frontend
  has no test suite either.
- **`--reload` inside Docker** — the container runs a plain `uvicorn`
  process; restart the `backend` service to pick up code changes, or run on
  the host (see above) if you want autoreload.
