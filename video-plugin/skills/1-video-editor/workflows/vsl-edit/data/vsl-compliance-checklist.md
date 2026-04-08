# VSL Compliance Checklist

Non-pacing gates derived from production analysis of the VSL. These complement the V1–V12 pacing rules in `vsl-pacing-rules.md`.

Loaded alongside pacing rules when editing a VSL. Each item is marked HARD (blocks progression) or SOFT (logged as warning).

---

## Transition Rules

| # | Rule | Gate | Source |
|---|------|------|--------|
| T1 | 100% hard cuts — zero dissolves, fades, wipes, or slide transitions | HARD | Section 3 — entire video uses hard cuts exclusively |
| T2 | No jump-cut zoom alternation on speaker — speaker framing stays static, energy comes from cuts not camera movement | HARD | Section 5 — zoom effects absent on speaker |
| T3 | Audio never breaks at visual transitions — voiceover bridges all cuts | HARD | Section 3 — audio continuity confirmed across all transitions |
| T4 | Graphics enter and exit via hard cut — no fade-in/fade-out on full-screen graphics | HARD | Section 3 — all graphic transitions are instant |

## Speaker Rules

| # | Rule | Gate | Source |
|---|------|------|--------|
| SP1 | Medium close-up framing (chest up), direct eye contact with camera | HARD | Section 2 — consistent framing throughout |
| SP2 | Shallow depth of field — speaker sharp, background softly blurred | SOFT | Section 2 — background out of focus |
| SP3 | Natural, slightly warm skin tone grade — no cinematic colour grading on speaker | SOFT | Section 5 — natural colour treatment |
| SP4 | Practical branded light source in background (neon sign) visible in speaker shots | SOFT | Section 2 — neon sign provides branded ambient light |

## Subtitle & Text Rules

| # | Rule | Gate | Source |
|---|------|------|--------|
| ST1 | Phrase-level subtitles on ALL speaker segments — center-bottom, white sans-serif (Inter), medium weight | HARD | Section 4 — constant subtitles during speaker |
| ST2 | Key emphasis words highlighted in brand green (#72E032) — at least 1 green word per phrase burst | HARD | Section 4 — green highlight on critical words |
| ST3 | Emphasis text breakouts: large, bold text filling left or right side of screen beside speaker — used for thesis statements | HARD | Section 4 — breakout text at key moments |
| ST4 | B-roll text: massive, aggressive, all-caps typography overlaid on B-roll — mixed green/white, acts like a poster not a subtitle | HARD | Section 4 — B-roll text is screen-filling |
| ST5 | Text shadow on all subtitles: `textShadow: '0px 4px 10px rgba(0,0,0,0.5)'` for legibility over speaker | SOFT | Section 10 — Remotion implementation note |

## Colour Palette Rules

| # | Rule | Gate | Source |
|---|------|------|--------|
| CP1 | Dark background on all graphics: `#0A0A0A` to `#1A1A1A` | HARD | Section 5 — all graphics use dark backgrounds |
| CP2 | Primary accent: Neon Green `#72E032` — used for text highlights, positive elements, icons, UI active states | HARD | Section 5 — brand colour throughout |
| CP3 | Text: White `#FFFFFF` — all body text and subtitles | HARD | Section 5 — consistent text colour |
| CP4 | Negative accent: Red `#EF4444` — used exclusively for crossing things out, financial losses, pain data | HARD | Section 5 — red for negative concepts only |
| CP5 | No additional colours — the palette is strictly dark/white/green/red | SOFT | Section 5 — four-colour palette enforced |

## B-Roll Rules

| # | Rule | Gate | Source |
|---|------|------|--------|
| BR1 | All B-roll converted to black and white with high contrast: CSS `grayscale(100%) contrast(120%)` | HARD | Section 5 — B-roll is desaturated pain state |
| BR2 | B-roll used exclusively for pain/story segments — never for solution or offer | HARD | Section 7 — B-roll only in Hook/Agitate/Epiphany sections |
| BR3 | B-roll always has large text overlay — never plays without accompanying text | HARD | Section 4 — all B-roll segments have aggressive typography |
| BR4 | B-roll creates visual contrast with speaker: desaturated "past" vs colourful "present" | SOFT | Section 9 — key pattern #6 |

## Motion Graphic Rules

| # | Rule | Gate | Source |
|---|------|------|--------|
| MG1 | Icon pop-ups use spring animation: `spring({ damping: 12, stiffness: 100 })` scaling from 0→1 | HARD | Section 5 — pop-up icons use spring scale |
| MG2 | When a tool/brand is mentioned, its logo appears within 0.5s — always | HARD | Section 9 — key pattern #3 |
| MG3 | UI mockups are high-fidelity — realistic dashboard/calculator/website screenshots, not abstract graphics | HARD | Section 9 — key pattern #5 |
| MG4 | Graphics never hold static — subtle `scale(1→1.02)` or simulated UI interaction during hold | SOFT | Section 10 — subtle motion during holds |
| MG5 | The "gear" motif: green gear icon represents the custom solution — used as visual shorthand contrasting with scattered app logos | SOFT | Section 9 — key pattern #8 |
| MG6 | Abstract conceptual graphics (node webs, connection diagrams) use SVG stroke-draw animation with green accent | SOFT | Section 10 — Remotion SVG animation notes |

## Audio Rules

| # | Rule | Gate | Source |
|---|------|------|--------|
| A1 | Single continuous voiceover — no gaps at visual boundaries | HARD | Section 6 — VO is the spine |
| A2 | Background music present throughout at 10-15% of VO volume | SOFT | Section 6 — driving electronic/synth track |
| A3 | Optional SFX: subtle "pop" on icon spring animations, "whoosh" on B-roll transitions | SOFT | Section 6 — sound effects complement visual rhythm |
| A4 | Speaker pace: 160-180 WPM (fast, energetic, conversational) | SOFT | Section 6 — pace estimate |

## Architecture Rules

| # | Rule | Gate | Source |
|---|------|------|--------|
| AR1 | Single continuous `<OffthreadVideo>` passthrough for speaker — no per-segment decomposition | HARD | Section 10 — speaker video is never cut in Remotion |
| AR2 | Layer stack: `[Speaker Video] → [B-roll Overlays] → [Graphic Overlays] → [Text Overlays]` | HARD | Section 10 — z-index layering |
| AR3 | All overlays as `<Sequence>` components with frame-accurate timing | HARD | Section 10 — conditional rendering on frame |
| AR4 | Single `<Audio>` element for pre-mixed audio — no per-segment audio splitting | HARD | Section 10 — audio strategy |
| AR5 | Composition: 1920x1080, 30fps | SOFT | Section 10 — composition setup |
