"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import { useAuth } from "@/lib/auth";

const LINKS = [{ href: "/dashboard", label: "Jobs" }];

export default function ConsoleNav() {
  const pathname = usePathname();
  const { user, logout } = useAuth();

  return (
    <header className="border-b border-console-border bg-console-bg/95 backdrop-blur">
      <div className="mx-auto flex max-w-6xl items-center justify-between px-6 py-4">
        <div className="flex items-center gap-8">
          <Link href="/dashboard" className="flex items-center gap-2 font-display text-lg font-semibold text-console-text">
            <span className="h-2 w-2 rounded-full bg-signal-go" />
            Hirely
            <span className="font-mono text-[10px] uppercase tracking-widest text-console-faint">
              console
            </span>
          </Link>
          <nav className="flex items-center gap-6">
            {LINKS.map((link) => (
              <Link
                key={link.href}
                href={link.href}
                className={`text-sm transition-colors ${
                  pathname?.startsWith(link.href)
                    ? "text-console-text"
                    : "text-console-muted hover:text-console-text"
                }`}
              >
                {link.label}
              </Link>
            ))}
          </nav>
        </div>
        <div className="flex items-center gap-4">
          {user && (
            <span className="hidden font-mono text-xs text-console-muted sm:inline">
              {user.name} · {user.role}
            </span>
          )}
          <button
            onClick={logout}
            className="rounded-md border border-console-border px-3 py-1.5 text-xs text-console-muted transition-colors hover:border-console-borderLight hover:text-console-text"
          >
            Sign out
          </button>
        </div>
      </div>
    </header>
  );
}
