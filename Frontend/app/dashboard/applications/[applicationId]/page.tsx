"use client";

import { useCallback, useEffect, useState } from "react";
import { useParams, useRouter } from "next/navigation";
import Link from "next/link";
import { api, ApiError } from "@/lib/api";
import type { ApplicationReview, CandidateProfile, ReviewDecision } from "@/lib/types";
import PipelineTracker from "@/components/PipelineTracker";
import { ApplicationStatusBadge } from "@/components/StatusBadge";
import ScoreCard from "@/components/ScoreCard";

export default function ApplicationReviewPage() {
  const { applicationId } = useParams<{ applicationId: string }>();
  const id = Number(applicationId);
  const router = useRouter();

  const [review, setReview] = useState<ApplicationReview | null>(null);
  const [profile, setProfile] = useState<CandidateProfile | null>(null);
  const [notes, setNotes] = useState("");
  const [error, setError] = useState<string | null>(null);
  const [busy, setBusy] = useState<string | null>(null);

  const load = useCallback(async () => {
    try {
      const r = await api.getApplicationReview(id);
      setReview(r);
      api.getCandidateProfile(r.candidate_id).then(setProfile).catch(() => setProfile(null));
    } catch (err) {
      setError(err instanceof ApiError ? err.message : "Couldn't load this application.");
    }
  }, [id]);

  useEffect(() => {
    load();
  }, [load]);

  async function handleAdvance() {
    setBusy("advance");
    setError(null);
    try {
      await api.advanceApplication(id);
      await load();
    } catch (err) {
      setError(err instanceof ApiError ? err.message : "Couldn't advance the pipeline.");
    } finally {
      setBusy(null);
    }
  }

  async function handleDecision(decision: ReviewDecision) {
    setBusy(decision);
    setError(null);
    try {
      await api.submitReview(id, decision, notes || undefined);
      await load();
    } catch (err) {
      setError(err instanceof ApiError ? err.message : "Couldn't record the decision.");
    } finally {
      setBusy(null);
    }
  }

  if (!review) {
    return (
      <p className="font-mono text-xs uppercase tracking-widest text-console-faint">
        {error ?? "Loading…"}
      </p>
    );
  }

  const status = review.application_status;
  const isPending = ["applied", "cv_processing", "ats_screening"].includes(status);
  const isAtGate = status === "human_review";

  return (
    <div className="mx-auto max-w-3xl">
      <button
        onClick={() => router.back()}
        className="text-sm text-console-muted hover:text-console-text"
      >
        ← Back
      </button>

      <div className="mt-4 mb-2 flex items-center gap-3">
        <h1 className="font-display text-2xl font-semibold text-console-text">
          Application #{review.application_id}
        </h1>
        <ApplicationStatusBadge status={status} />
      </div>

      <div className="mb-8 rounded-lg border border-console-border bg-console-surface p-5">
        <PipelineTracker status={status} />
      </div>

      {error && (
        <p className="mb-4 rounded-md border border-signal-stop/30 bg-signal-stop/10 px-3 py-2 text-sm text-signal-stop">
          {error}
        </p>
      )}

      {isPending && (
        <div className="mb-8 rounded-lg border border-console-border bg-console-surface p-6">
          <p className="mb-3 text-sm text-console-muted">
            This application hasn't reached ATS screening yet. Advance it through resume parsing
            and screening to generate the match evidence below.
          </p>
          <button
            onClick={handleAdvance}
            disabled={busy === "advance"}
            className="rounded-md bg-signal-go px-4 py-2 text-sm font-medium text-console-bg transition-opacity hover:opacity-90 disabled:opacity-50"
          >
            {busy === "advance" ? "Advancing…" : "Advance pipeline"}
          </button>
        </div>
      )}

      <div className="mb-8">
        <h2 className="mb-3 font-mono text-xs uppercase tracking-wide text-console-muted">
          ATS evidence
        </h2>
        <ScoreCard
          overallScore={review.overall_score}
          dimensionScores={review.dimension_scores}
          strengths={review.strengths}
          gaps={review.gaps}
        />
      </div>

      {profile && (
        <div className="mb-8">
          <h2 className="mb-3 font-mono text-xs uppercase tracking-wide text-console-muted">
            Parsed profile
          </h2>
          <div className="grid gap-4 rounded-lg border border-console-border bg-console-surface p-6 sm:grid-cols-2">
            <ProfileList label="Skills" items={profile.skills} />
            <ProfileList label="Experience" items={profile.experience} />
            <ProfileList label="Education" items={profile.education} />
            <ProfileList label="Projects" items={profile.projects} />
          </div>
          {profile.low_confidence_fields.length > 0 && (
            <p className="mt-2 font-mono text-[10px] uppercase tracking-wide text-signal-pending">
              Low-confidence fields — verify against the resume: {profile.low_confidence_fields.join(", ")}
            </p>
          )}
        </div>
      )}

      {isAtGate && (
        <div className="rounded-lg border border-signal-pending/30 bg-signal-pending/5 p-6">
          <h2 className="mb-1 font-display text-lg font-semibold text-console-text">
            Human review gate
          </h2>
          <p className="mb-4 text-sm text-console-muted">
            This is the one stage Hirely never crosses on its own. Your decision — logged with
            your name and a timestamp — is what moves this candidate forward or ends it.
          </p>

          <textarea
            rows={3}
            value={notes}
            onChange={(e) => setNotes(e.target.value)}
            placeholder="Notes for the audit log (optional)"
            className="mb-4 w-full resize-y rounded-md border border-console-border bg-console-surface px-3 py-2.5 text-sm text-console-text outline-none focus:border-signal-go"
          />

          <div className="flex flex-wrap gap-3">
            <button
              onClick={() => handleDecision("approve")}
              disabled={busy !== null}
              className="rounded-md bg-signal-go px-4 py-2 text-sm font-medium text-console-bg transition-opacity hover:opacity-90 disabled:opacity-50"
            >
              {busy === "approve" ? "Recording…" : "Approve → AI interview"}
            </button>
            <button
              onClick={() => handleDecision("request_info")}
              disabled={busy !== null}
              className="rounded-md border border-console-border px-4 py-2 text-sm text-console-text transition-colors hover:border-console-borderLight disabled:opacity-50"
            >
              {busy === "request_info" ? "Recording…" : "Request more info"}
            </button>
            <button
              onClick={() => handleDecision("reject")}
              disabled={busy !== null}
              className="rounded-md border border-signal-stop/40 px-4 py-2 text-sm text-signal-stop transition-colors hover:bg-signal-stop/10 disabled:opacity-50"
            >
              {busy === "reject" ? "Recording…" : "Reject"}
            </button>
          </div>
        </div>
      )}

      {!isPending && !isAtGate && status !== "rejected" && status !== "hired" && (
        <div className="rounded-lg border border-console-border bg-console-surface p-6">
          <p className="mb-3 text-sm text-console-muted">
            Past the human review gate — this stage is still a stub transition in the orchestrator
            (see the project README). Advance manually to move it forward.
          </p>
          <button
            onClick={handleAdvance}
            disabled={busy === "advance"}
            className="rounded-md bg-signal-go px-4 py-2 text-sm font-medium text-console-bg transition-opacity hover:opacity-90 disabled:opacity-50"
          >
            {busy === "advance" ? "Advancing…" : "Advance pipeline"}
          </button>
        </div>
      )}
    </div>
  );
}

function ProfileList({ label, items }: { label: string; items: unknown[] }) {
  return (
    <div>
      <h3 className="mb-2 font-mono text-[10px] uppercase tracking-wide text-console-muted">
        {label}
      </h3>
      {items.length === 0 ? (
        <p className="text-sm text-console-faint">Not found in resume.</p>
      ) : (
        <ul className="space-y-1 text-sm text-console-text">
          {items.map((item, i) => (
            <li key={i}>{typeof item === "string" ? item : JSON.stringify(item)}</li>
          ))}
        </ul>
      )}
    </div>
  );
}
