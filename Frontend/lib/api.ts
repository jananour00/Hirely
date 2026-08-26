import type {
  Application,
  ApplicationReview,
  CandidateProfile,
  HumanReviewResult,
  Job,
  JobApplicationSummary,
  PublicJob,
  ReviewDecision,
  User,
} from "./types";

const API_URL = process.env.NEXT_PUBLIC_API_URL ?? "http://localhost:8000";
const TOKEN_KEY = "hirely_token";

export class ApiError extends Error {
  status: number;
  constructor(status: number, message: string) {
    super(message);
    this.status = status;
  }
}

export function getToken(): string | null {
  if (typeof window === "undefined") return null;
  return window.localStorage.getItem(TOKEN_KEY);
}

export function setToken(token: string) {
  window.localStorage.setItem(TOKEN_KEY, token);
}

export function clearToken() {
  window.localStorage.removeItem(TOKEN_KEY);
}

async function request<T>(
  path: string,
  options: RequestInit & { auth?: boolean } = {}
): Promise<T> {
  const { auth = false, headers, ...rest } = options;
  const finalHeaders = new Headers(headers);

  if (auth) {
    const token = getToken();
    if (token) finalHeaders.set("Authorization", `Bearer ${token}`);
  }

  const res = await fetch(`${API_URL}${path}`, { ...rest, headers: finalHeaders });

  if (!res.ok) {
    let detail = res.statusText;
    try {
      const body = await res.json();
      detail = body.detail ?? detail;
    } catch {
      // response wasn't JSON — fall back to statusText
    }
    throw new ApiError(res.status, typeof detail === "string" ? detail : JSON.stringify(detail));
  }

  if (res.status === 204) return undefined as T;
  return res.json() as Promise<T>;
}

function jsonBody(body: unknown) {
  return {
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(body),
  };
}

export const api = {
  // ---- auth ----
  register(payload: { org_name: string; name: string; email: string; password: string }) {
    return request<{ access_token: string; token_type: string }>("/auth/register", {
      method: "POST",
      ...jsonBody(payload),
    });
  },
  login(payload: { email: string; password: string }) {
    return request<{ access_token: string; token_type: string }>("/auth/login", {
      method: "POST",
      ...jsonBody(payload),
    });
  },
  me() {
    return request<User>("/users/me", { auth: true });
  },

  // ---- jobs (recruiter console) ----
  listJobs() {
    return request<Job[]>("/jobs/", { auth: true });
  },
  getJob(jobId: number) {
    return request<Job>(`/jobs/${jobId}`, { auth: true });
  },
  createJob(rawDescription: string) {
    return request<Job>("/jobs/", {
      method: "POST",
      auth: true,
      ...jsonBody({ raw_description: rawDescription }),
    });
  },
  approveJob(jobId: number, jdText: string) {
    return request<Job>(`/jobs/${jobId}/approve`, {
      method: "POST",
      auth: true,
      ...jsonBody({ jd_text: jdText }),
    });
  },
  listJobApplications(jobId: number) {
    return request<JobApplicationSummary[]>(`/jobs/${jobId}/applications`, { auth: true });
  },

  // ---- jobs (public careers site) ----
  listPublicJobs() {
    return request<PublicJob[]>("/jobs/public");
  },
  getPublicJob(jobId: number) {
    return request<PublicJob>(`/jobs/${jobId}/public`);
  },

  // ---- candidate application ----
  applyToJob(form: FormData) {
    return request<Application>("/apply/", { method: "POST", body: form });
  },
  getApplicationStatus(applicationId: number) {
    return request<Application>(`/apply/${applicationId}/status`);
  },

  // ---- applications (recruiter console) ----
  advanceApplication(applicationId: number) {
    return request<{ id: number; status: string }>(`/applications/${applicationId}/advance`, {
      method: "POST",
      auth: true,
    });
  },
  getApplicationReview(applicationId: number) {
    return request<ApplicationReview>(`/applications/${applicationId}/review`, { auth: true });
  },
  submitReview(applicationId: number, decision: ReviewDecision, notes?: string) {
    return request<HumanReviewResult>(`/applications/${applicationId}/review`, {
      method: "POST",
      auth: true,
      ...jsonBody({ decision, notes }),
    });
  },
  getCandidateProfile(candidateId: number) {
    return request<CandidateProfile>(`/candidates/${candidateId}/profile`, { auth: true });
  },
};
