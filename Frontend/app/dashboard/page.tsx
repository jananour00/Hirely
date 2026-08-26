"use client";

import { useEffect, useState } from "react";
import Link from "next/link";
import { api, ApiError } from "@/lib/api";
import type { Job } from "@/lib/types";
import { JobStatusBadge } from "@/components/StatusBadge";

const demoJobs = [
  { id: 101, title: "Senior Product Designer", status: "published", location: "New York · Hybrid", applicants: 48, shortlisted: 12, age: "2d ago" },
  { id: 102, title: "Backend Engineer, Payments", status: "draft", location: "Remote · US timezones", applicants: 0, shortlisted: 0, age: "Edited today" },
  { id: 103, title: "Customer Success Lead", status: "published", location: "Austin · Hybrid", applicants: 31, shortlisted: 8, age: "5d ago" },
] as const;

export default function DashboardPage() {
  const [jobs, setJobs] = useState<Job[] | null>(null);
  const [error, setError] = useState<string | null>(null);
  useEffect(() => { api.listJobs().then(setJobs).catch((err) => setError(err instanceof ApiError ? err.message : "Showing demo workspace.")); }, []);
  const rows = jobs && jobs.length ? jobs : demoJobs;
  return (
    <main className="flex flex-col gap-8">
      <div className="flex flex-col justify-between gap-5 md:flex-row md:items-end">
        <div><p className="font-mono text-xs uppercase tracking-[0.24em] text-signal-go">Monday, August 26</p><h1 className="mt-2 font-display text-3xl font-semibold tracking-tight text-console-text">Good morning, Alex.</h1><p className="mt-2 max-w-xl text-sm text-console-muted">Your hiring room is calm. Here&apos;s what deserves your attention today.</p></div>
        <Link href="/dashboard/jobs/new" className="inline-flex items-center justify-center rounded-md bg-signal-go px-4 py-2.5 text-sm font-medium text-console-bg transition-opacity hover:opacity-90">+ New requisition</Link>
      </div>
      {error && <p className="rounded-md border border-console-border bg-console-surface px-3 py-2 text-sm text-console-muted">{error} Fictional workspace data is shown below.</p>}
      <section aria-label="Hiring overview" className="grid gap-3 sm:grid-cols-2 lg:grid-cols-4">
        <div className="metric-box"><span className="metric-label">Open roles</span><span className="metric-value">08</span><span className="metric-detail text-signal-go">↑ 2 this month</span></div>
        <div className="metric-box"><span className="metric-label">New applicants</span><span className="metric-value">79</span><span className="metric-detail">Across 3 active roles</span></div>
        <div className="metric-box"><span className="metric-label">Human review</span><span className="metric-value">14</span><span className="metric-detail text-signal-pending">Needs your decision</span></div>
        <div className="metric-box"><span className="metric-label">Avg. time to review</span><span className="metric-value">1.8d</span><span className="metric-detail">↓ 0.4d vs last month</span></div>
      </section>
      <div className="grid gap-6 lg:grid-cols-[1.5fr_1fr]">
        <section className="rounded-lg border border-console-border bg-console-surface"><div className="flex items-center justify-between border-b border-console-border px-5 py-4"><div><h2 className="font-display font-semibold text-console-text">Active requisitions</h2><p className="mt-1 text-xs text-console-muted">Roles currently moving through your funnel</p></div><Link href="/dashboard" className="font-mono text-xs uppercase tracking-wide text-signal-go">View all</Link></div><div className="flex flex-col">{rows.map((job, i) => { const demo = demoJobs[i % demoJobs.length]; return <Link key={job.id} href={`/dashboard/jobs/${job.id}`} className="flex items-center justify-between gap-4 border-b border-console-border px-5 py-4 transition-colors last:border-0 hover:bg-console-bg/50"><div className="min-w-0"><h3 className="truncate text-sm font-medium text-console-text">{job.title}</h3><p className="mt-1 text-xs text-console-muted">{demo.location} · {demo.applicants} applicants</p></div><div className="flex shrink-0 items-center gap-3"><JobStatusBadge status={job.status} /><span className="hidden text-xs text-console-faint sm:inline">{demo.age}</span><span className="text-console-muted">→</span></div></Link>; })}</div></section>
        <section className="rounded-lg border border-console-border bg-console-surface p-5"><div className="flex items-center justify-between"><div><h2 className="font-display font-semibold text-console-text">Funnel snapshot</h2><p className="mt-1 text-xs text-console-muted">All active roles · last 30 days</p></div><span className="font-mono text-xs text-signal-go">+18%</span></div><div className="mt-6 flex flex-col gap-4">{[["Applied","79","w-full"],["ATS screened","42","w-[72%]"],["Human review","14","w-[42%]"],["Interview","6","w-[24%]"],["Offer","2","w-[12%]"]].map(([label,count,width]) => <div key={label} className="flex items-center gap-3 text-xs"><span className="w-24 text-console-muted">{label}</span><div className="h-2 flex-1 rounded-full bg-console-bg"><div className={`h-full rounded-full bg-signal-go ${width}`} /></div><span className="w-7 text-right font-mono text-console-text">{count}</span></div>)}</div><div className="mt-7 border-t border-console-border pt-4"><p className="text-xs leading-5 text-console-muted">Hirely surfaces evidence and keeps every final decision with your team.</p></div></section>
      </div>
      <section className="rounded-lg border border-console-border bg-console-surface p-5"><div className="flex items-center justify-between"><h2 className="font-display font-semibold text-console-text">Recent activity</h2><span className="font-mono text-[10px] uppercase tracking-widest text-console-faint">Live log</span></div><div className="mt-4 grid gap-3 text-sm sm:grid-cols-3"><p className="border-l-2 border-signal-go pl-3 text-console-muted"><strong className="block font-medium text-console-text">Maya Chen advanced</strong>Senior Product Designer to human review · 12m ago</p><p className="border-l-2 border-console-borderLight pl-3 text-console-muted"><strong className="block font-medium text-console-text">New requisition drafted</strong>Backend Engineer, Payments · 2h ago</p><p className="border-l-2 border-console-borderLight pl-3 text-console-muted"><strong className="block font-medium text-console-text">Jordan Lee commented</strong>On Customer Success Lead · Yesterday</p></div></section>
    </main>
  );
}
