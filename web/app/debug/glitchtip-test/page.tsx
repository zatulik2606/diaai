import { notFound } from "next/navigation";

import { GlitchTipTestClient } from "./glitchtip-test-client";

export const dynamic = "force-dynamic";

export default function GlitchTipTestPage() {
  if (!process.env.GLITCHTIP_DEBUG_TOKEN) {
    notFound();
  }

  return <GlitchTipTestClient />;
}
