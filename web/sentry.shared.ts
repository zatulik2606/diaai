/** GlitchTip init defaults for diaai-web (via @sentry/nextjs SDK) */
export const glitchTipTracesSampleRate = Number(
  process.env.GLITCHTIP_TRACES_SAMPLE_RATE ?? "0.01",
);

export const glitchTipEnvironment =
  process.env.GLITCHTIP_ENVIRONMENT ?? process.env.NODE_ENV;

export const glitchTipInitOptions = {
  tracesSampleRate: glitchTipTracesSampleRate,
  autoSessionTracking: false as const,
  sendDefaultPii: false,
};
