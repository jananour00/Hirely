"use client";

import { useEffect, useState } from "react";
import Link from "next/link";
import { api, ApiError } from "@/lib/api";
import type { PublicJob } from "@/lib/types";
import PaperNav from "@/components/PaperNav";

export default function CareersPage() {
  const [jobs, setJobs] = useState<PublicJob[] | null>(null);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    api
      .listPublicJobs()
      .then(setJobs)
      .catch((err) => setError(err instanceof ApiError ? err.message : "Couldn't load roles."));
  }, []);

  return (
    <main className="min-h-screen bg-paper-bg">
      <PaperNav />
      <div className="mx-auto max-w-3xl px-6 py-16">
        <span className="mb-3 block font-mono text-xs uppercase tracking-[0.3em] text-paper-muted">
          Open roles
        </span>
        <h1 className="mb-3 font-display text-4xl font-semibold text-paper-text">
          Find where you fit.
        </h1>
        <p className="mb-12 max-w-xl text-paper-muted">
          Every role below has a human reviewer at the other end — no application disappears
          into a black box.
        </p>

        {error && <p className="text-signal-stop">{error}</p>}
        {jobs === null && !error && <p className="text-paper-muted">Loading…</p>}
        {jobs && jobs.length === 0 && (
          <p className="text-paper-muted">No open roles right now — check back soon.</p>
        )}

        <div className="space-y-3">
          {jobs?.map((job) => (
            <Link
              key={job.id}
              href={`/careers/${job.id}`}
              className="block rounded-lg border border-paper-border bg-paper-surface p-5 transition-colors hover:border-paper-text/30"
            >
              <h2 className="font-display text-lg font-semibold text-paper-text">{job.title}</h2>
              <p className="mt-1 line-clamp-2 text-sm text-paper-muted">
                {job.jd_text?.slice(0, 180) ?? "View details for the full description."}
              </p>
              <span className="mt-3 inline-block text-sm text-paper-text underline decoration-paper-muted underline-offset-4">
                View & apply
              </span>
            </Link>
          ))}
        </div>
      </div>
    </main>
  );
}
