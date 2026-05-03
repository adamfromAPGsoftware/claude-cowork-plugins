/* global React, HookSlide, ContentSlide, CodeSlide, ScreenshotSlide, CTASlide */

const CAROUSEL_1 = [
  { type: "hook", props: {
    heroSrc: "hero-mac.svg",
    anchor: "top-left",
    tab: "5",
    head1: "Claude Code",
    accent: "skills",
    head2: "I can't live without",
    sub: "the exact prompts I use every week to ship faster…",
  }},
  { type: "content", props: {
    bg: "paper",
    badge: "skill · 01",
    ghost: "Brief",
    title: "Turn messy notes into a",
    accent: "brief",
    body: "I paste raw Slack threads, voice-memo transcripts, and half-baked ideas. Claude structures them into problem, audience, constraints, and success criteria.",
    mono: "~/notes/raw.md  →  /brief",
  }},
  { type: "code", props: {
    bg: "paper",
    eyebrow: "Send this to Claude",
    head1: "It writes the",
    serifAccent: "brief",
    head2: "for you",
    code: [
      { parts: [{ t: "You are my ", c: "#e8ddc8" }, { t: "chief of staff", c: "#d97757" }, { t: ".", c: "#e8ddc8" }] },
      "",
      { parts: [{ t: "Read the notes and return a one-page", c: "#e8ddc8" }] },
      { parts: [{ t: "brief", c: "#d97757" }, { t: " with: ", c: "#e8ddc8" }, { t: "problem, audience,", c: "#f4a387" }] },
      { parts: [{ t: "constraints, success, open questions", c: "#f4a387" }, { t: ".", c: "#e8ddc8" }] },
      "",
      { parts: [{ t: "Be ", c: "#e8ddc8" }, { t: "concise", c: "#d97757" }, { t: ". Ask ", c: "#e8ddc8" }, { t: "before", c: "#d97757" }, { t: " you invent.", c: "#e8ddc8" }] },
    ],
  }},
  { type: "content", props: {
    bg: "paper",
    badge: "skill · 02",
    ghost: "Kill it",
    title: "Run a",
    accent: "pre-mortem",
    body: "Before I ship anything risky, Claude plays the skeptical investor and tries to kill the idea. I keep what survives the beating.",
    mono: "role: skeptical-investor · mode: pre-mortem",
  }},
  { type: "content", props: {
    bg: "paper",
    badge: "skill · 03",
    ghost: "ADR",
    title: "Turn decisions into",
    accent: "docs",
    body: "After every working session, Claude reads the transcript and writes the ADR — what we decided, why, what we rejected. Gets committed to the repo.",
    mono: "docs/adr/2026-04-19-routing.md",
  }},
  { type: "code", props: {
    bg: "paper",
    eyebrow: "Send this to Claude",
    head1: "Then it",
    serifAccent: "reviews",
    head2: "every diff",
    code: [
      { parts: [{ t: "You are a ", c: "#e8ddc8" }, { t: "staff engineer", c: "#d97757" }, { t: ".", c: "#e8ddc8" }] },
      "",
      { parts: [{ t: "Review the ", c: "#e8ddc8" }, { t: "diff", c: "#d97757" }, { t: " against ", c: "#e8ddc8" }, { t: "CLAUDE.md", c: "#f4a387" }, { t: ".", c: "#e8ddc8" }] },
      "",
      { parts: [{ t: "Flag ", c: "#e8ddc8" }, { t: "naming drift, dead code,", c: "#f4a387" }] },
      { parts: [{ t: "missing tests, security smells", c: "#f4a387" }, { t: ".", c: "#e8ddc8" }] },
      "",
      { parts: [{ t: "Return a ", c: "#e8ddc8" }, { t: "severity table", c: "#d97757" }, { t: ".", c: "#e8ddc8" }] },
    ],
  }},
  { type: "content", props: {
    bg: "paper",
    badge: "skill · 04",
    ghost: "Outreach",
    title: "Draft the",
    accent: "outreach",
    body: "Cold emails, partner intros, investor updates. I feed Claude context + the ask. It drafts three tones — warm, direct, playful. I pick one.",
    mono: "tones: [warm, direct, playful]",
  }},
  { type: "screenshot", props: {
    bg: "paper",
    eyebrow: "skill · 05",
    title: "Then Claude ships the whole",
    accent: "feature",
    caption: "I describe it in plain English. Claude Code scaffolds the files, writes the tests, and opens the PR.",
    label: "CLAUDE CODE · PR #284",
  }},
  { type: "cta", props: {
    bg: "paper",
    eyebrow: "your turn",
    head1: "Want these",
    serifAccent: "prompts?",
    ghost: "Yours",
    sub: "Comment CLAUDE and I'll send the full pack — prompts, templates, and the CLAUDE.md I actually use.",
    cta: "comment 'CLAUDE'",
  }},
];

const CAROUSEL_2 = [
  { type: "hook", props: {
    heroSrc: "hero-crt.svg",
    anchor: "bottom-right",
    tab: "NEW",
    head1: "Claude just",
    accent: "replaced",
    head2: "my designer",
    sub: "not the craft — the bottleneck…",
  }},
  { type: "content", props: {
    bg: "dark",
    badge: "the problem",
    ghost: "Queue",
    title: "Every idea waited in a",
    accent: "queue",
    body: "Mock → review → revise → build. By the time it shipped, the market had moved on. For years this was just… the job.",
    mono: "avg. cycle: 11 days",
  }},
  { type: "content", props: {
    bg: "dark",
    badge: "the shift",
    ghost: "Now",
    title: "Now I mock in",
    accent: "minutes",
    body: "I describe the screen, paste our design system, and Claude produces a real HTML prototype. Not a Figma file — a thing I can click.",
    mono: "input: brief.md + design-system/",
  }},
  { type: "code", props: {
    eyebrow: "Send this to Claude",
    head1: "How I brief",
    serifAccent: "Claude",
    code: [
      { parts: [{ t: "Build the ", c: "#e8ddc8" }, { t: "settings page", c: "#d97757" }, { t: ".", c: "#e8ddc8" }] },
      "",
      { parts: [{ t: "Use the ", c: "#e8ddc8" }, { t: "brand system", c: "#f4a387" }, { t: " in ", c: "#e8ddc8" }, { t: "/brand/", c: "#d97757" }, { t: ".", c: "#e8ddc8" }] },
      { parts: [{ t: "Inter for type, ", c: "#e8ddc8" }, { t: "orange accent", c: "#d97757" }, { t: " word per", c: "#e8ddc8" }] },
      { parts: [{ t: "section. Blocky underline. No emoji.", c: "#e8ddc8" }] },
      "",
      { parts: [{ t: "Give me ", c: "#e8ddc8" }, { t: "three variants", c: "#d97757" }, { t: " as tweaks.", c: "#e8ddc8" }] },
    ],
  }},
  { type: "screenshot", props: {
    bg: "dark",
    eyebrow: "the output",
    title: "Three variants. One",
    accent: "prompt.",
    caption: "Claude returns the full page — responsive, on-brand, and tweakable. I pick the direction in 60 seconds instead of 3 days.",
    label: "VARIANT GRID",
  }},
  { type: "content", props: {
    bg: "dark",
    badge: "the shift · 02",
    ghost: "Director",
    title: "Designers become",
    accent: "directors",
    body: "The work isn't gone. It shifted. The taste, the system, the judgment — that's the job now. The pixel-pushing got automated.",
    mono: "role: designer  →  design director",
  }},
  { type: "content", props: {
    bg: "dark",
    badge: "the moat",
    ghost: "System",
    title: "The moat is your",
    accent: "system",
    body: "Claude is only as good as the brand you feed it. A tight design system + a clear voice beats a thousand one-shot prompts.",
    mono: "brand/ + CLAUDE.md = unfair advantage",
  }},
  { type: "content", props: {
    bg: "dark",
    badge: "what i still hire for",
    ghost: "Taste",
    title: "The",
    serifAccent: "5%",
    head2: "that sets the ceiling",
    body: "Original art direction. Brand identity from zero. Motion craft. Claude hits the ceiling — it doesn't raise it. That's still a human job.",
    mono: "hire: taste · system · direction",
  }},
  { type: "cta", props: {
    bg: "dark",
    eyebrow: "get the stack",
    head1: "Steal my",
    serifAccent: "setup",
    sub: "The design system, the CLAUDE.md, and the three prompts I use every day. Free.",
    cta: "comment 'STACK'",
  }},
];

function renderSlide(slide, i, total) {
  const props = { ...slide.props, index: i + 1, total };
  switch (slide.type) {
    case "hook": return <HookSlide {...props}/>;
    case "content": return <ContentSlide {...props}/>;
    case "code": return <CodeSlide {...props}/>;
    case "screenshot": return <ScreenshotSlide {...props}/>;
    case "cta": return <CTASlide {...props}/>;
    default: return null;
  }
}

window.CAROUSEL_1 = CAROUSEL_1;
window.CAROUSEL_2 = CAROUSEL_2;
window.renderSlide = renderSlide;
