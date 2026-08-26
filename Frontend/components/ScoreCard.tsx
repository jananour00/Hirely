interface Props {
  overallScore: number | null;
  dimensionScores: Record<string, number> | null;
  strengths: string[] | null;
  gaps: string[] | null;
}

function scoreTone(score: number) {
  if (score >= 75) return "text-signal-go";
  if (score >= 50) return "text-signal-pending";
  return "text-signal-stop";
}

/**
 * The Human Review gate is deliberately never a bare percentage (FR-8) — this
 * always renders the per-dimension evidence and strengths/gaps the ATS agent
 * produced, next to the number, so a recruiter is looking at reasoning, not
 * a score they have to trust blindly.
 */
export default function ScoreCard({ overallScore, dimensionScores, strengths, gaps }: Props) {
  if (overallScore === null) {
    return (
      <div className="rounded-lg border border-console-border bg-console-surface p-6 text-sm text-console-muted">
        No ATS evaluation yet — advance the application to run screening first.
      </div>
    );
  }

  return (
    <div className="rounded-lg border border-console-border bg-console-surface p-6">
      <div className="flex items-baseline gap-3">
        <span className={`font-display text-4xl font-semibold ${scoreTone(overallScore)}`}>
          {Math.round(overallScore)}
        </span>
        <span className="font-mono text-xs uppercase tracking-wide text-console-muted">
          overall match
        </span>
      </div>

      {dimensionScores && Object.keys(dimensionScores).length > 0 && (
        <div className="mt-5 space-y-3">
          {Object.entries(dimensionScores).map(([dimension, score]) => (
            <div key={dimension}>
              <div className="mb-1 flex items-center justify-between text-xs">
                <span className="text-console-muted">{dimension.replace(/_/g, " ")}</span>
                <span className="font-mono text-console-text">{Math.round(score)}</span>
              </div>
              <div className="h-1.5 w-full rounded-full bg-console-raised">
                <div
                  className="h-1.5 rounded-full bg-signal-go"
                  style={{ width: `${Math.min(100, Math.max(0, score))}%` }}
                />
              </div>
            </div>
          ))}
        </div>
      )}

      <div className="mt-6 grid gap-4 sm:grid-cols-2">
        <div>
          <h4 className="mb-2 font-mono text-[10px] uppercase tracking-wide text-signal-go">
            Strengths
          </h4>
          {strengths && strengths.length > 0 ? (
            <ul className="space-y-1 text-sm text-console-text">
              {strengths.map((s, i) => (
                <li key={i} className="flex gap-2">
                  <span className="text-signal-go">+</span>
                  {s}
                </li>
              ))}
            </ul>
          ) : (
            <p className="text-sm text-console-faint">None recorded.</p>
          )}
        </div>
        <div>
          <h4 className="mb-2 font-mono text-[10px] uppercase tracking-wide text-signal-stop">
            Gaps
          </h4>
          {gaps && gaps.length > 0 ? (
            <ul className="space-y-1 text-sm text-console-text">
              {gaps.map((g, i) => (
                <li key={i} className="flex gap-2">
                  <span className="text-signal-stop">−</span>
                  {g}
                </li>
              ))}
            </ul>
          ) : (
            <p className="text-sm text-console-faint">None recorded.</p>
          )}
        </div>
      </div>
    </div>
  );
}
