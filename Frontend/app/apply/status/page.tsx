"use client";

import { FormEvent, Suspense, useEffect, useState } from "react";
import { useSearchParams } from "next/navigation";
import { api, ApiError } from "@/lib/api";
import type { Application } from "@/lib/types";
import { STAGE_LABELS } from "@/lib/types";
import PaperNav from "@/components/PaperNav";
import PipelineTracker from "@/components/PipelineTracker";

function StatusChecker() {
  const searchParams = useSearchParams();
  const initialId = searchParams.get("id") ?? "";

  const [applicationId, setApplicationId] = useState(initialId);
  const [application, setApplication] = useState<Application | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);

  async function lookup(id: string) {
    if (!id) return;
    setLoading(true);
    setError(null);
    setApplication(null);
    try {
      const app = await api.getApplicationStatus(Number(id));
      setApplication(app);
    } catch (err) {
      setError(
        err instanceof ApiError
          ? "No application found with that number."
          : "Couldn't check status right now."
      );
    } finally {
      setLoading(false);
    }
  }

  useEffect(() => {
    if (initialId) lookup(initialId);
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  function handleSubmit(e: FormEvent) {
    e.preventDefault();
    lookup(applicationId);
  }

  return (
    <main className="min-h-screen bg-paper-bg">
      <PaperNav />
      <div className="mx-auto max-w-xl px-6 py-16">
        <h1 className="mb-2 font-display text-3xl font-semibold text-paper-text">
          Check your application
        </h1>
        <p className="mb-8 text-paper-muted">
          Enter the application number you received when you applied.
        </p>

        <form onSubmit={handleSubmit} className="mb-10 flex gap-3">
          <input
            value={applicationId}
            onChange={(e) => setApplicationId(e.target.value)}
            placeholder="e.g. 42"
            inputMode="numeric"
            className="flex-1 rounded-md border border-paper-border bg-paper-surface px-3 py-2.5 text-sm text-paper-text outline-none focus:border-paper-text/50"
          />
          <button
            type="submit"
            disabled={loading}
            className="rounded-md bg-paper-text px-5 py-2.5 text-sm font-medium text-paper-bg transition-opacity hover:opacity-90 disabled:opacity-50"
          >
            {loading ? "Checking…" : "Check"}
          </button>
        </form>

        {error && <p className="text-sm text-signal-stop">{error}</p>}

        {application && (
          <div className="rounded-lg border border-paper-border bg-paper-surface p-6">
            <p className="mb-1 font-mono text-xs uppercase tracking-wide text-paper-muted">
              Application #{application.id}
            </p>
            <p className="mb-6 font-display text-xl font-semibold text-paper-text">
              {application.status === "rejected"
                ? "Not moving forward this time"
                : STAGE_LABELS[application.status]}
            </p>
            <div className="rounded-md bg-console-bg p-5">
              <PipelineTracker status={application.status} compact />
            </div>
          </div>
        )}
      </div>
    </main>
  );
}

export default function ApplicationStatusPage() {
  return (
    <Suspense
      fallback={
        <main className="min-h-screen bg-paper-bg">
          <PaperNav />
        </main>
      }
    >
      <StatusChecker />
    </Suspense>
  );
}
