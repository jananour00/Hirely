import { ApplicationStatus, PIPELINE_STAGES, STAGE_LABELS } from "@/lib/types";

interface Props {
  status: ApplicationStatus;
  compact?: boolean;
}

/**
 * Renders the application lifecycle as a signal trace: completed stages are
 * lit, the current stage pulses, future stages sit dim. HUMAN_REVIEW is
 * marked as a gate — it's the one stage `/advance` can never skip past on
 * its own (see Backend/orchestrator/engine.py).
 */
export default function PipelineTracker({ status, compact = false }: Props) {
  if (status === "rejected") {
    return (
      <div className="flex items-center gap-2 font-mono text-xs uppercase tracking-wider text-signal-stop">
        <span className="h-2 w-2 rounded-full bg-signal-stop" />
        Not moving forward
      </div>
    );
  }

  const currentIndex = PIPELINE_STAGES.indexOf(status);

  return (
    <div className="w-full overflow-x-auto">
      <div className={`flex items-center ${compact ? "gap-1" : "gap-1.5"} min-w-max`}>
        {PIPELINE_STAGES.map((stage, i) => {
          const isDone = i < currentIndex;
          const isCurrent = i === currentIndex;
          const isGate = stage === "human_review";

          return (
            <div key={stage} className="flex items-center">
              <div className="flex flex-col items-center gap-1.5">
                <div
                  className={[
                    "flex items-center justify-center rounded-full border transition-colors",
                    compact ? "h-2.5 w-2.5" : "h-3 w-3",
                    isDone
                      ? "border-signal-go bg-signal-go"
                      : isCurrent
                      ? isGate
                        ? "border-signal-pending bg-signal-pending animate-pulse"
                        : "border-signal-go bg-signal-go animate-pulse"
                      : "border-console-borderLight bg-transparent",
                  ].join(" ")}
                />
                {!compact && (
                  <span
                    className={[
                      "font-mono text-[10px] uppercase tracking-wide whitespace-nowrap",
                      isDone || isCurrent ? "text-console-text" : "text-console-faint",
                    ].join(" ")}
                  >
                    {STAGE_LABELS[stage]}
                  </span>
                )}
              </div>
              {i < PIPELINE_STAGES.length - 1 && (
                <div
                  className={[
                    compact ? "h-px w-4" : "h-px w-8",
                    "mx-0.5",
                    isDone ? "bg-signal-go" : "bg-console-borderLight",
                  ].join(" ")}
                />
              )}
            </div>
          );
        })}
      </div>
    </div>
  );
}
