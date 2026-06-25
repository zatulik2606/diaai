import * as Sentry from "@sentry/nextjs";

import { glitchTipInitOptions, glitchTipEnvironment } from "./sentry.shared";

Sentry.init({
  dsn: process.env.NEXT_PUBLIC_GLITCHTIP_DSN,
  environment: glitchTipEnvironment,
  ...glitchTipInitOptions,
});

export const onRouterTransitionStart = Sentry.captureRouterTransitionStart;
