import type { Config } from "tailwindcss";

const config: Config = {
  content: ["./app/**/*.{ts,tsx}", "./components/**/*.{ts,tsx}"],
  theme: {
    extend: {
      colors: {
        // Console — the recruiter/ops side. Deep graphite, not pure black.
        console: {
          bg: "#12141A",
          surface: "#181B23",
          raised: "#1F2330",
          border: "#2A2E3C",
          borderLight: "#363B4C",
          text: "#E7E9EE",
          muted: "#9298A8",
          faint: "#5B6072",
        },
        // Careers — the candidate side. Warm paper, human.
        paper: {
          bg: "#F7F4EE",
          surface: "#FFFFFF",
          border: "#E4DFD3",
          text: "#1B1E27",
          muted: "#6B6659",
        },
        // Shared signal accents (pipeline states)
        signal: {
          go: "#5EEAD4", // advancing / open / hired
          pending: "#F0B429", // awaiting review / in progress
          hold: "#8B93A8", // draft / not started
          stop: "#F87171", // rejected / closed
        },
      },
      fontFamily: {
        display: ["var(--font-display)"],
        body: ["var(--font-body)"],
        mono: ["var(--font-mono)"],
      },
      backgroundImage: {
        "trace-grid":
          "linear-gradient(rgba(255,255,255,0.035) 1px, transparent 1px), linear-gradient(90deg, rgba(255,255,255,0.035) 1px, transparent 1px)",
      },
      backgroundSize: {
        trace: "28px 28px",
      },
    },
  },
  plugins: [],
};
export default config;
