import Link from "next/link";
import PipelineTracker from "@/components/PipelineTracker";

export default function Home() {
  return (
    <main className="relative min-h-screen overflow-hidden bg-console-bg bg-trace-grid bg-trace">
      <div className="absolute inset-0 bg-gradient-to-b from-console-bg via-console-bg/95 to-console-bg" />

      <div className="relative mx-auto flex min-h-screen max-w-5xl flex-col justify-center px-6 py-24">
        <span className="mb-6 font-mono text-xs uppercase tracking-[0.3em] text-signal-go">
          Agentic recruitment, v1
        </span>
        <h1 className="max-w-3xl font-display text-5xl font-semibold leading-[1.05] text-console-text sm:text-6xl">
          Every hire, traced from{" "}
          <span className="text-signal-go">applied</span> to{" "}
          <span className="text-signal-go">hired</span>.
        </h1>
        <p className="mt-6 max-w-xl text-lg text-console-muted">
          Hirely runs your requisition through requirement extraction, resume parsing,
          and ATS scoring — then stops for a human at the one gate that matters, before
          anyone is rejected.
        </p>

        <div className="mt-10 flex flex-wrap gap-4">
          <Link
            href="/login"
            className="rounded-md bg-signal-go px-5 py-3 font-medium text-console-bg transition-opacity hover:opacity-90"
          >
            Sign in to the console
          </Link>
          <Link
            href="/careers"
            className="rounded-md border border-console-border px-5 py-3 font-medium text-console-text transition-colors hover:border-console-borderLight"
          >
            Browse open roles
          </Link>
        </div>

        <div className="mt-20 rounded-lg border border-console-border bg-console-surface/60 p-6">
          <p className="mb-4 font-mono text-[10px] uppercase tracking-wide text-console-muted">
            Live pipeline shape
          </p>
          <PipelineTracker status="ats_screening" />
        </div>
      </div>
    </main>
  );
}
