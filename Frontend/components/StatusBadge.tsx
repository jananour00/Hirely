type Tone = "go" | "pending" | "hold" | "stop";

const TONE_CLASSES: Record<Tone, string> = {
  go: "bg-signal-go/10 text-signal-go border-signal-go/30",
  pending: "bg-signal-pending/10 text-signal-pending border-signal-pending/30",
  hold: "bg-signal-hold/10 text-signal-hold border-signal-hold/30",
  stop: "bg-signal-stop/10 text-signal-stop border-signal-stop/30",
};

const JOB_STATUS_TONE: Record<string, Tone> = {
  draft: "hold",
  pending_approval: "pending",
  open: "go",
  closed: "stop",
};

const APPLICATION_STATUS_TONE: Record<string, Tone> = {
  applied: "hold",
  cv_processing: "pending",
  ats_screening: "pending",
  human_review: "pending",
  ai_interview: "pending",
  interview_evaluation: "pending",
  hr_scheduling: "pending",
  hr_interview: "pending",
  offer: "go",
  hired: "go",
  rejected: "stop",
};

export function JobStatusBadge({ status }: { status: string }) {
  const tone = JOB_STATUS_TONE[status] ?? "hold";
  return (
    <span
      className={`inline-flex items-center rounded-full border px-2.5 py-0.5 font-mono text-[10px] uppercase tracking-wide ${TONE_CLASSES[tone]}`}
    >
      {status.replace(/_/g, " ")}
    </span>
  );
}

export function ApplicationStatusBadge({ status }: { status: string }) {
  const tone = APPLICATION_STATUS_TONE[status] ?? "hold";
  return (
    <span
      className={`inline-flex items-center rounded-full border px-2.5 py-0.5 font-mono text-[10px] uppercase tracking-wide ${TONE_CLASSES[tone]}`}
    >
      {status.replace(/_/g, " ")}
    </span>
  );
}
