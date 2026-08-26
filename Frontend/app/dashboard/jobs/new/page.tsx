"use client";

import { FormEvent, useState } from "react";
import { useRouter } from "next/navigation";
import { api, ApiError } from "@/lib/api";

export default function NewJobPage() {
  const router = useRouter();
  const [rawDescription, setRawDescription] = useState("");
  const [error, setError] = useState<string | null>(null);
  const [submitting, setSubmitting] = useState(false);

  async function handleSubmit(e: FormEvent) {
    e.preventDefault();
    setError(null);
    setSubmitting(true);
    try {
      const job = await api.createJob(rawDescription);
      router.push(`/dashboard/jobs/${job.id}`);
    } catch (err) {
      setError(err instanceof ApiError ? err.message : "Couldn't draft the requisition.");
      setSubmitting(false);
    }
  }

  return (
    <div className="mx-auto max-w-2xl">
      <h1 className="font-display text-2xl font-semibold text-console-text">New requisition</h1>
      <p className="mt-1 mb-8 text-sm text-console-muted">
        Describe the role in plain language. Hirely's requirement-extraction and JD-generation
        agents turn it into a structured requisition you can review before publishing.
      </p>

      <form onSubmit={handleSubmit} className="space-y-4">
        <div>
          <label htmlFor="raw" className="mb-1.5 block text-xs text-console-muted">
            Role description
          </label>
          <textarea
            id="raw"
            required
            rows={10}
            value={rawDescription}
            onChange={(e) => setRawDescription(e.target.value)}
            placeholder="Senior backend engineer, 5+ years, Python/FastAPI, owns our payments service, remote-friendly, reports to the VP of Engineering…"
            className="w-full resize-y rounded-md border border-console-border bg-console-surface px-3 py-2.5 text-sm text-console-text outline-none focus:border-signal-go"
          />
        </div>

        {error && (
          <p className="rounded-md border border-signal-stop/30 bg-signal-stop/10 px-3 py-2 text-sm text-signal-stop">
            {error}
          </p>
        )}

        <button
          type="submit"
          disabled={submitting}
          className="rounded-md bg-signal-go px-5 py-2.5 text-sm font-medium text-console-bg transition-opacity hover:opacity-90 disabled:opacity-50"
        >
          {submitting ? "Drafting JD…" : "Generate job description"}
        </button>
      </form>
    </div>
  );
}
