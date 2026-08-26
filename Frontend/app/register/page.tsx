"use client";

import { FormEvent, useState } from "react";
import Link from "next/link";
import { useAuth } from "@/lib/auth";
import { ApiError } from "@/lib/api";

export default function RegisterPage() {
  const { register } = useAuth();
  const [orgName, setOrgName] = useState("");
  const [name, setName] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState<string | null>(null);
  const [submitting, setSubmitting] = useState(false);

  async function handleSubmit(e: FormEvent) {
    e.preventDefault();
    setError(null);
    setSubmitting(true);
    try {
      await register({ org_name: orgName, name, email, password });
    } catch (err) {
      setError(err instanceof ApiError ? err.message : "Couldn't create the account. Try again.");
    } finally {
      setSubmitting(false);
    }
  }

  return (
    <main className="flex min-h-screen items-center justify-center bg-console-bg px-6 py-16">
      <div className="w-full max-w-sm">
        <Link href="/" className="mb-8 flex items-center gap-2 font-display text-lg font-semibold">
          <span className="h-2 w-2 rounded-full bg-signal-go" />
          Hirely
        </Link>

        <h1 className="mb-1 font-display text-2xl font-semibold text-console-text">
          Set up your organization
        </h1>
        <p className="mb-8 text-sm text-console-muted">
          The first account you create becomes the org admin.
        </p>

        <form onSubmit={handleSubmit} className="space-y-4">
          <div>
            <label htmlFor="orgName" className="mb-1.5 block text-xs text-console-muted">
              Organization name
            </label>
            <input
              id="orgName"
              required
              value={orgName}
              onChange={(e) => setOrgName(e.target.value)}
              className="w-full rounded-md border border-console-border bg-console-surface px-3 py-2.5 text-sm text-console-text outline-none focus:border-signal-go"
              placeholder="Acme Inc."
            />
          </div>
          <div>
            <label htmlFor="name" className="mb-1.5 block text-xs text-console-muted">
              Your name
            </label>
            <input
              id="name"
              required
              value={name}
              onChange={(e) => setName(e.target.value)}
              className="w-full rounded-md border border-console-border bg-console-surface px-3 py-2.5 text-sm text-console-text outline-none focus:border-signal-go"
              placeholder="Jordan Lee"
            />
          </div>
          <div>
            <label htmlFor="email" className="mb-1.5 block text-xs text-console-muted">
              Work email
            </label>
            <input
              id="email"
              type="email"
              required
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              className="w-full rounded-md border border-console-border bg-console-surface px-3 py-2.5 text-sm text-console-text outline-none focus:border-signal-go"
              placeholder="you@company.com"
            />
          </div>
          <div>
            <label htmlFor="password" className="mb-1.5 block text-xs text-console-muted">
              Password
            </label>
            <input
              id="password"
              type="password"
              required
              minLength={8}
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              className="w-full rounded-md border border-console-border bg-console-surface px-3 py-2.5 text-sm text-console-text outline-none focus:border-signal-go"
              placeholder="At least 8 characters"
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
            className="w-full rounded-md bg-signal-go py-2.5 font-medium text-console-bg transition-opacity hover:opacity-90 disabled:opacity-50"
          >
            {submitting ? "Creating account…" : "Create organization"}
          </button>
        </form>

        <p className="mt-6 text-center text-sm text-console-muted">
          Already set up?{" "}
          <Link href="/login" className="text-signal-go hover:underline">
            Sign in instead
          </Link>
        </p>
      </div>
    </main>
  );
}
