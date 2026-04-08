---
name: short-form-scripts
description: Generate 5 short-form video scripts with B-roll plan, MG prompts, and conceptual storyboard
menu-code: SS
---

# [SS] Short-Form Scripts

## Purpose

Analyse long-form video content and generate 5 short-form video scripts (15-45 seconds each) optimised for Instagram Reels, TikTok, and YouTube Shorts — including B-roll extraction plans, Hera motion graphic prompts, and conceptual storyboards.

## Role Context

You are a short-form content strategist specialising in vertical video repurposing. You understand hook psychology, scroll-stopping patterns, and the art of distilling long-form insights into punchy, self-contained clips.

**Key insight:** A good short-form clip isn't a "cut down" version of a long video; it's a self-contained story that happens to use the same source material.

## Prerequisites

Load before generating:
- Brand guidelines and ICP profile
- Adam Voice Library
- Script rules from `{project-root}/content-plugin/skills/2-copywriter/workflows/short-form-scripts/data/script-rules.md`
- Example hooks from `{project-root}/content-plugin/skills/2-copywriter/workflows/short-form-scripts/data/example-hooks.md`
- ICP profiles from `{project-root}/content-plugin/skills/2-copywriter/workflows/short-form-scripts/data/icp-profiles.md`

---

## Execution Mode Selection

"**How would you like to run this workflow?**

[A] **Auto** — I'll make best-case decisions at every step, auto-approve all checkpoints, and only come back to you when all 5 scripts are complete. Fastest option.
[C] **Collab** — I'll work through each step with you, presenting concepts for approval, letting you review scripts, and waiting for your input at each checkpoint. Most control."

---

## Phase 1: Source Material Ingestion

### 1.1 Discover Source Content

Check project folder for:
1. Long-form video script (primary source)
2. Video transcript (if already filmed)
3. Content concept brief
4. Storyboard or visual analysis

Present what was found and confirm with user.

### 1.2 Analyse Source Material

Extract from source content:
- Core topic and key arguments
- 5-8 self-contained "clip-worthy" moments
- Key quotes, statistics, or bold claims
- Tool demonstrations or visual moments
- Emotional peaks or transformation moments

### 1.3 Concept Extraction

For each clip-worthy moment, define:
- **Concept ID** — SF-01 through SF-05
- **Hook type** — question, bold claim, demonstration, result reveal, pattern interrupt
- **Core message** — the self-contained insight (1 sentence)
- **Target duration** — 15-45 seconds
- **Target pacing** — 3.3-4.0 words per second

Present concept overview table for approval (Collab mode) or proceed (Auto mode).

---

## Phase 2: Script Writing

For each of the 5 concepts, write a complete short-form script:

### Script Structure

**Hook (0-3 seconds)**
- Must stop the scroll instantly
- Use proven short-form hook formula from example-hooks.md
- First frame must be visually and verbally compelling

**Body (3-35 seconds)**
- Deliver the core insight with clarity and speed
- Short sentences, punchy delivery
- Include 1-2 visual demonstration moments
- Target 3.3-4.0 words per second pacing

**Payoff/CTA (last 5-10 seconds)**
- Satisfying conclusion to the self-contained story
- Lead magnet CTA if applicable (e.g. "Comment KEYWORD for the free guide")
- Follow/subscribe nudge

### Per-Script Deliverables

For each script, produce:
1. **Script text** — word-for-word dialogue with timing markers
2. **B-roll extraction plan** — which segments from the long-form video to use
3. **Motion graphic prompts** — Hera Video API prompts for any graphic overlays
4. **Text overlay plan** — key text that appears on screen
5. **Music/mood note** — energy level and vibe

---

## Phase 3: Review and Polish

### 3.1 Quality Checks

For each script:
- **Voice check** — Would Adam say this casually?
- **Anti-AI filter** — No corporate buzzwords, no filler phrases
- **Hook strength** — Does it stop the scroll?
- **Self-contained test** — Does it make sense without the long-form context?
- **Duration check** — 15-45 seconds at target pacing

### 3.2 Present for Review

Present all 5 scripts in a summary table:

| # | ID | Hook | Duration | Hook Type | Lead Magnet Keyword |
|---|-----|------|----------|-----------|---------------------|
| 1 | SF-01 | {first line} | {seconds} | {type} | {keyword or N/A} |

Then present each script in full for approval.

### 3.3 Save Scripts

Save each script to `{project_folder}/{project-slug}/video-editor/short-form/scripts/sf-{NN}-script.md` with frontmatter including title, concept_id, hook_type, status, duration, and lead_magnet_keyword.

---

## Success Criteria

- 5 distinct scripts generated from source material analysis
- Each script is self-contained (makes sense without long-form context)
- Hook formulas from proven patterns
- Pacing targets 3.3-4.0 wps
- B-roll extraction plans reference specific source material segments
- Motion graphic prompts are Hera-compatible
- Anti-AI red flags cleared
- All scripts saved with correct frontmatter
