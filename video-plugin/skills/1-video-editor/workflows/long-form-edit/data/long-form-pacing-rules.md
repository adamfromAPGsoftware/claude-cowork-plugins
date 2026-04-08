# Long-Form Pacing Rules (P1–P25)

Enforcement rules for long-form tutorial video pacing, derived from inspiration analysis of 5 high-performing YouTube tutorials (252K–3.3M views, 4 creators) and aggregated MG style guide data. Each rule includes explicit Gate, Measurement, and Remediation fields.

---

## P1: Hook Cut Density

- **Target:** 12–17.5 cuts/min in the first 15 seconds
- **Visual change every 2–4 seconds**
- Maximum visual energy — every second should have a change

**Gate:** FAIL — intro hook section with < 12 cuts/min
**Measurement:** Count layout changes in the first 15s, multiply by 4 to get cuts/min
**Remediation:** Add B-roll cuts, MG overlays, or zoom changes to increase cut density

**Section scope:** P1 applies to the **talking head intro** only — the full-frame speaker section before any screen share/agenda transition. If the intro includes a screen share/agenda walkthrough, that portion uses P3 rules instead.

## P2: Authority/Value Prop Pacing

- **Target:** 5–12 cuts/min during credibility stacking and value proposition
- **Visual change every 5–8 seconds**
- High energy maintained but slightly less frenetic than hook

**Gate:** FAIL — credibility/value section with < 5 cuts/min
**Measurement:** Count layout changes in credibility + value prop sections, divide by duration in minutes
**Remediation:** Add branded template segments, MG-A text overlays, or B-roll cuts

**Section scope:** P2 applies to talking head authority/credibility sections. These are part of the talking head intro (before screen share transition).

## P3: Agenda Walkthrough Pacing

- **Target:** 0–5 cuts/min during agenda previews and syllabus walkthroughs
- **Visual change every 10–30 seconds** (smooth movements instead of hard cuts)
- Allow content to breathe — smooth zoom/pan movements replace cuts

**Gate:** WARN — agenda section with > 5 cuts/min (over-edited for this section type)
**Measurement:** Count layout changes in agenda/preview sections, divide by duration in minutes
**Remediation:** Replace hard cuts with smooth zoom/pan movements (Type G MGs)

**Section scope:** P3 applies to screen share/agenda sections — the portion after the speaker transitions from full-frame talking head to slides, Excalidraw, or screen share. Use visual analysis frame classification as the primary signal for identifying this transition.

## P4: Body Screen Share Pacing

- **Target:** 0–2 cuts/min during screen share tutorial content
- **Layout changes every 30–90 seconds**
- Visual variety comes from PiP toggling, zoom, and caption changes — not hard cuts
- Screen share sections must have a visual change every 30–90s (chapter card, zoom, or PiP toggle)

**Gate:** WARN — body screen share section with > 30s static hold and zero overlays planned
**Measurement:** Measure longest gap between visual changes (chapter cards, zoom keyframes, PiP toggles) in body
**Remediation:** Add chapter cards at section boundaries, plan digital zoom keyframes, or add PiP toggle points

## P5: Max Speaker Hold

- **Maximum 15 seconds** of speaker-only footage before a visual break
- Break options: B-roll cut, motion graphic overlay, screen share, zoom change

**Gate:** FAIL — any speaker-only segment > 15s without a visual break
**Measurement:** Measure duration of each continuous speaker-only segment in the storyboard
**Remediation:** Insert MG overlay, B-roll cut, or zoom change within the segment

## P6: Max Screen Share Hold

- **Maximum 30 seconds** of screen share without a visual change
- Break options: Zoom into target area, pan to next section, return to speaker, PiP toggle
- During body screen share: PiP speaker should be visible 60–80% of the time

**Gate:** FAIL (intro) / WARN (body) — screen share hold > 30s without visual change
**Measurement:** Measure longest static screen share segment without zoom, PiP toggle, or speaker return
**Remediation:** Add digital zoom keyframes, PiP toggle points, or speaker return segments

## P7: Speaker Return Cadence

- **Return to full-frame speaker every 45s–2 min** during extended screen share sections
- 8–15s duration for each speaker return
- Maintains personal connection and prevents viewer fatigue

**Gate:** WARN (body) — screen share section > 2 min without speaker return
**Measurement:** Measure gaps between speaker return points during screen share sections
**Remediation:** Insert 8–15s speaker return segments at natural break points

## P8: Jump-Cut Zoom Factors

- **Base scale:** 1.0x
- **Punched-in scale:** 1.05–1.15x (observed range across 4/5 inspiration creators)
- **Alternation:** Even segments → base, odd segments → punched-in
- **Transform origin:** Always `center center`
- Jump cuts create energy in speaker-only sections without requiring B-roll

**Gate:** FAIL — speaker segments using zoom factors outside 1.05–1.15x range or not alternating
**Measurement:** Check each speaker segment's zoom factor and verify even/odd alternation pattern
**Remediation:** Adjust zoom factors to 1.05–1.15x range and ensure alternation on consecutive speaker segments

## P9: Title Card Duration

- **2–4 seconds** for chapter transition cards
- Black background (#000000), white text (#FFFFFF), centered
- Hard cut in and out (no fade transitions)

**Gate:** FAIL — chapter cards with fade/dissolve transitions or duration outside 2–4s
**Measurement:** Check each chapter card segment duration and transition type
**Remediation:** Set duration to 60–120 frames (2–4s at 30fps), use hard cut in/out

## P10: B-Roll Clip Duration

- **3–6 seconds** per B-roll insertion
- Longer holds (up to 15s) acceptable for screen recordings that require viewer comprehension

**Gate:** WARN — B-roll segments outside 3–6s range (unless screen recording)
**Measurement:** Check duration of each B-roll segment
**Remediation:** Trim or extend B-roll clips to 3–6s target range

## P11: Music Usage

- **4 of 5 inspiration creators use zero background music**
- Music is clearly optional and NOT expected for long-form tutorials
- If used: keep barely audible (~10–15% of voiceover volume), limit to intro/transition sections
- Never use music during deep technical screen share content

**Gate:** WARN — music present during body screen share sections
**Measurement:** Check audio track plan for music presence by section
**Remediation:** Remove music from body sections; keep only in intro/transitions if used at all

**Sourcing guidance:** If music is used, source from royalty-free libraries (Pixabay Music API, Uppbeat, Artlist). Download before Remotion scaffold step. Place in project `public/` as `background-music.mp3`. Volume: 8-12% of voiceover (`volume={0.08-0.12}` on the `<Audio>` element). Fade in over 2s at intro start, fade out over 2s before body transition.

## P12: MG Spacing (Intro)

- **Max gap:** 8s between consecutive MGs in the intro (target 6s)
- **Min gap:** 2s between consecutive MGs (avoid visual overload)
- Ensures consistent visual energy without clustering

**Gate:** FAIL — any intro MG gap > 8s OR any consecutive MG gap < 2s
**Measurement:** Calculate time from each MG end to next MG start across all intro MGs
**Remediation:** Redistribute MGs to maintain 2–8s spacing; add MGs in gaps > 8s, merge or shift MGs with gaps < 2s

## P13: Layout Change Frequency

- **Intro:** 3–9 layout changes per minute
- **Body:** 1–2 layout changes per minute
- A layout change is a switch between segment types (speaker → B-roll, speaker → screen share, etc.)

**Gate:** FAIL — intro with < 3 layout changes/min
**Measurement:** Count segment type transitions per section, divide by section duration in minutes
**Remediation:** Add visual break segments (B-roll, MG, branded template) to increase layout variety

## P14: Hook Timing

- **Core hook delivered ≤ 7s** from video start
- The attention-grabbing statement or problem framing must land within the first 7 seconds
- Visual support (text overlay, B-roll tease) should accompany the hook

**Gate:** FAIL — hook section duration > 7s before first major visual or verbal hook lands
**Measurement:** Check storyboard hook section end timestamp
**Remediation:** Tighten hook scripting; move the core hook statement earlier; trim pre-hook filler

## P15: Credibility Timing

- **Credibility stack completes ≤ 25s** from video start
- Authority signals (revenue numbers, social proof, credentials) must be established quickly
- Includes both spoken credibility and visual proof (branded templates, MG-A overlays)

**Gate:** WARN — credibility section ending > 25s from video start
**Measurement:** Check storyboard credibility section end timestamp
**Remediation:** Compress credibility delivery; combine visual and verbal proof; move branded templates earlier

## P16: MG Type Compliance

- **Type A** at every number/metric mention (revenue, stats, quantities)
- **Type B** at first mention of each tool/platform name
- **No MGs** during deep screen share execution segments
- Ensures motion graphics match their narration triggers

**Gate:** FAIL — any number/metric mention in intro without a Type A MG planned
**Measurement:** Cross-reference script narration triggers against MG type assignments in storyboard
**Remediation:** Add missing Type A overlays at number mentions; add Type B at first tool mentions; remove any MGs from deep screen share sections

## P17: Body Caption Frequency

- **Target:** 1 caption burst per 10–15 seconds of body speaker footage
- **Most body speaker segments should have `captionText: null`**
- Reserve captions for "power moments" — numbers/metrics, tool names on first mention, key takeaway phrases, emotional hooks
- A 60s body speaker section should have roughly 4–6 caption bursts total, NOT a caption on every segment

**Gate:** WARN — body section with > 1 caption burst per 8s of speaker footage (over-captioned)
**Measurement:** Count body speaker segments with non-null `captionText`, divide by total body speaker duration in seconds, multiply by 10
**Remediation:** Set `captionText: null` on lower-impact body speaker segments, keeping captions only at power moments

**Rationale:** Inspiration videos (5/5 analysed) show keyword captions at key moments only — not continuous subtitles. Over-captioning dilutes impact and creates visual noise. Viewers tune out captions that appear on every segment.

## P18: Body Visual Monotony Prevention

- **Target:** No body section >60s without a visual change (chapter card, MG overlay, speaker return, or zoom event)
- **Applies to:** Body (screen share and speaker return sections)
- **Visual change includes:** chapter cards, text overlay MGs (Type A), concept graphics (Type D), sequential bullet reveals (Type E), speaker return cuts, and digital zoom events

**Gate:** WARN — body section with >60s of purely static screen share (no visual change of any kind)
**Measurement:** Walk the body overlay plan (chapter cards + body MGs). Calculate the maximum gap between consecutive visual events. If any gap exceeds 60s, trigger WARN.
**Remediation:** Insert concept MGs (Type D/E) at narration trigger points within the sparse zone, or add a text overlay (Type A) at the next number/metric mention. Ensure added MGs comply with M1 (no MGs during deep screen share *execution* — concept explanation moments within screen share are fine).

**Category-specific guidance (from mg-style-guide.md):**
- **Shorter-form (10-30 min):** Higher body MG density expected — consult style guide for MGs/minute target
- **Course-length (1hr+):** Lower body MG density is acceptable — long tutorials have more uninterrupted screen share execution time

**Rationale:** MG analysis of 5 high-performing tutorials shows that even body sections have periodic visual variety through speaker returns, chapter cards, and concept graphics. Pure static screen share for >60s correlates with audience drop-off. This rule ensures minimum visual rhythm without over-editing the body.

## P19: Intro MG Density

- **Minimum MGs:** `min_mgs = ceil(intro_s / 9)` for shorter-form (10–30 min videos)
  - For a 60s intro: min 7 MGs (1 per ~8.6s)
  - For a 90s intro: min 10 MGs (1 per 9s)
- **Target MGs:** `target_mgs = ceil(intro_s / 7.5)`
  - For a 60s intro: target 8 MGs
  - For a 90s intro: target 12 MGs (matches inspiration avg of 11/video)
- **Course-length adjustment (videos >60min):** Use `min_mgs = ceil(intro_s / 15)` instead
  - For a 90s intro: min 6 MGs
- Inspiration benchmark: shorter-form intros average 11 MGs per 90s (1 per 8.2s), course-length average 5 per 90s (1 per 18s)

**Gate:** FAIL — intro with fewer MGs than `min_mgs`
**Measurement:** Count total MG events in intro, compare to formula using intro duration in seconds
**Remediation:** Add MG overlays at narration trigger points (numbers → Type A, tools → Type B, concepts → Type D). Prioritize the type distribution targets from P20.

## P20: Intro MG Type Distribution

- **Target distribution** (from style guide category ranking across 42 intro MG events):
  - UI-mockup (Type C): ≥15% of intro MGs (inspiration: 21%)
  - text-overlay (Type A): ≥12% of intro MGs (inspiration: 17%)
  - sequential-bullets (Type E): ≥10% of intro MGs (inspiration: 14%)
  - floating-card: ≥5% of intro MGs (inspiration: 10%)
  - concept-graphic (Type D): ≥5% of intro MGs (inspiration: 7%)
- **Minimum variety:** Intro must use ≥3 distinct MG categories
- **No single type dominance:** No single MG category may exceed 40% of all intro MGs

**Gate:** WARN — intro using <3 distinct MG categories OR any single type >40%
**Measurement:** Count MGs by category, compute percentage distribution, count distinct categories used
**Remediation:** Replace redundant MG types with under-represented categories. Ensure at least one UI-mockup, one text-overlay, and one sequential-bullets or concept-graphic in every intro.

## P21: Intro Layout Variation

- **Minimum distinct layouts in intro:** 3 (from: full-frame-speaker, full-screen-graphic, split-screen/PiP, screen-share, B-roll)
- **No three consecutive segments may share the same layout** — e.g., speaker → speaker → speaker is forbidden; must interleave with MG, B-roll, or screen share
- **Layout sequence guidance** (from inspiration):
  - Hook (0–7s): full-frame speaker OR speaker + text overlay
  - Credibility (7–25s): speaker + branded template, full-screen social proof, speaker + MG overlay — rapid switching
  - Agenda (25s+): screen share with PiP OR full-screen sequential bullets
  - Bridge: full-frame speaker (clean exit)

**Gate:** WARN — intro with <3 distinct layout types OR 3+ consecutive same-layout segments
**Measurement:** Walk the storyboard segment list, record layout type per segment, check for 3+ same-layout consecutive runs, count distinct types
**Remediation:** Insert MG overlays, B-roll cuts, or branded templates between consecutive speaker segments. Ensure at least one full-screen graphic and one split/PiP segment in the intro.

## P22: Body MG Density Targets

- **Shorter-form (10–30 min):**
  - **Minimum overall:** 1.0 MG/min of body duration
  - **Target overall:** 1.6–3.1 MGs/min
  - **Explanatory sections** (concept explanation, not screen share execution): target 4–8 MGs/min
  - **Screen share execution sections:** 0 MGs/min (M1 applies)
- **Course-length (1hr+):**
  - **Minimum overall:** 0.15 MG/min of body duration
  - **Target overall:** 0.19–0.55 MGs/min
  - **Explanatory sections:** target 1–3 MGs/min
  - **Screen share execution sections:** 0 MGs/min (M1 applies)
- **Bimodal distribution is expected:** Body MGs cluster at concept explanation and speaker return points, with near-zero MGs during tutorial screen share execution

**Gate:** WARN — body MG density below minimum for video category
**Measurement:** Count body MGs planned, divide by body duration in minutes, classify by video category
**Remediation:** Add concept MGs (Type D/E) at narration explanation points within the body. Add Type A overlays at number/metric mentions during speaker returns. Do NOT add MGs to screen share execution segments.

## P23: Hook Content Pattern

- **Hook MUST establish authority or relevance in the first 7s** using one of these proven patterns:
  1. **Authority-first:** Lead with a revenue number, credential, or measurable result ("I made $4M with this tool")
  2. **FOMO-first:** Lead with a trend or urgency statement ("You're getting left behind")
  3. **Curiosity-first:** Lead with an unexpected claim or question ("Did you know you could do this for free?")
  4. **Social-proof-first:** Lead with audience demand evidence ("Thousands of comments asked for this")
- **Hook MUST NOT contain:**
  - Any CTA (subscribe, like, click below) — CTAs come later (P25)
  - Product demo or screen share — hook is always speaker-on-camera or speaker + MG overlay
  - Generic greeting without a hook statement ("Hey guys, welcome back" alone is not a hook)
- **Visual support in hook is mandatory:** At least 1 MG event (Type A text overlay, B-roll tease, or branded template) must appear within the first 7s

**Gate:** FAIL — hook section with no authority/relevance statement in first 7s OR hook containing a CTA
**Measurement:** Review hook section script and storyboard segment for authority signal and absence of CTA
**Remediation:** Rewrite hook to lead with the strongest authority signal from the script. Move any CTA to post-credibility section. Add a visual MG to the first 7s if missing.

## P24: MG Duration Clustering

MG durations follow a U-shaped distribution. Use these duration bands when setting MG duration in the storyboard:

| Band | Duration | MG Types | Usage |
|------|----------|----------|-------|
| Ultra-short | 0.8–3s | logo-animation (B), text-overlay (A), floating-card | Quick visual accents, logo reveals, stat pops |
| Short | 3–8s | UI-mockup (C), concept-graphic (D), stylized-b-roll | Standard MG events, UI reveals, B-roll cuts |
| Medium | 8–15s | digital-pan-zoom (G), sequential-bullets (E, partial reveals) | Pan/zoom walkthroughs, multi-item reveals |
| Long | 15–30s | sequential-bullets (E, full list), comparison-layout, concept-graphic (D, complex) | Agenda walkthroughs, multi-step explanations |
| Extended | 30–65s | Only agenda walkthroughs (Type G + E combined) | Rare — only for syllabus walkthroughs |

- **Target distribution in intro:** ~30% ultra-short/short, ~50% short/medium, ~20% medium/long
- **Avoid the dead zone:** MGs of 4–6s are underrepresented in inspiration data — lean toward either 2–3s (punchy) or 8–12s (substantive)
- MG duration must be cross-referenced with the style guide's per-category avg duration (±50% tolerance)

**Gate:** WARN — MG with duration >30s that is NOT an agenda walkthrough, OR >50% of intro MGs in the same duration band
**Measurement:** Check each MG duration against its type's band, compute distribution across bands
**Remediation:** Adjust MG durations to match the target band for their type. Split extended MGs into sequential shorter segments if they exceed 30s.

## P25: CTA Placement

- **No CTA in the first 90 seconds** of the video — all 5 inspiration videos have zero intro CTAs
- **First permitted CTA:** After the intro-to-body transition (after the first chapter card / WhiteFlash)
- **CTA types permitted in body:** Mid-roll verbal mentions (subscribe, check link below) at natural section breaks only
- **CTA must never interrupt a tutorial flow** — place CTAs at chapter transitions, not mid-explanation
- **End CTA (if present):** Last 30s of video, after all tutorial content is delivered

**Gate:** HARD — any CTA (subscribe, like, link, discount code) appearing in the first 90s of the video
**Measurement:** Scan script and storyboard for CTA language in the intro section and first 90s
**Remediation:** Move all CTAs to body section breaks or end of video. Remove any CTA from the intro script.

---

## Section Identification Guidance

The pacing rules above are **section-aware** — different rules apply to different section types. Use these signals to identify sections:

**Talking head intro** (P1, P2 apply): Full-frame speaker on camera. Primary signal: visual analysis shows `speaker` frame type. Typically first 20–90s of the video.

**Screen share / agenda** (P3 applies): Speaker transitions to PiP on slides/Excalidraw/screen recording. Primary signal: visual analysis shows `screen-recording` or `slides` frame type. Transitional phrases in transcript: "let me show you", "let's jump into", "here's what we'll cover".

**Body** (P4 applies): Main tutorial content. Predominantly screen share with PiP speaker.

**Key boundary signal:** The most reliable intro boundary is the transition from full-frame talking head to screen share. This is detectable from the visual analysis frame classification. Do NOT inflate the "intro" by including screen share/agenda content — this leads to incorrect density targets.

---

## Pacing Validation Table

When validating a long-form storyboard, use this summary:

| Section | Min Events/Min | Max Events/Min | Max Hold (seconds) |
|---------|---------------|----------------|-------------------|
| Hook | 12 | 20 | 4 |
| Intro (credibility/value) | 5 | 15 | 8 |
| Agenda | 0 | 8 | 30 |
| Body | 0 | 8 | 30 (speaker) / 60 (screen share — P18) |
| CTA | 5 | 15 | 8 |

| Hook (content) | P23: authority/FOMO/curiosity/social-proof pattern, ≥1 MG, no CTA | — | — |

### Additional Validation Gates (P19–P25)

| Rule | Gate Level | Quick Check |
|------|-----------|-------------|
| P19 | FAIL | Intro MG count ≥ `ceil(intro_s / 9)` [shorter-form] or `ceil(intro_s / 15)` [course-length] |
| P20 | WARN | ≥3 distinct MG categories, none >40% |
| P21 | WARN | ≥3 distinct layouts, no 3+ consecutive same-layout |
| P22 | WARN | Body MGs ≥1.0/min [shorter-form] or ≥0.15/min [course-length] |
| P23 | FAIL | Authority/relevance hook in ≤7s, no CTA, ≥1 MG in first 7s |
| P24 | WARN | MG durations match type-specific bands, no >30s non-agenda MG |
| P25 | HARD | Zero CTAs in first 90s |

**PASS:** All sections within targets, all FAIL-level gates pass.
**WARN:** Any section within 2 of boundary, or any WARN-level gate triggered.
**FAIL:** Any section more than 2 outside boundary, max hold exceeded, or any FAIL-level gate triggered. Must remediate and re-validate before proceeding.
