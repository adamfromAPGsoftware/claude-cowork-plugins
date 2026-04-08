---
generatedDate: '2026-03-27'
videosAnalyzed: 5
category: long-form
totalIntroMGEvents: 42
totalBodySampleMGEvents: 54
totalIntroTransitions: 19
totalBodyTransitions: 88
---

# Long-Form Motion Graphics Style Guide

> **Source:** 5 high-performing YouTube tutorials across 5 creators
> **Analysis date:** 2026-03-27
> **Method:** Three-pass Gemini 3.1 Pro analysis (intro MG @ 1fps, body samples @ 0.5fps, density @ 0.1fps)

## Creator Breakdown

| Creator | Videos | Intro MG Events | Body MG Events | Avg Body MG Spacing |
|---------|--------|-----------------|----------------|---------------------|
| Futurepedia | 1 | 11 | 15 | N/A |
| Kevin Stratvert | 1 | 11 | 28 | N/A |
| Nate Herk | 1 | 9 | 4 | N/A |
| Nick Saraev | 1 | 1 | 2 | N/A |
| Varun Mayya | 1 | 10 | 5 | N/A |

## Video Category Profiles

### Shorter-Form (10-30 min)

- **Videos:** 3
- **Total Intro MG Events:** 32 (avg 11/video)
- **Total Body MG Events (sampled):** 48 (avg 16/video)

### Course-Length (1hr+)

- **Videos:** 2
- **Total Intro MG Events:** 10 (avg 5/video)
- **Total Body MG Events (sampled):** 6 (avg 3/video)

## Most Common MG Categories (Intro)

| Rank | Category | Count | Avg Duration |
|------|----------|-------|-------------|
| 1 | UI-mockup | 9 | 9.4s |
| 2 | text-overlay | 7 | 2.7s |
| 3 | sequential-bullets | 6 | 22.1s |
| 4 | floating-card | 4 | 3.7s |
| 5 | concept-graphic | 3 | 18.2s |
| 6 | digital-pan-zoom | 3 | 11.2s |
| 7 | logo-animation | 3 | 3.8s |
| 8 | stylized-b-roll | 2 | 4.8s |
| 9 | diagram | 2 | 3.5s |
| 10 | comparison-layout | 2 | 18.5s |
| 11 | shape-animation | 1 | 7.5s |

## Most Common MG Categories (Body)

> **Note:** Body MG categories below are manually curated from cross-video analysis (the automated Gemini Pass B returned `null` categories). These are derived from the body sample analysis markdown files across all 5 videos.

| Rank | Category | Typical Duration | Frequency | Context |
|------|----------|-----------------|-----------|---------|
| 1 | sequential-bullets | 20–30s | Common | Agenda/list walkthroughs, component definitions, feature lists |
| 2 | text-overlay | 8–13s | Common | Annotations, call-outs on screen share, keyword emphasis |
| 3 | concept-graphic / diagram | 20–27s | Common | System architecture, workflow visualization, abstract concepts |
| 4 | floating-card / title-card | 3–4s | Moderate | Chapter transitions, section breaks |
| 5 | screen-share-annotation | 13–15s | Moderate | Arrow overlays, text callouts on UI during tutorials |

**Total body MG events (sampled):** 54 across 5 videos

## Most Common Entry Animations (Intro — 42 events)

| Entry Animation | Count | % |
|-----------------|-------|---|
| cut-in | 17 | 40% |
| pop-in | 13 | 31% |
| fade-in | 4 | 10% |
| slide-in-left | 3 | 7% |
| slide-in-bottom | 2 | 5% |
| scale-up | 2 | 5% |
| slide-in-right | 1 | 2% |

## Most Common Entry Animations (Body — estimated from cross-video analysis)

| Entry Animation | Estimated % |
|-----------------|-------------|
| cut-in | ~50% |
| pop-in | ~35% |
| fade-in | ~10% |
| other (slide, scale) | ~5% |

## Most Common Exit Animations (Intro — 42 events)

| Exit Animation | Count | % |
|----------------|-------|---|
| cut-out | 31 | 74% |
| fade-out | 6 | 14% |
| hold-then-cut | 5 | 12% |

## Most Common Exit Animations (Body — estimated from cross-video analysis)

| Exit Animation | Estimated % |
|----------------|-------------|
| cut-out | ~74% |
| fade-out | ~15% |
| hold-then-cut | ~11% |

## Transition Types (Intro)

| Type | Count |
|------|-------|
| cut | 19 |

## Transition Types (Body)

| Type | Count |
|------|-------|
| Cut | 56 |
| Hard Cut | 26 |
| hard cut | 3 |
| cut | 2 |
| Slide | 1 |

## Body MG Density Targets

| Category | MGs/minute (overall) | Peak MGs/minute (explanatory sections) | Screen Share Execution |
|----------|---------------------|---------------------------------------|----------------------|
| Shorter-form (10–30 min) | 1.6–3.1 | 6–10 | 0 (M1 applies) |
| Course-length (1hr+) | 0.19–0.55 | 1–3 | 0 (M1 applies) |

> **Bimodal distribution:** Body MGs cluster at concept explanation and speaker return points, with near-zero MGs during tutorial screen share execution. Shorter-form videos (Futurepedia, Kevin, Varun) maintain 1.6–3.1 MGs/min overall. Course-length videos (Nate, Nick) drop to 0.19–0.55 MGs/min due to extended screen share tutorials.

## Color Palette (Aggregated)

> **Note:** Manually curated from the 5 inspiration video analyses. The automated Gemini analysis did not populate color palette fields.

### Background Colors

| Hex | Usage | Creators |
|-----|-------|----------|
| `#0F172A` | Dark navy (Tailwind slate-900) | Futurepedia (x3) |
| `#121212` | Near-black | Nick Saraev (x2) |
| `#1E1E1E` | VS Code dark / dark studio | Kevin Stratvert (x2), Varun Mayya |
| `#111827` | Tailwind gray-900 | Nate Herk |
| `#000000` | Chapter cards (universal) | All 5 creators |
| `#FFFFFF` | White slides / light panels | Kevin Stratvert, Nate Herk |
| `#F5F5F5` | Light gray panel background | Kevin Stratvert |

### Text Colors

| Hex | Usage | Creators |
|-----|-------|----------|
| `#FFFFFF` | Primary text (universal) | All 5 creators |

### Accent Colors

| Hex | Usage | Creators |
|-----|-------|----------|
| `#3B82F6` | Tailwind blue-500 (links, highlights) | Futurepedia, Varun Mayya, Nate Herk |
| `#4A90E2` | Code accent blue / marker | Nick Saraev, Kevin Stratvert |
| `#EF4444` | Red emphasis / alerts | Futurepedia, Nate Herk |
| `#FF6B6B` / `#FF6D5A` | n8n brand pink/coral | Kevin Stratvert, Varun Mayya |
| `#D9534F` | Muted red / definition highlight | Futurepedia |
| `#C67B3B` | Warm orange | Futurepedia |
| `#82B1FF` | Banner blue | Kevin Stratvert |
| `#8B5CF6` | Purple accent | Nate Herk |
| `#06B6D4` | Cyan accent | Futurepedia |

## Hook Patterns (First 15 Seconds)

| Creator | Hook Strategy | Elements |
|---------|--------------|----------|
| Nate Herk | Establishes a 'zero-to-hero' framework immediately. Uses high-contrast revenue proof to build instant authority and bypa... | Clear transformation timeline (Beginner to AI Agents).; Objection handling (No coding experience needed).; High-value social proof ($500k revenue screenshots). |
| Nick Saraev | Direct authority establishment. Speaker states revenue ($4M) and student count (2000+) to build instant credibility. No ... | Direct eye contact; High-value claims ($4M profit); Clear target audience (beginners to pros) |
| Futurepedia | Uses authority and FOMO to grab attention, followed by a promise of simplicity. | News article proof.; Relatable FOMO B-roll.; Complex UI contrasted with a reassuring statement. |
| Varun Mayya | Uses social proof via user comments to establish demand. References past successful videos to build credibility before i... | YouTube search UI mockup; Animated comment/DM popups; Archival B-roll footage |
| Kevin Stratvert | Uses a relatable hypothetical scenario (donut shop) to ground a complex technical concept (AI agents). Visualizes the bu... | Direct question to viewer.; Fictional business B-roll.; Clear problem statement (unpaid invoices). |

## CTA Patterns

### Nate Herk — Build & Sell n8n AI Agents (8+ Hour Course, No Code)
- **Intro CTA:** No CTA in intro — CTA appears later in video.
- **Mid-roll (09:15):**  — 
- **Mid-roll (12:56):**  — 
- **Mid-roll (34:40):**  — 
- **Mid-roll (42:28):**  — 
- **Mid-roll (48:40):**  — 

### Nick Saraev — CLAUDE CODE FULL COURSE 4 HOURS: Build & Sell (2026)
- **Intro CTA:** No CTA in intro — CTA appears later in video.

### Futurepedia — From Zero to Your First AI Agent in 25 Minutes (No Coding)
- **Intro CTA:** No CTA in intro.
- **Mid-roll (05:05):**  — 
- **End CTA (25:39):**  — 

### Varun Mayya — How to Automate ANYTHING with AI (N8N Tutorial)
- **Intro CTA:** No CTA in intro — CTA appears later in video.

### Kevin Stratvert — n8n Tutorial for Beginners - Build Your First Free AI Agent
- **Intro CTA (?):** N/A

## MG Spacing Rules by Video Length

### Intro (All Lengths)
- **MG Event Count (avg per video):** 8 (shorter-form avg: 11, course-length avg: 5)
- **MG Density:** ~1 MG per 8–10s for shorter-form intros, ~1 per 18s for course-length
- **Max gap between consecutive MGs:** 8s (target 6s)
- **Min gap between consecutive MGs:** 2s

### Body — Shorter-Form (10-30 min)
- **Body MG Events (sampled avg):** 16 per video
- **Body MG Density (overall):** 1.6–3.1 MGs/min
- **Explanatory sections peak:** 6–10 MGs/min
- **Screen share execution:** 0 MGs/min

### Body — Course-Length (1hr+)
- **Body MG Events (sampled avg):** 3 per video
- **Body MG Density (overall):** 0.19–0.55 MGs/min
- **Explanatory sections peak:** 1–3 MGs/min
- **Screen share execution:** 0 MGs/min

## Recurring Patterns Across Creators

- **unknown** (x7) — Using a digital marker to highlight text during screen share.
- **Pop-in Overlays** (x1) — Fast, centered white text with drop shadows to emphasize keywords.

## Chapter Transition Styles

- **Black Title Card:** 11 occurrences
- **Direct cut:** 8 occurrences
- **Direct Cut:** 7 occurrences
- **unknown:** 6 occurrences
- **Title Card:** 5 occurrences
