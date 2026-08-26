"use client";

import { FormEvent, useEffect, useRef, useState } from "react";
import { useParams } from "next/navigation";
import Link from "next/link";
import { api, ApiError } from "@/lib/api";
import type { Application, PublicJob } from "@/lib/types";
import PaperNav from "@/components/PaperNav";

export default function JobApplyPage() {
  const { jobId } = useParams<{ jobId: string }>();
  const id = Number(jobId);

  const [job, setJob] = useState<PublicJob | null>(null);
  const [loadError, setLoadError] = useState<string | null>(null);
  const [submitError, setSubmitError] = useState<string | null>(null);
  const [submitting, setSubmitting] = useState(false);
  const [result, setResult] = useState<Application | null>(null);
  const formRef = useRef<HTMLFormElement>(null);

  useEffect(() => {
    api
      .getPublicJob(id)
      .then(setJob)
      .catch((err) =>
        setLoadError(err instanceof ApiError ? err.message : "Couldn't load this role.")
      );
  }, [id]);

  async function handleSubmit(e: FormEvent<HTMLFormElement>) {
    e.preventDefault();
    setSubmitError(null);
    setSubmitting(true);
    try {
      const form = new FormData(e.currentTarget);
      form.set("job_id", String(id));
      const application = await api.applyToJob(form);
      setResult(application);
    } catch (err) {
      setSubmitError(err instanceof ApiError ? err.message : "Couldn't submit your application.");
    } finally {
      setSubmitting(false);
    }
  }

  if (loadError) {
    return (
      <main className="min-h-screen bg-paper-bg">
        <PaperNav />
        <div className="mx-auto max-w-2xl px-6 py-16">
          <p className="text-signal-stop">{loadError}</p>
          <Link href="/careers" className="mt-4 inline-block text-paper-text underline">
            ← Back to open roles
          </Link>
        </div>
      </main>
    );
  }

  if (!job) {
    return (
      <main className="min-h-screen bg-paper-bg">
        <PaperNav />
        <div className="mx-auto max-w-2xl px-6 py-16 text-paper-muted">Loading…</div>
      </main>
    );
  }

  if (result) {
    return (
      <main className="min-h-screen bg-paper-bg">
        <PaperNav />
        <div className="mx-auto max-w-xl px-6 py-24 text-center">
          <span className="mb-4 inline-block h-3 w-3 rounded-full bg-signal-go" />
          <h1 className="mb-3 font-display text-3xl font-semibold text-paper-text">
            Application received
          </h1>
          <p className="mb-8 text-paper-muted">
            We've got your resume for <strong>{job.title}</strong>. Save your application number
            to check status any time — we don't send status emails yet.
          </p>
          <div className="mb-8 inline-block rounded-md border border-paper-border bg-paper-surface px-6 py-3 font-mono text-2xl text-paper-text">
            #{result.id}
          </div>
          <div>
            <Link
              href={`/apply/status?id=${result.id}`}
              className="text-paper-text underline decoration-paper-muted underline-offset-4"
            >
              Check this application's status →
            </Link>
          </div>
        </div>
      </main>
    );
  }

  return (
    <main className="min-h-screen bg-paper-bg">
      <PaperNav />
      <div className="mx-auto max-w-2xl px-6 py-16">
        <Link href="/careers" className="text-sm text-paper-muted hover:text-paper-text">
          ← All roles
        </Link>

        <h1 className="mt-4 mb-6 font-display text-3xl font-semibold text-paper-text">
          {job.title}
        </h1>

        <div className="mb-12 whitespace-pre-wrap rounded-lg border border-paper-border bg-paper-surface p-6 text-sm leading-relaxed text-paper-text">
          {job.jd_text || "No description available."}
        </div>

        <h2 className="mb-4 font-display text-xl font-semibold text-paper-text">Apply</h2>
        <form ref={formRef} onSubmit={handleSubmit} className="space-y-4" encType="multipart/form-data">
          <div>
            <label htmlFor="candidate_name" className="mb-1.5 block text-xs text-paper-muted">
              Full name
            </label>
            <input
              id="candidate_name"
              name="candidate_name"
              required
              className="w-full rounded-md border border-paper-border bg-paper-surface px-3 py-2.5 text-sm text-paper-text outline-none focus:border-paper-text/50"
            />
          </div>
          <div>
            <label htmlFor="candidate_email" className="mb-1.5 block text-xs text-paper-muted">
              Email
            </label>
            <input
              id="candidate_email"
              name="candidate_email"
              type="email"
              required
              className="w-full rounded-md border border-paper-border bg-paper-surface px-3 py-2.5 text-sm text-paper-text outline-none focus:border-paper-text/50"
            />
          </div>
          <div>
            <label htmlFor="resume" className="mb-1.5 block text-xs text-paper-muted">
              Resume (PDF or DOCX)
            </label>
            <input
              id="resume"
              name="resume"
              type="file"
              accept=".pdf,.doc,.docx"
              required
              className="w-full rounded-md border border-paper-border bg-paper-surface px-3 py-2.5 text-sm text-paper-text file:mr-3 file:rounded file:border-0 file:bg-paper-text file:px-3 file:py-1.5 file:text-paper-bg"
            />
          </div>
          <label className="flex items-start gap-2 text-sm text-paper-muted">
            <input type="checkbox" name="consent" value="true" required className="mt-1" />
            I consent to Hirely processing my resume and application data to evaluate this
            application, per the org's hiring process.
          </label>

          {submitError && <p className="text-sm text-signal-stop">{submitError}</p>}

          <button
            type="submit"
            disabled={submitting}
            className="rounded-md bg-paper-text px-5 py-2.5 text-sm font-medium text-paper-bg transition-opacity hover:opacity-90 disabled:opacity-50"
          >
            {submitting ? "Submitting…" : "Submit application"}
          </button>
        </form>
      </div>
    </main>
  );
}
