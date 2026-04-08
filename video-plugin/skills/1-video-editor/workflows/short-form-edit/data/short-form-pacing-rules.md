# Short-Form Pacing Rules

## Overview

These rules enforce the fast-paced visual rhythm required for Instagram Reels, TikTok, and YouTube Shorts. Short-form content competes with infinite scroll — every second must earn the viewer's attention.

---

## Pacing Rules

| # | Rule | Value | Rationale |
|---|------|-------|-----------|
| P1 | Max same-shot duration | 3 seconds (90 frames @ 30fps) | Competitor avg scene duration 1.5–2.1s — 3s is generous ceiling |
| P2 | Visual change frequency | Every 2–4 seconds | Retain mobile-scroll audience |
| P3 | Min MG coverage | 75–80% of total duration (Punchy/Standard: 75%, Deep: 80%) | Competitor avg 85–95% density — 75% is minimum floor; target 85–90% |
| P4 | Hook = V5 split-screen | V5 (1-2s) then snap to V1/V4/V5 ping-pong | Split-screen hook with recognizable visual — stop the scroll |
| P5 | Layout rotation | Min 3 different segment patterns per video | Engagement variety |
| P6 | No chapter cards | Forbidden | Too slow for short-form |
| P7 | Max branded template | 3 seconds (90 frames @ 30fps) | Brief authority flash |
| P8 | Caption style | **Platform-native** — YouTube SRT via API, Instagram/TikTok auto-captions toggled per post. Zero burned-in text overlays in Remotion. | Multilingual translation support, cleanest visual aesthetic, platform handles styling |
| P9 | Caption safe zone | Platform-handled | Auto-captions respect platform UI zones natively |
| P10 | Min cut density | At least 8 visual changes per 15 seconds | Competitor avg 0.5–0.7 cuts/sec = 7.5–10.5 cuts per 15s |
| P11 | MG content specificity | MG cutaways must be contextual to spoken content | Generic MGs feel disconnected — cutaways must reinforce the message |

---

## Enforcement

These rules are checked during storyboard generation (step 03) and QA (step 05). Any violation blocks progression.

### P1 — Max Same-Shot Duration

Every segment in the storyboard must have `durationInFrames ≤ 90` (at 30fps = 3 seconds max). If a speaker segment exceeds this, split it by inserting an MG cut. Competitor average scene duration is 1.5–2.1s — aim for 2–3s segments, never exceed 3s.

### P2 — Visual Change Frequency

Count the total number of segment boundaries. For a 30s video at 30fps (900 frames), there must be at least `900 / 120 = 7.5` → **8 visual changes minimum**.

### P3 — Min MG Coverage

Sum the `durationInFrames` of all non-speaker segments (V4, V4b, V5, V6). This sum must meet the minimum for the duration category:
- Punchy (15–20s): ≥ 75% of `PROJECT.totalDurationInFrames`
- Standard (30–45s): ≥ 75% of `PROJECT.totalDurationInFrames`
- Deep (50–60s): ≥ 80% of `PROJECT.totalDurationInFrames`

**Aspirational target:** Competitor reels average 85–95% MG density. 75% is the minimum floor — target 85–90%.

**MG cutaway sub-rule:** At least 1 MG cutaway (V4b) per 10–12 seconds. For a 30s video, minimum 2 MG cutaways. MG cutaways = 2–3 seconds (60–90 frames at 30fps).

**Design principle:** The speaker's voice plays continuously under all visual types. MG segments don't interrupt the script — they replace the visual while audio continues. Think of it as "MG with occasional speaker moments" rather than "speaker with occasional MG."

### P4 — Hook Visual Change

The first segment must be a **V5 split-screen (50/50)** (1-2 seconds, 30-60 frames) with a recognizable visual in the top half and speaker face in the bottom half. Acceptable hook patterns:

**Primary (4/5 videos):** V5 (split-screen, 1-2s) → V1 (speaker, 1s) → V5/V4 (ping-pong alternating)
**Secondary:** V5 (split-screen, 2s) → V4 (full-screen MG)
**Tertiary (acceptable but NOT primary):** V2 (speaker-zoom, 1-2s) → V4/V5

**FORBIDDEN:** V6 (hook text) as the opening segment. Top-performing shorts open with visual context + speaker face, not text cards.

### P4a — Hero Keyword Visual

The opening V5 split-screen top half MUST show the video's **hero keyword visual** — the most recognizable image related to the primary subject. This is the single visual that tells viewers "this video is about X" within the first 1-2 seconds.

**Hero keyword identification:**
- The hero keyword is the dominant tool, platform, or concept from the script's hook section
- Example: script about "Claude Code" → hero keyword = Claude; script about "VS Code extensions" → hero keyword = VS Code

**Hero keyword → visual type mapping:**
| Hero Keyword Type | Visual Asset | Source |
|-------------------|-------------|--------|
| Tool / platform | Tool logo MG | `fetch-logo.ts` waterfall → Hera MG |
| Code / dev topic | IDE or terminal MG | Hera prompt-only |
| AI tool | Tool logo OR chat interface MG | `fetch-logo.ts` → Hera MG |
| Comparison | Side-by-side logos | `fetch-logo.ts` for each → canvas composite → Hera MG |

**FORBIDDEN:** Text-only MGs (animated text, counters, abstract text graphics) as the opening segment's top-half visual. The hook must show a recognizable, concrete visual — never text.

### P5 — Layout Rotation

Count the distinct segment pattern types (V1–V7) used across the video. Must be ≥ 3.

### P6 — No Chapter Cards

The storyboard must not contain any `chapter-card` visual type. Short-form has no chapters.

### P7 — Max Branded Template

Any segment using `SocialProofStack`, `UpworkProfile`, or `AgencyBrand` must have `durationInFrames ≤ 90`.

### P8 — Caption Style (Platform-Native)

**Zero burned-in captions in Remotion.** All caption delivery is platform-native:
- **YouTube:** SRT file generated from `clipped-refined-transcript.json`, uploaded via YouTube API
- **Instagram Reels / TikTok:** Platform auto-captions toggled on per post (manually in the app)

This gives multilingual translation support (platform auto-translate), the cleanest visual aesthetic, and lets each platform style captions to match its current UI conventions.

### P9 — Caption Safe Zone

Platform-handled. Auto-captions on YouTube, Instagram, and TikTok respect their own UI zones natively. No Remotion-level safe zone enforcement needed.

### P10 — Min Cut Density

Count the total number of visual changes (segment boundaries) in any 15-second window. Must be at least 8. For a 30s video, that means at least 16 total cuts — averaging ~1.9s per segment. Competitor average is 0.5–0.7 cuts/sec.

If a section has fewer than 8 cuts per 15s, insert additional MG cutaways (V4b, 45-75 frames) to increase density.

### P11 — MG Content Specificity

Every MG cutaway (V4 or V4b) must be contextually relevant to the spoken content at that moment. Selection rules:
- Tool or platform mentioned → tool logo MG (e.g., Claude logo, VS Code icon)
- Build/creation action described → typing/coding animation
- Statistic or number cited → animated counter or data visualisation
- Comparison being made → side-by-side or before/after graphic
- Default (no specific context) → abstract tech/data flow

**Central library reference images satisfy contextual specificity** — Tier C MGs use curated tool interface screenshots from the central library as Hera reference images, ensuring the generated animation matches the actual tool being discussed.

**Forbidden:** Generic landscape stock footage, unrelated abstract art, or static screenshots used as MG cutaways.

**Note:** For the FIRST MG segment (hook), see P4a for the mandatory hero keyword visual requirement. The hook MG is pre-assigned during storyboard step C2 — P11 governs all subsequent MG cutaways.
