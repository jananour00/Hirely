import Link from "next/link";

export default function PaperNav() {
  return (
    <header className="border-b border-paper-border bg-paper-bg">
      <div className="mx-auto flex max-w-5xl items-center justify-between px-6 py-5">
        <Link href="/careers" className="flex items-center gap-2 font-display text-lg font-semibold text-paper-text">
          <span className="h-2 w-2 rounded-full bg-signal-go" />
          Hirely
          <span className="font-mono text-[10px] uppercase tracking-widest text-paper-muted">
            careers
          </span>
        </Link>
        <nav className="flex items-center gap-6 text-sm text-paper-muted">
          <Link href="/apply/status" className="hover:text-paper-text">
            Check application
          </Link>
          <Link
            href="/login"
            className="rounded-md border border-paper-text/20 px-3 py-1.5 text-paper-text hover:border-paper-text/40"
          >
            Recruiter sign in
          </Link>
        </nav>
      </div>
    </header>
  );
}
