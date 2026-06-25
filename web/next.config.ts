import type { NextConfig } from "next";
import { withSentryConfig } from "@sentry/nextjs";

const nextConfig: NextConfig = {
  experimental: {
    optimizePackageImports: ["lucide-react", "recharts"],
  },
};

const hasGlitchTip =
  Boolean(process.env.GLITCHTIP_DSN) ||
  Boolean(process.env.NEXT_PUBLIC_GLITCHTIP_DSN);

export default hasGlitchTip
  ? withSentryConfig(nextConfig, {
      org: process.env.GLITCHTIP_ORG ?? "diaai",
      project: process.env.GLITCHTIP_PROJECT ?? "diaai-web",
      sentryUrl: process.env.GLITCHTIP_URL ?? "https://eu.glitchtip.com",
      tunnelRoute: "/monitoring",
      silent: !process.env.CI,
      disableLogger: true,
      sourcemaps: {
        disable: !process.env.GLITCHTIP_AUTH_TOKEN,
      },
      authToken: process.env.GLITCHTIP_AUTH_TOKEN,
    })
  : nextConfig;
