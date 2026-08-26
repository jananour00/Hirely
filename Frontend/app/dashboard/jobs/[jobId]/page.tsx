"use client";

import { useEffect, useState } from "react";
import { useParams } from "next/navigation";
import Link from "next/link";
import { api, ApiError } from "@/lib/api";
import type { Job, JobApplicationSummary } from "@/lib/types";
import { ApplicationStatusBadge, JobStatusBadge } from "@/components/StatusBadge";

export default function JobDetailPage() {
  const { jobId } = useParams<{ jobId: string }>();
  const id = Number(jobId);

  const [job, setJob] = useState<Job | null>(null);
  const [applications, setApplications] = useState<JobApplicationSummary[] | null>(null);
  const [jdDraft, setJdDraft] = useState("");
  const [error, setError] = useState<string | null>(null);
  const [publishing, setPublishing] = useState(false);

  useEffect(() => {
    api
      .getJob(id)
      .then((j) => {
        setJob(j);
        setJdDraft(j.jd_text ?? "");
      })
      .catch((err) => setError(err instanceof ApiError ? err.message : "Couldn't load job."));
  }, [id]);

  useEffect(() => {
    if (job?.status === "open" || job?.status === "closed") {
      api.listJobApplications(id).then(setApplications).catch(() => setApplications([]));
    }
  }, [job, id]);

  async function handlePublish() {
    setPublishing(true);
    setError(null);
    try {
      const updated = await api.approveJob(id, jdDraft);
      setJob(updated);
    } catch (err) {
      setError(err instanceof ApiError ? err.message : "Couldn't publish the job.");
    } finally {
      setPublishing(false);
    }
  }

  if (!job) {
    return (
      <p className="font-mono text-xs uppercase tracking-widest text-console-faint">
        {error ?? "Loading…"}
      </p>
    );
  }

  const isPendingApproval = job.status === "pending_approval";

  return (
    <div>
      <Link href="/dashboard" className="text-sm text-console-muted hover:text-console-text">
        ← All requisitions
      </Link>

      <div className="mt-4 mb-8 flex items-center gap-3">
        <h1 className="font-display text-2xl font-semibold text-console-text">{job.title}</h1>
        <JobStatusBadge status={job.status} />
      </div>

      {error && (
        <p className="mb-4 rounded-md border border-signal-stop/30 bg-signal-stop/10 px-3 py-2 text-sm text-signal-stop">
          {error}
        </p>
      )}

      <section className="mb-10">
        <div className="mb-3 flex items-center justify-between">
          <h2 className="font-mono text-xs uppercase tracking-wide text-console-muted">
            Job description
          </h2>
          {isPendingApproval && (
            <span className="font-mono text-[10px] uppercase tracking-wide text-signal-pending">
              Awaiting your edits before publish
            </span>
          )}
        </div>

        {isPendingApproval ? (
          <>
            <textarea
              rows={16}
              value={jdDraft}
              onChange={(e) => setJdDraft(e.target.value)}
              className="w-full resize-y rounded-md border border-console-border bg-console-surface px-4 py-3 text-sm leading-relaxed text-console-text outline-none focus:border-signal-go"
            />
            <button
              onClick={handlePublish}
              disabled={publishing}
              className="mt-3 rounded-md bg-signal-go px-5 py-2.5 text-sm font-medium text-console-bg transition-opacity hover:opacity-90 disabled:opacity-50"
            >
              {publishing ? "Publishing…" : "Publish to careers site"}
            </button>
          </>
        ) : (
          <div className="whitespace-pre-wrap rounded-md border border-console-border bg-console-surface px-4 py-3 text-sm leading-relaxed text-console-text">
            {job.jd_text || "No description generated."}
          </div>
        )}
      </section>

      {(job.status === "open" || job.status === "closed") && (
        <section>
          <h2 className="mb-3 font-mono text-xs uppercase tracking-wide text-console-muted">
            Applicants
          </h2>

          {applications === null && (
            <p className="font-mono text-xs uppercase tracking-widest text-console-faint">
              Loading…
            </p>
          )}

          {applications && applications.length === 0 && (
            <div className="rounded-lg border border-dashed border-console-border p-8 text-center text-sm text-console-muted">
              No applicants yet.
            </div>
          )}

          {applications && applications.length > 0 && (
            <div className="overflow-hidden rounded-lg border border-console-border">
              <table className="w-full text-left text-sm">
                <thead>
                  <tr className="border-b border-console-border bg-console-surface text-xs uppercase tracking-wide text-console-muted">
                    <th className="px-4 py-3 font-medium">Candidate</th>
                    <th className="px-4 py-3 font-medium">Status</th>
                    <th className="px-4 py-3 font-medium">Score</th>
                    <th className="px-4 py-3 font-medium" />
                  </tr>
                </thead>
                <tbody>
                  {applications.map((a) => (
                    <tr
                      key={a.application_id}
                      className="border-b border-console-border last:border-0 hover:bg-console-surface/60"
                    >
                      <td className="px-4 py-3">
                        <div className="text-console-text">{a.candidate_name}</div>
                        <div className="text-xs text-console-faint">{a.candidate_email}</div>
                      </td>
                      <td className="px-4 py-3">
                        <ApplicationStatusBadge status={a.status} />
                      </td>
                      <td className="px-4 py-3 font-mono text-console-text">
                        {a.overall_score !== null ? Math.round(a.overall_score) : "—"}
                      </td>
                      <td className="px-4 py-3 text-right">
                        <Link
                          href={`/dashboard/applications/${a.application_id}`}
                          className="text-signal-go hover:underline"
                        >
                          Review →
                        </Link>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          )}
        </section>
      )}
    </div>
  );
}
