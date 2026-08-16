# Hirly — Agentic AI Recruitment Operating System
### Full Project Description, Software Requirements Specification (SRS), and Phased Delivery Plan

**Document version:** 1.0
**Prepared for:** Capstone / Portfolio Project — Agentic AI Track
**Author:** Jana Nour

---

## Table of Contents

1. Project Description
2. Software Requirements Specification (SRS)
   - 2.1 Introduction
   - 2.2 Overall Description
   - 2.3 System Features (Functional Requirements)
   - 2.4 External Interface Requirements
   - 2.5 Non-Functional Requirements
   - 2.6 Data Model
   - 2.7 System Architecture
   - 2.8 Constraints & Assumptions
3. Modules & Phased Delivery Plan (V1 → V3)
4. Risk Register
5. Success Metrics

---

# 1. Project Description

## 1.1 Vision

**Hirly** is an AI-native recruitment operating system that orchestrates the full hiring lifecycle — from job creation to hire — through a set of coordinated, specialized AI agents working under human supervision. Rather than automating one step of recruitment (parsing, or scoring, or scheduling), Hirly chains these steps into a single agentic workflow with **Human-in-the-Loop (HITL)** checkpoints at every consequential decision.

## 1.2 Problem Statement

Recruitment teams manage a fragmented, manual pipeline: job descriptions are hand-written, CVs are screened by eye or by primitive keyword filters, interview scheduling is done by email back-and-forth, and candidate communication is inconsistent. This is slow, inconsistent, and doesn't scale. Existing "AI ATS" tools typically automate a single stage (parsing or scoring) but leave the rest of the pipeline manual and disconnected.

## 1.3 Product Positioning

> Hirly is an AI-native recruitment operating system that lets companies manage the full hiring lifecycle through coordinated AI agents: natural-language job creation, explainable ATS matching and ranking, adaptive AI interviews, human review gates, automated scheduling and communication — all with recruiter oversight and full auditability.

Hirly is explicitly **not** marketed as "AI decides who gets hired." The AI recommends; a human approves every consequential step (rejection, advancement, offer).

## 1.4 Primary Users

| User | Goals |
|---|---|
| **Recruiter / Company Admin** | Create jobs fast, screen high volumes of candidates reliably, reduce time-to-hire, retain final decision authority |
| **Candidate** | Apply easily, understand where they stand, get timely, clear communication |

## 1.5 Why This Project Is a Strong Capstone / Portfolio Piece

- Combines **Generative AI** (job description generation, adaptive interviewing), **RAG** (company knowledge base), and **Agentic AI** (multi-agent orchestration, tool calling, state machines).
- Full-stack: frontend, backend, database, background workers, cloud infra, auth/RBAC.
- Demonstrates system design maturity: state machines, audit trails, agent observability — not just "call an LLM and show the output."
- Has a natural narrative arc for interviews and demos: MVP → agentic depth → intelligence layer.

## 1.6 Recommended Scope Discipline

This is a large concept. The rest of this document defines a **realistic, phased scope** (Section 3) so the build stays achievable while preserving the ambitious end-state vision.

---

# 2. Software Requirements Specification (SRS)

## 2.1 Introduction

### 2.1.1 Purpose
This SRS defines the functional and non-functional requirements for Hirly V1 (MVP), with forward references to V2/V3 capabilities so the architecture is not painted into a corner.

### 2.1.2 Scope
Hirly V1 covers: natural-language job creation, AI job description generation with human approval, single-channel job publishing (internal candidate portal), candidate application and CV upload, AI CV parsing, ATS semantic matching and ranking, human review gate, AI technical + behavioral interview (text-based, adaptive), interview evaluation report, HR interview scheduling, and email/notification communication.

Out of scope for V1: multi-channel external job board publishing, voice interviews, talent pool re-matching, company RAG knowledge base, advanced predictive analytics, payroll/onboarding.

### 2.1.3 Definitions
- **ATS** — Applicant Tracking System / matching engine
- **HITL** — Human-in-the-Loop
- **Agent** — A bounded, tool-using LLM-driven process responsible for one pipeline stage
- **Orchestrator** — The component that sequences agents according to the hiring state machine
- **RBAC** — Role-Based Access Control

### 2.1.4 Intended Audience
Developer(s) building the system (solo or small team), technical reviewers/mentors, and future contributors.

## 2.2 Overall Description

### 2.2.1 Product Perspective
Hirly is a new, standalone web application (not an extension of an existing ATS). It exposes two web experiences (Company dashboard, Candidate portal) backed by a shared API and an agent orchestration layer.

### 2.2.2 Product Functions (Summary)
1. Natural-language job creation → structured job + AI-generated JD → human approval → publish
2. Candidate application with CV upload
3. CV parsing → structured candidate profile
4. Semantic ATS matching → explainable score + ranking
5. Human review gate (approve / reject / request info / advance)
6. AI adaptive technical interview (text-based chat)
7. AI behavioral interview (text-based chat, rubric-scored)
8. Interview evaluation report generation
9. HR interview scheduling (calendar slot negotiation)
10. Automated candidate communication (email + in-app notifications)
11. Candidate timeline / status tracking
12. Agent execution trace / observability log
13. Basic hiring funnel analytics

### 2.2.3 User Classes and Characteristics
| Role | Description | Permissions |
|---|---|---|
| **Company Admin** | Owns the org account | Full access: users, jobs, billing/settings |
| **Recruiter** | Runs day-to-day hiring | Create/manage jobs, review candidates, approve/reject, schedule |
| **Candidate** | Job seeker | Apply, view own application status, complete interviews |
| **(System) Agent** | Non-human actor | Executes bounded tool calls within permission scope; cannot make final hire/reject decisions autonomously |

### 2.2.4 Operating Environment
Web application (desktop + mobile-responsive browser). Cloud-hosted backend. No native mobile app in V1.

### 2.2.5 Design & Implementation Constraints
- LLM calls must be logged with inputs/outputs for auditability.
- No agent may transition a candidate to `REJECTED` or `HIRED` without a corresponding human-review record.
- All PII (CVs, personal data) encrypted at rest; tenant-isolated storage.

### 2.2.6 Assumptions and Dependencies
- Access to an LLM API (e.g., Anthropic API) with tool-calling / structured output support.
- Candidates and recruiters interact only through Hirly (no external ATS import in V1).
- Single-tenant-per-organization data model (multi-tenant DB, not multi-tenant infra) is sufficient for V1.

## 2.3 System Features (Functional Requirements)

Each feature includes: description, inputs, processing, outputs, and priority (Must/Should/Could — MoSCoW).

### FR-1: Natural-Language Job Creation — **Must**
- **Input:** Free-text HR description of the role.
- **Processing:** Requirement Extraction Agent parses the text into structured fields (title, experience, required skills, preferred skills, responsibilities, soft skills).
- **Output:** Structured job draft object.
- **Acceptance criteria:** Given a 2–4 sentence role description, the system extracts at minimum: title, experience range, ≥3 required skills, ≥2 responsibilities, with each field traceable to source text (for review).

### FR-2: AI Job Description Generation — **Must**
- **Input:** Structured job draft from FR-1.
- **Processing:** JD Generator Agent produces a full job posting (About, Responsibilities, Required/Preferred Qualifications, Benefits placeholder, Location).
- **Output:** Editable JD document.
- **Acceptance criteria:** Recruiter can edit any section before publishing; nothing is published without explicit "Approve" action.

### FR-3: Job Publishing — **Must (internal portal only in V1)**
- Publish approved job to the Hirly candidate portal with status `OPEN`.
- **Should (V2):** Multi-channel push to external job boards via API integrations.

### FR-4: Candidate Application — **Must**
- Multi-step form: personal info → CV upload → additional info → consent/AI transparency notice → submit.
- **Acceptance criteria:** Candidate cannot submit without explicit consent checkbox acknowledging AI-assisted screening.

### FR-5: CV Intelligence (Parsing) — **Must**
- **Input:** PDF/DOCX CV file.
- **Processing:** File validation → text extraction (OCR fallback for scanned PDFs) → resume parser → entity extraction.
- **Output:** Structured `CandidateProfile` (Personal, Education, Experience, Skills, Projects, Certifications, Languages, Links).
- **Acceptance criteria:** ≥90% field-extraction success rate on a test set of 30 varied CV formats; low-confidence fields are flagged, not silently dropped.

### FR-6: Semantic ATS Matching & Scoring — **Must**
- **Input:** Job requirements + candidate profile.
- **Processing:** ATS Agent computes a multi-dimension score (Required Skills, Experience, Technical Evidence, Responsibilities Fit, Education, Soft Skills) using embedding-based semantic matching, not raw keyword matching.
- **Output:** Overall match %, per-dimension scores, explicit **Strengths** list and **Gaps** list.
- **Acceptance criteria:** Every score is accompanied by at least one human-readable evidence sentence per dimension.

### FR-7: Candidate Ranking — **Must**
- Rank candidates per job by overall score, re-computed whenever a new application arrives.
- Ranking criteria weights are configurable per job family (e.g., technical roles weight Technical Evidence higher than a UX role would).

### FR-8: Human Review Gate — **Must**
- Recruiter sees AI recommendation, match score, evidence, and confidence level.
- Actions: `Approve`, `Reject`, `Request More Information`, `Move to Interview`.
- **Acceptance criteria:** No candidate advances past this gate without a logged human action tied to a specific recruiter user ID and timestamp.

### FR-9: AI Technical Interview (Adaptive) — **Must**
- Text-based chat interview driven by an Interview Agent.
- Adapts follow-up question difficulty based on answer quality (strong answer → harder question; weak answer → clarification).
- **Acceptance criteria:** Given a job with defined must-have skills, the agent asks at least one question per must-have skill area, plus at least one adaptive follow-up triggered by an actual candidate answer (not pre-scripted).

### FR-10: AI Behavioral Interview — **Must**
- Chat interview covering a configurable competency rubric (Leadership, Communication, Teamwork, Conflict Resolution, Ownership, Adaptability).
- Each answer scored against the rubric with justification.

### FR-11: Interview Evaluation Report — **Must**
- Aggregates technical + behavioral scores into a single report: per-dimension bar scores, Strengths, Areas to Explore, and a recommendation (`Proceed to HR Interview` / `Do Not Proceed` — presented as decision support, editable by recruiter).

### FR-12: HR Interview Scheduling — **Should**
- Scheduling Agent proposes slots based on recruiter availability (manual calendar entry in V1; calendar API integration in V2).
- Candidate selects a slot; system creates the interview record and sends confirmations.

### FR-13: Candidate Communication — **Must**
- Automated email + in-app notifications for: application received, AI screening result (if configured to notify), interview invitation, interview reminder, scheduling confirmation, status updates.
- **Acceptance criteria:** Every state transition in the candidate state machine (2.6) has a corresponding notification template.

### FR-14: Candidate Timeline — **Must**
- Chronological view of every state transition for a candidate, visible to both recruiter and candidate (candidate sees a simplified version).

### FR-15: Agent Execution Trace / Observability — **Should**
- Every agent action logged with: timestamp, agent name, input reference, output reference, duration, and linked candidate/job ID.
- Powers an "Agent Operations Center" view showing active agents and recent task outcomes.

### FR-16: Hiring Funnel Analytics — **Should**
- Dashboard metrics: Open Jobs, Total Applications, AI Screened, Human Review pending, Interviews (AI/HR), Offers, Hired.
- Funnel visualization: Applications → ATS Screening → Human Review → AI Interview → HR Interview → Offer → Hired.

### FR-17: Talent Pool — **Could (V2)**
- Retain non-hired but strong candidates; re-match them automatically against new job postings.

### FR-18: Company Knowledge Base (RAG) — **Could (V2)**
- Company uploads handbook/guidelines; agents use RAG to ground JD generation and interview questions in company-specific context.

### FR-19: Recruitment Intelligence Copilot — **Could (V3)**
- Natural-language Q&A over aggregated hiring data (e.g., "Why are we struggling to hire Senior Backend Engineers?").

## 2.4 External Interface Requirements

### 2.4.1 User Interfaces
- **Company Web App:** Dashboard, Jobs, Candidates, Interviews, Talent Pool (V2+), AI Agents (observability), Analytics, Settings.
- **Candidate Web Portal:** Job search, application flow, application tracker, interview chat interface, notifications.

### 2.4.2 API Interfaces
- REST API (FastAPI) consumed by both frontends.
- LLM Provider API (Anthropic API) for generation, extraction, and evaluation tasks — via tool calling / structured JSON outputs.
- Email provider API (e.g., SMTP/transactional email service) for FR-13.
- (V2) Calendar API (Google Calendar / Outlook) for FR-12.
- (V2) Job board APIs for FR-3 multi-channel publishing.

### 2.4.3 Hardware Interfaces
None beyond standard client devices with a modern browser.

## 2.5 Non-Functional Requirements

| Category | Requirement |
|---|---|
| **Performance** | ATS scoring for a single candidate completes in <10s (excluding queueing); CV parsing completes in <15s per document. |
| **Scalability** | Architecture supports background job processing (queue + workers) so a burst of 500 applications does not block the API. |
| **Security** | All PII encrypted at rest and in transit; tenant data isolation at the query layer; role-based access control enforced server-side, not just in UI. |
| **Auditability** | Every AI recommendation that could affect a hiring outcome is logged with the model output, timestamp, and any human override. |
| **Reliability** | Agent failures fail *safely* — a failed ATS scoring job leaves a candidate in `HUMAN_REVIEW` with a visible error, never silently drops them. |
| **Explainability** | Every AI score must ship with human-readable evidence; no bare percentage without justification. |
| **Usability** | Recruiter can go from "job idea in plain English" to "published job" in under 5 minutes of interaction. |
| **Maintainability** | Agents are modular — each agent has a single responsibility and a defined input/output schema, so agents can be modified independently. |
| **Compliance** | Candidate consent captured before any AI-assisted screening (FR-4); data retention policy configurable per org. |

## 2.6 Data Model (Core Entities)

```
User (id, org_id, role, email, name)
Organization (id, name, settings)

Job (id, org_id, title, status, requirements_json, jd_text, created_by)
JobRequirement (id, job_id, field, value, source_span)
JobPublication (id, job_id, channel, published_at)

Candidate (id, email, name)
CandidateProfile (id, candidate_id, education, experience, skills, projects, certifications, languages, links)
Resume (id, candidate_id, file_url, parsed_at)

Application (id, job_id, candidate_id, status, submitted_at)
ATSEvaluation (id, application_id, overall_score, dimension_scores_json, strengths, gaps)
CandidateRanking (id, job_id, application_id, rank, computed_at)
HumanReview (id, application_id, reviewer_id, decision, notes, decided_at)

Interview (id, application_id, type[technical|behavioral], status)
InterviewSession (id, interview_id, started_at, ended_at)
InterviewQuestion (id, session_id, text, order, difficulty)
InterviewAnswer (id, question_id, text, submitted_at)
InterviewEvaluation (id, session_id, dimension_scores_json, strengths, concerns, recommendation)

CalendarEvent (id, application_id, start_time, end_time, status)
Notification (id, recipient_id, type, channel, sent_at, status)

Agent (id, name, type)
AgentExecution (id, agent_id, application_id, input_ref, output_ref, started_at, duration_ms, status)

AuditLog (id, actor_type[human|agent], actor_id, action, entity, entity_id, timestamp)
```

*(V2+ adds: CompanyKnowledge, Document, Embedding, Offer, HiringDecision.)*

## 2.7 System Architecture

### 2.7.1 High-Level Components
```
Candidate Portal (Next.js) ─┐
                             ├─► API Gateway (FastAPI) ─► Orchestrator ─► Agents ─► LLM API
Company Dashboard (Next.js) ─┘                │                              │
                                               ▼                              ▼
                                        PostgreSQL + pgvector          Object Storage (CVs)
                                               │
                                        Background Workers (queue: Redis)
```

### 2.7.2 Orchestration Model
The Orchestrator drives every application through a **finite state machine** (below), invoking the relevant agent at each transition and pausing at Human Review / HR Scheduling gates for manual input.

### 2.7.3 Candidate State Machine
```
APPLIED
   → CV_PROCESSING
      → ATS_SCREENING
         → HUMAN_REVIEW ──(reject)──► REJECTED
            → AI_INTERVIEW ──(reject)──► REJECTED
               → INTERVIEW_EVALUATION
                  → HR_SCHEDULING
                     → HR_INTERVIEW ──(reject)──► REJECTED
                        → OFFER
                           → HIRED
```

### 2.7.4 Recommended Tech Stack

| Layer | Choice |
|---|---|
| Frontend | Next.js, React, TypeScript, Tailwind, shadcn/ui |
| Backend | Python, FastAPI, Pydantic, SQLAlchemy |
| AI | Anthropic API (tool calling, structured outputs), LangGraph or a lightweight custom orchestrator, RAG (V2), embeddings |
| Database | PostgreSQL + pgvector |
| Infra | Docker, Redis (queue), background workers, object storage (S3-compatible), AWS |
| Auth | OAuth + JWT, RBAC middleware |

## 2.8 Constraints & Assumptions

- Solo/small-team build → V1 must be achievable in a bounded timeframe (see Section 3).
- No autonomous rejection/hiring by AI — hard constraint, not a nice-to-have.
- LLM cost/latency must be considered — batch or async where evaluation isn't time-critical (e.g., ranking recompute).

---

# 3. Modules & Phased Delivery Plan

## Phase 1 — V1 / MVP (core, demoable, portfolio-ready)

**Goal:** A working end-to-end pipeline for one job, one company, a handful of candidates — proving the full agentic loop.

| Module | Contents | Maps to |
|---|---|---|
| **M1. Foundations** | Auth (JWT + RBAC), org/user model, DB schema, base API scaffolding, Docker setup | FR- (infra) |
| **M2. Job Creation** | Requirement Extraction Agent, JD Generator Agent, approval UI, publish to internal portal | FR-1, FR-2, FR-3 |
| **M3. Candidate Application** | Candidate portal, multi-step application form, consent capture, file upload to object storage | FR-4 |
| **M4. CV Intelligence** | Parsing pipeline (extraction + OCR fallback), structured profile storage | FR-5 |
| **M5. ATS Matching Engine** | Embedding-based semantic matcher, scoring dimensions, evidence generation, ranking | FR-6, FR-7 |
| **M6. Human Review Center** | Recruiter review UI, decision logging, HumanReview entity | FR-8 |
| **M7. AI Interview System** | Adaptive technical interview agent + behavioral interview agent (text chat), rubric scoring | FR-9, FR-10 |
| **M8. Interview Reporting** | Aggregated evaluation report, recommendation surfacing | FR-11 |
| **M9. Scheduling & Communication (basic)** | Manual-availability scheduling, email/notification templates for all state transitions | FR-12 (basic), FR-13 |
| **M10. Timeline & Dashboard** | Candidate timeline, hiring funnel metrics dashboard | FR-14, FR-16 |
| **M11. Orchestrator & State Machine** | The FSM engine wiring all agents together; this is the architectural spine — build early, iterate throughout | 2.7.2–2.7.3 |

**Suggested build order:** M1 → M11 (skeleton state machine with stub agents) → M2 → M3 → M4 → M5 → M6 → M7 → M8 → M9 → M10.
Building the orchestrator skeleton early (with stub/mock agents) lets you demo the full pipeline shape before every agent is fully "smart," then upgrade agents one at a time.

## Phase 2 — V2 (depth & polish)

| Module | Contents | Maps to |
|---|---|---|
| **M12. Agent Observability** | Agent Execution Trace log, Agent Operations Center UI | FR-15 |
| **M13. Multi-Channel Publishing** | External job board integrations (as APIs allow) | FR-3 (extended) |
| **M14. Calendar Integration** | Real calendar API (Google/Outlook) for scheduling | FR-12 (full) |
| **M15. Talent Pool** | Store non-hired strong candidates, auto re-match against new jobs | FR-17 |
| **M16. Company Knowledge Base (RAG)** | Document ingestion, embeddings, retrieval grounding for JD generation & interviews | FR-18 |
| **M17. Advanced Analytics** | Time-to-hire, source analytics, human-override rate, agent success rate | FR-16 (extended) |

## Phase 3 — V3 (intelligence & scale)

| Module | Contents | Maps to |
|---|---|---|
| **M18. Recruitment Intelligence Copilot** | NL Q&A over hiring data with root-cause style answers | FR-19 |
| **M19. Multi-Agent Collaboration** | Agent-to-agent negotiation (e.g., scheduling ↔ candidate ↔ recruiter), richer tool ecosystems | 2.7.2 (extended) |
| **M20. Voice Interviews** | Voice-based AI interview channel | — |
| **M21. Governance Hardening** | Prompt-injection defenses, tool authorization boundaries, formal audit export, data retention automation | Security / FR-15 |

## What to explicitly defer past V1 (per original scope guidance)

- 30+ job-board integrations
- Video interview analysis
- Fully autonomous rejection decisions
- Predictive hiring models
- Payroll / onboarding
- Massive enterprise analytics
- Supporting 20 different LLM providers

---

# 4. Risk Register

| Risk | Impact | Mitigation |
|---|---|---|
| LLM extraction/parsing accuracy too low on messy real-world CVs | Broken candidate profiles, bad matching | Confidence flagging (FR-5), fallback to manual field entry, curated test CV set |
| Scope creep toward the full V3 vision before V1 ships | Project never demos | Hard phase gating (Section 3); V1 checklist must be feature-frozen |
| LLM cost/latency during interviews | Poor candidate UX | Async where possible, cap adaptive follow-ups per skill, cache/reuse embeddings |
| Bias or unfair scoring perceived in ATS matching | Trust/ethical risk | Mandatory evidence-with-every-score (FR-6), human gate before any rejection (FR-8) |
| Data privacy of CVs/PII | Legal/ethical risk, portfolio credibility | Encryption at rest, tenant isolation, consent capture (FR-4), audit log |

---

# 5. Success Metrics (for demo/portfolio purposes)

- End-to-end pipeline runs for a real job posting from natural-language input to a scheduled HR interview, with zero manual data entry outside the intended human-review gates.
- ≥90% CV field-extraction accuracy on a 30-CV test set.
- Every AI recommendation in the demo has visible, human-readable evidence.
- Zero candidates reach `REJECTED` or `HIRED` without a logged human decision.
- Agent Execution Trace can reconstruct the full lifecycle of any single candidate for a demo walkthrough.

---

*End of document. This SRS is intended as a living document — update Section 3's phase boundaries as the actual build progresses, and keep FR acceptance criteria in sync with what's actually implemented for accurate portfolio/interview claims.*
