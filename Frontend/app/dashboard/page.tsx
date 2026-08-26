"use client";

import { useEffect, useState } from "react";
import Link from "next/link";
import { api, ApiError } from "@/lib/api";
import type { Job } from "@/lib/types";
import { JobStatusBadge } from "@/components/StatusBadge";

export default function DashboardPage() {
  const [jobs, setJobs] = useState<Job[] | null>(null);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    api
      .listJobs()
      .then(setJobs)
      .catch((err) => setError(err instanceof ApiError ? err.message : "Couldn't load jobs."));
  }, []);

  return (
    <div>
      <div className="mb-8 flex items-center justify-between">
        <div>
          <h1 className="font-display text-2xl font-semibold text-console-text">Requisitions</h1>
          <p className="mt-1 text-sm text-console-muted">
            Every job your org has drafted, published, or closed.
          </p>
        </div>
        <Link
          href="/dashboard/jobs/new"
          className="rounded-md bg-signal-go px-4 py-2.5 text-sm font-medium text-console-bg transition-opacity hover:opacity-90"
        >
          New requisition
        </Link>
      </div>

      {error && (
        <p className="mb-4 rounded-md border border-signal-stop/30 bg-signal-stop/10 px-3 py-2 text-sm text-signal-stop">
          {error}
        </p>
      )}

      {jobs === null && !error && (
        <p className="font-mono text-xs uppercase tracking-widest text-console-faint">Loading…</p>
      )}

      {jobs && jobs.length === 0 && (
        <div className="rounded-lg border border-dashed border-console-border p-12 text-center">
          <p className="text-console-muted">
            No requisitions yet. Describe a role in plain text and Hirely will draft the JD.
          </p>
          <Link
            href="/dashboard/jobs/new"
            className="mt-4 inline-block text-sm text-signal-go hover:underline"
          >
            Create your first requisition →
          </Link>
        </div>
      )}

      {jobs && jobs.length > 0 && (
        <div className="overflow-hidden rounded-lg border border-console-border">
          <table className="w-full text-left text-sm">
            <thead>
              <tr className="border-b border-console-border bg-console-surface text-xs uppercase tracking-wide text-console-muted">
                <th className="px-4 py-3 font-medium">Title</th>
                <th className="px-4 py-3 font-medium">Status</th>
                <th className="px-4 py-3 font-medium" />
              </tr>
            </thead>
            <tbody>
              {jobs.map((job) => (
                <tr
                  key={job.id}
                  className="border-b border-console-border last:border-0 hover:bg-console-surface/60"
                >
                  <td className="px-4 py-3 text-console-text">{job.title}</td>
                  <td className="px-4 py-3">
                    <JobStatusBadge status={job.status} />
                  </td>
                  <td className="px-4 py-3 text-right">
                    <Link href={`/dashboard/jobs/${job.id}`} className="text-signal-go hover:underline">
                      Open →
                    </Link>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
    </div>
  );
}
