// Mirrors Backend/app/schemas/*.py and the enums in Backend/app/models/*.py.
// Keep these in sync by hand — there's no shared codegen yet.

export type UserRole = "admin" | "recruiter";

export type JobStatus = "draft" | "pending_approval" | "open" | "closed";

export type ApplicationStatus =
  | "applied"
  | "cv_processing"
  | "ats_screening"
  | "human_review"
  | "ai_interview"
  | "interview_evaluation"
  | "hr_scheduling"
  | "hr_interview"
  | "offer"
  | "hired"
  | "rejected";

export type ReviewDecision = "approve" | "reject" | "request_info" | "advance";

// The full pipeline, in order, for rendering a progress tracker.
// HUMAN_REVIEW is a deliberate gate: nothing advances past it automatically.
export const PIPELINE_STAGES: ApplicationStatus[] = [
  "applied",
  "cv_processing",
  "ats_screening",
  "human_review",
  "ai_interview",
  "interview_evaluation",
  "hr_scheduling",
  "hr_interview",
  "offer",
  "hired",
];

export const STAGE_LABELS: Record<ApplicationStatus, string> = {
  applied: "Applied",
  cv_processing: "Parsing resume",
  ats_screening: "ATS screening",
  human_review: "Human review",
  ai_interview: "AI interview",
  interview_evaluation: "Interview evaluation",
  hr_scheduling: "Scheduling",
  hr_interview: "HR interview",
  offer: "Offer",
  hired: "Hired",
  rejected: "Not moving forward",
};

export interface User {
  id: number;
  email: string;
  name: string;
  role: UserRole;
  org_id: number;
}

export interface Job {
  id: number;
  title: string;
  status: JobStatus;
  requirements_json: Record<string, unknown> | null;
  jd_text: string | null;
}

export interface PublicJob {
  id: number;
  title: string;
  jd_text: string | null;
}

export interface JobApplicationSummary {
  application_id: number;
  candidate_id: number;
  candidate_name: string;
  candidate_email: string;
  status: ApplicationStatus;
  submitted_at: string;
  overall_score: number | null;
}

export interface Application {
  id: number;
  job_id: number;
  candidate_id: number;
  status: ApplicationStatus;
  submitted_at: string;
}

export interface ApplicationReview {
  application_id: number;
  application_status: ApplicationStatus;
  candidate_id: number;
  overall_score: number | null;
  dimension_scores: Record<string, number> | null;
  strengths: string[] | null;
  gaps: string[] | null;
}

export interface HumanReviewResult {
  id: number;
  application_id: number;
  reviewer_id: number;
  decision: ReviewDecision;
  notes: string | null;
  decided_at: string;
}

export interface CandidateProfile {
  id: number;
  candidate_id: number;
  education: unknown[];
  experience: unknown[];
  skills: unknown[];
  projects: unknown[];
  certifications: unknown[];
  languages: unknown[];
  links: unknown[];
  low_confidence_fields: unknown[];
}
