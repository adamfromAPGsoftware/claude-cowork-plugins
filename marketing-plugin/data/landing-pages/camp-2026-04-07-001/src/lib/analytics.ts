/**
 * GA4 event tracking helper.
 *
 * Wraps gtag() with a typed API, safe no-ops if gtag isn't loaded
 * (SSR, ad-blockers, dev mode), and a single place to add/remove params.
 *
 * Event taxonomy (see docs/analytics-events.md):
 *   cta_click        - any CTA button click          { cta_location }
 *   quiz_open        - qualification modal opens     { cta_location }
 *   quiz_answer      - per-question answer           { quiz_step, question, answer }
 *   quiz_complete    - all 5 questions answered      { qualified }
 *   generate_lead    - qualified lead (key event)    { saas_spend, team_size, revenue_band }
 *   quiz_abandon     - modal closed mid-quiz         { quiz_step }
 *   booking_complete - GHL booking confirmed         {}
 *   scroll_depth     - 25/50/75/100% of page         { percent }
 */

declare global {
  interface Window {
    gtag?: (...args: unknown[]) => void;
    dataLayer?: unknown[];
  }
}

export type CtaLocation =
  | "hero"
  | "header"
  | "nav"
  | "mid_page"
  | "footer"
  | "sticky"
  | "exit_intent"
  | "roi_calculator"
  | "value_prop"
  | "other";

type EventParams = Record<string, string | number | boolean | undefined>;

function send(eventName: string, params: EventParams = {}): void {
  if (typeof window === "undefined") return;
  // Strip undefined so GA4 doesn't record empty params
  const clean: EventParams = {};
  for (const [k, v] of Object.entries(params)) {
    if (v !== undefined && v !== null && v !== "") clean[k] = v;
  }
  if (typeof window.gtag === "function") {
    window.gtag("event", eventName, clean);
  }
  // Dev visibility
  if (import.meta.env?.DEV) {
    // eslint-disable-next-line no-console
    console.debug("[ga4]", eventName, clean);
  }
}

// ---- Public API ------------------------------------------------------------

export const track = {
  ctaClick(location: CtaLocation, label?: string) {
    send("cta_click", { cta_location: location, cta_label: label });
  },

  quizOpen(location: CtaLocation) {
    send("quiz_open", { cta_location: location });
  },

  quizAnswer(step: number, question: string, answer: string) {
    send("quiz_answer", { quiz_step: step, question, answer });
  },

  quizComplete(qualified: boolean) {
    send("quiz_complete", { qualified });
  },

  quizAbandon(step: number) {
    send("quiz_abandon", { quiz_step: step });
  },

  generateLead(params: {
    saas_spend?: string;
    team_size?: string;
    revenue_band?: string;
    qualified: boolean;
  }) {
    send("generate_lead", params);
  },

  bookingComplete() {
    send("booking_complete", {});
  },

  scrollDepth(percent: 25 | 50 | 75 | 100) {
    send("scroll_depth", { percent });
  },
};

// ---- Scroll depth tracker --------------------------------------------------

let scrollDepthInstalled = false;
export function installScrollDepthTracker(): () => void {
  if (typeof window === "undefined" || scrollDepthInstalled) return () => {};
  scrollDepthInstalled = true;

  const thresholds: Array<25 | 50 | 75 | 100> = [25, 50, 75, 100];
  const fired = new Set<number>();

  const onScroll = () => {
    const doc = document.documentElement;
    const scrollTop = window.scrollY || doc.scrollTop;
    const height = doc.scrollHeight - doc.clientHeight;
    if (height <= 0) return;
    const pct = Math.round((scrollTop / height) * 100);
    for (const t of thresholds) {
      if (pct >= t && !fired.has(t)) {
        fired.add(t);
        track.scrollDepth(t);
      }
    }
  };

  window.addEventListener("scroll", onScroll, { passive: true });
  return () => {
    window.removeEventListener("scroll", onScroll);
    scrollDepthInstalled = false;
  };
}
