"use client";

import { useEffect } from "react";
import { useRouter } from "next/navigation";
import { useAuth } from "@/lib/auth";
import ConsoleNav from "@/components/ConsoleNav";

export default function DashboardLayout({ children }: { children: React.ReactNode }) {
  const { user, loading } = useAuth();
  const router = useRouter();

  useEffect(() => {
    if (!loading && !user) router.replace("/login");
  }, [loading, user, router]);

  if (loading || !user) {
    return (
      <div className="flex min-h-screen items-center justify-center bg-console-bg">
        <p className="font-mono text-xs uppercase tracking-widest text-console-faint">
          Loading console…
        </p>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-console-bg">
      <ConsoleNav />
      <div className="mx-auto max-w-6xl px-6 py-10">{children}</div>
    </div>
  );
}
