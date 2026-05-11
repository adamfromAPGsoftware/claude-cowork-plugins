# Inspiration Compliance Checklist

Non-pacing gates derived from the inspiration analysis of 5 high-performing YouTube tutorials and the aggregated MG style guide. These complement the P1–P18 pacing rules in `long-form-pacing-rules.md`.

Loaded by step-04-storyboard alongside pacing rules. Each item is marked HARD (blocks progression) or SOFT (logged as warning).

---

## Transition Rules

| # | Rule | Gate | Source |
|---|------|------|--------|
| T1 | 95%+ of transitions are hard cuts — no dissolves, wipes, or slide transitions | HARD | Section 5 — all 5 creators use hard cuts exclusively |
| T2 | Jump cuts use 1.05–1.15x zoom alternation (even=base, odd=punched) | HARD | Section 5 — confirmed across 4/5 creators |
| T3 | Audio never breaks at visual transitions — voiceover bridges all cuts | HARD | Section 5 — #1 pacing rule across all 5 videos |
| T4 | Chapter cards use hard cut in/out — no fade transitions | HARD | Section 9 — confirmed across all 5 creators |

## Social Proof Rules

| # | Rule | Gate | Source |
|---|------|------|--------|
| S1 | Social proof uses branded Remotion templates (AgencyBrand, UpworkProfile, SocialProofStack) — NOT Hera MGs | HARD | Section 2 — social proof is constant branding, not generated graphics |
| S2 | Revenue/metric figures use exact numbers from the script — no approximations | SOFT | Section 2.1 Type A — e.g., "$453,745" not "~$450K" |
| S3 | Branded templates use `style="full-screen"` for credibility — never `lower-third` | HARD | Pattern 7 — lower-third renders too small for authority building |

## Motion Graphic Usage Rules

| # | Rule | Gate | Source |
|---|------|------|--------|
| M1 | No MGs during deep screen share execution segments | HARD | Section 2.3 — all 5 creators remove graphics during step-by-step tutorials |
| M2 | No MG within 2s of a previous MG ending | HARD | Section 2.3 — avoid visual overload |
| M3 | No MGs during emotional/personal speaker moments | SOFT | Section 2.3 — stay on full-frame speaker |
| M4 | Type A (text overlay) at every number/metric narration trigger | HARD | Section 2.2 — HIGH priority trigger |
| M5 | Type B (logo) at first mention of each tool/platform | SOFT | Section 2.2 — MEDIUM priority trigger |
| M6 | Type D (concept graphic) when speaker explains abstract concepts | SOFT | Section 2.2 — HIGH priority trigger |
| M7 | Body MG spacing within style guide targets for video category | SOFT | mg-style-guide.md — body MG spacing benchmarks |
| M8 | Intro MG entry animation types match style guide frequency distribution | SOFT | mg-style-guide.md — most common entry animations |
| M9 | Intro uses ≥3 distinct MG categories; no single type >40%; priority: UI-mockup ≥15%, text-overlay ≥12%, sequential-bullets ≥10% (P20) | SOFT | mg-style-guide.md — MG category frequency; P20 |
| M10 | Tool-referencing MGs (Types B, C, D) must use reference frame library as primary image source — no logo-only fallback for Type C | HARD | Short-form workflow pattern — library contains 21 tools with pre-uploaded Supabase URLs |
| M11 | If tool not in library: resolve via frame-extract or ask user to add screenshot — never skip reference image | HARD | resolve-reference-image.ts waterfall; user adds to `example-account-brand-plugin/context/brand/brand-assets/reference-frames/` |

## Caption Rules

| # | Rule | Gate | Source |
|---|------|------|--------|
| C1 | Captions cover 100% of spoken words in the intro | HARD | Section 6 — filling the gap all 5 creators leave |
| C2 | Caption position bottom-center, clear of PiP areas | HARD | Section 6 — `bottom: 8%`, `maxWidth: 60%` |
| C3 | Phrase-level bursts (2–4 words), not word-level | SOFT | Section 6 — matches instructional pacing |
| C4 | Font: Inter/Roboto, bold, 48px, white with text shadow | SOFT | Section 6 — readable on mobile |

## PiP Decision Rules

| # | Rule | Gate | Source |
|---|------|------|--------|
| P1 | Concept/agenda slides: PiP ON, 30–40% width. Position: right-center (60%), top-center (20%), bottom-left (15%), or other (5%). Default right-center. | SOFT | Section 3 — PiP positioning frequency distribution from 5 videos |
| P2 | Screen share execution: PiP OFF or small (≤16% width). Position: bottom-left (standard), bottom-right (when UI has left sidebar), or OFF (when full legibility needed). | SOFT | Section 3 — maximize UI legibility |
| P3 | Speaker section transitions: full-frame speaker, PiP OFF. No split-screen during verbal bridges. | SOFT | Section 3 — PiP Decision Rule |
| P4 | PiP position must not overlap caption text | HARD | Step-05 — if captions bottom-center, PiP bottom-right or top-right |
| P5 | Full-screen MG overlays (Type C UI mockups, Type D concept graphics): PiP OFF during the MG. Speaker returns when MG ends. | SOFT | Pattern from 5 videos — full-screen graphics never overlay PiP |

## Audio Continuity

| # | Rule | Gate | Source |
|---|------|------|--------|
| A1 | Single continuous audio track — no gaps at visual boundaries | HARD | Section 5 — audio bridges all cuts |
| A2 | If music used: ≤10–15% of voiceover volume, intro/transitions only | SOFT | Section 7 — 4/5 creators use zero music |
| A3 | No music during deep technical screen share content | HARD | Section 7 |

## Intro Structure

| # | Rule | Gate | Source |
|---|------|------|--------|
| I1 | Intro follows 4-beat arc: Hook → Authority/Value → Agenda → Transition | HARD | Section 1 — universal across all 5 videos |
| I2 | Hook within first 7s (P14) | HARD | Section 1 — hook timing 0:00–0:15 |
| I3 | Credibility stack within first 25s (P15) | SOFT | Section 1 — authority timing 0:05–0:30 |
| I4 | Intro duration 45s–90s before first title card (sweet spot) | SOFT | Section 1 — range is 36s–3:00 |
| I5 | Hook (first 7s) uses authority-first, FOMO-first, curiosity-first, or social-proof-first pattern — no CTA, no screen share, no generic greeting alone (P23) | HARD | Section 1 — all 5 creators establish authority/relevance immediately |
| I6 | At least 1 MG event in first 7s (text overlay, B-roll tease, or branded template) (P23) | HARD | Section 2 — visual support accompanies every hook |
| I7 | Zero CTAs in first 90s of video — no subscribe, like, link, or discount mentions in intro (P25) | HARD | CTA Patterns — 5/5 videos have zero intro CTAs |

## Color & Visual Treatment

| # | Rule | Gate | Source |
|---|------|------|--------|
| V1 | Chapter cards: black bg #000000, white text #FFFFFF | HARD | Section 9 — confirmed across all 5 creators |
| V2 | Slide/graphic backgrounds: dark mode dominant | SOFT | Section 8 — 4/5 use dark backgrounds |
| V3 | Text overlays: white sans-serif, 56–80px, with text shadow | SOFT | Section 9 — text overlay defaults |
