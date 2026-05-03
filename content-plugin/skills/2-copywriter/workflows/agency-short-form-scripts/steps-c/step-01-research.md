---
name: 'step-01-research'
description: 'Per-pillar research pass covering BOFU, Reputation, Case Study, and News slots for agency short-form scripts'

nextStepFile: './step-02-concept-generate.md'
agencyScriptRulesData: '../data/agency-script-rules.md'
newsSearchQueries: '../data/agency-news-search-queries.md'
reputationAnglesData: '../data/reputation-angles.md'
icpBofuDoc: '{project-root}/content-plugin/data/memory/agency-sidecar/agency-offer.md'
---

# Step 1: Research — Per-Pillar Content Discovery

## STEP GOAL:

Run a targeted research pass for each of the 5 pillar slots (BOFU A, BOFU B, Reputation, Case Study, News). Curate at least 2 candidate angles per slot (10 total minimum) so step-02 can select the strongest concept per slot.

## MANDATORY EXECUTION RULES (READ FIRST):

### Universal Rules:

- CRITICAL: Read the complete step file before taking any action
- CRITICAL: When loading next step with 'C', ensure entire file is read
- YOU MUST ALWAYS SPEAK OUTPUT in your Agent communication style with the config `{communication_language}`

### Role Reinforcement:

- You are a content strategist serving a wholesome brand system — BOFU conversion AND authority building
- Each slot has a different audience state: strangers, warm, ready
- Collaborative partnership with the user

### Step-Specific Rules:

- Focus ONLY on research and angle curation — do NOT generate concepts or write scripts
- FORBIDDEN to write full concepts or scripts in this step
- FORBIDDEN to proceed without at least 2 candidate angles per pillar slot (10 total minimum)

## MANDATORY SEQUENCE

### 1. Load Context Documents

Load and read ALL of the following before any research:
- `{icpBofuDoc}` — ICP profile with pain points, value framework, case studies, and CTA patterns
- `{agencyScriptRulesData}` — especially the Batch Pillar System, CTA rules by pillar, hook patterns, and brand voice overrides
- `{reputationAnglesData}` — evergreen Reputation angle library, credibility anchors, hot-take templates
- Brand guidelines from `{project-root}/references/brand-voice.md`

### 2. Load News Search Query Templates

Load `{newsSearchQueries}` — curated Exa search queries organised by value pillar, plus evergreen fallback angles.

### 3. Per-Pillar Research Pass

Run research for each of the 5 pillar slots. Each slot has a different source strategy:

---

#### SLOT SF-01 — BOFU A (Problem Awareness)

**Goal:** Find 2–3 angles that reveal operational waste, SaaS cost, or efficiency loss for SME decision-makers.

**Source strategy:**
- Run 1–2 Exa searches using SaaS Waste and Efficiency queries from `{newsSearchQueries}`
- Pull 1–2 evergreen angles from the pain point matrix in `{icpBofuDoc}` if news is thin
- Prioritise angles with a specific metric or dollar figure (strongest BOFU hooks)

---

#### SLOT SF-02 — BOFU B (AI Enablement / Offer Proof)

**Goal:** Find 2–3 angles covering AI readiness, data foundation, or proof of the audit offer.

**Source strategy:**
- Run 1–2 Exa searches using AI Enablement queries from `{newsSearchQueries}`
- Pull 1 evergreen angle from the AI Enablement pillar in `{icpBofuDoc}` as fallback
- Offer proof angles (audit walkthrough, ROI breakdown) are always available from `{icpBofuDoc}` — no Exa needed

---

#### SLOT SF-03 — Reputation (Opinion / Authority)

**Goal:** Identify 2–3 strong opinion angles that build authority without pitching.

**Source strategy:**
- Pull 2–3 pre-seeded hot takes from `{reputationAnglesData}` that haven't been used recently (check memories)
- If running fresh Exa research for another slot surfaces a stat that would anchor a Reputation take (SaaS valuations, AI adoption data, AUS SME tech spend), capture it here
- Optional: Run 1 targeted Exa search for the most topical Reputation angle (e.g., current SaaS valuations, AI adoption surveys)

**Reputation angle requirements:**
- Must be a genuine opinion or strong take — not educational how-to
- Must include at least one credibility anchor from `{reputationAnglesData}`
- No offer bridge required — authority IS the value

---

#### SLOT SF-04 — Case Study (Client Transformation)

**Goal:** Select 2–3 case study angles from existing material.

**Source strategy:**
- Pull directly from case studies section in `{icpBofuDoc}` — NO Exa search needed
- Each candidate must have: client profile + before state + after state + at least one specific metric
- Available cases: {CASE_STUDY_1}, {CASE_STUDY_2}, Construction/Landscaping, NDIS Provider, Agricultural Equipment Dealer
- Flag any case study metrics that were used in the previous batch (check memories) to avoid repetition

---

#### SLOT SF-05 — News (Current Events Hook)

**Goal:** Find 2–3 angles anchored in recent news that the creator can opine on.

**Source strategy:**
- Run 1–2 Exa searches using News Commentary queries from `{newsSearchQueries}`
- Prioritise: local SME tech news, SaaS platform changes/pricing, AI adoption stats, government digital policy
- Every News angle needs both a news hook AND an opinion angle — pure news recap is not enough
- If news cycle is quiet (fewer than 2 usable fresh/recent items), note it and use a Recent (14–30 days) angle rather than skipping the slot

---

### 4. Curate Angles Per Slot

For each slot, document 2–3 candidate angles using this structure:

| Field | Description |
|-------|-------------|
| **Angle title** | Short, descriptive title |
| **Pillar slot** | BOFU-A / BOFU-B / Reputation / Case-Study / News |
| **Source** | News headline + publication + date / "Case study: {name}" / "Evergreen — reputation-angles.md Take {N}" |
| **Key finding / core POV** | 1–2 sentence summary of the insight or opinion |
| **ICP connection** | Which SME pain point or audience state does this reach? |
| **offer bridge** | How does this connect to the $3K audit? (N/A for Reputation) |
| **Potential hook format** | Pain Interrupt / Result Reveal / News Anchor / Opinion Statement / Credibility Reveal |
| **Freshness** | Fresh (< 14 days) / Recent (14–30 days) / Evergreen |

### 5. Coverage Check

Before saving, verify:
- All 5 pillar slots have at least 2 candidate angles
- BOFU and Case Study angles have specific metrics or dollar figures
- Reputation angles have a credibility anchor and a genuine opinion (not a soft pitch)
- News angles have both a news source AND an opinion layer
- No hard keyword CTA is planned for Reputation or News slots (CTA assignment happens in step-02)

If any slot has fewer than 2 candidates, fill the gap before proceeding.

### 6. Save Research Brief

Save the research brief to:
`{agency_folder}/{project-slug}/copywriter/agency-sf/research-brief-{date}.md`

Format:

```markdown
---
title: 'Agency SF Research Brief'
date: '{current_date}'
queries_run: {count}
angles_curated: {count}
slots_covered: ['BOFU-A', 'BOFU-B', 'Reputation', 'Case-Study', 'News']
stepsCompleted: ['step-01-research']
---

# Agency Short-Form Research Brief — {date}

## Queries Executed

| # | Query | Slot Target | Results Found | Usable Angles |
|---|-------|-------------|--------------|---------------|
| 1 | {query text} | {slot} | {count} | {count} |
| ... | ... | ... | ... | ... |

## Candidate Angles by Slot

### SF-01 BOFU A — Candidates

#### Candidate A1: {title}
- **Source:** {source}
- **Core POV / Key finding:** {1-2 sentences}
- **ICP connection:** {pain point or audience state}
- **offer bridge:** {connection to your sales/audit pipeline}
- **Hook format:** {format}
- **Freshness:** {Fresh/Recent/Evergreen}

#### Candidate A2: {title}
...

### SF-02 BOFU B — Candidates
...

### SF-03 Reputation — Candidates
...

### SF-04 Case Study — Candidates
...

### SF-05 News — Candidates
...

## Coverage Summary

| Slot | Candidates Found | Metrics Present | Source Type |
|------|-----------------|-----------------|-------------|
| BOFU-A | {count} | {yes/no} | {news/evergreen} |
| BOFU-B | {count} | {yes/no} | {news/evergreen} |
| Reputation | {count} | credibility anchor: {yes/no} | reputation-angles.md + {optional exa} |
| Case-Study | {count} | {yes/no} | agency-offer.md |
| News | {count} | opinion angle: {yes/no} | {fresh/recent} |
```

### 7. Present and Proceed

**If `{execution_mode}` = `collab`:**

"**Research Complete — {count} Angles Curated Across 5 Pillar Slots**

{Show summary table: slot, candidate count, top angle title per slot, freshness}

**Coverage check:**
- BOFU A: {count} candidates
- BOFU B: {count} candidates
- Reputation: {count} candidates
- Case Study: {count} candidates
- News: {count} candidates

[R] Review angles for a specific slot | [A] Add an angle | [D] Drop an angle | [C] Approve and continue to concept generation"

Wait for user input.

**If `{execution_mode}` = `auto`:**

Auto-approve all curated angles. Log: "**Auto mode:** {count} angles auto-approved across all 5 pillar slots."

Proceed immediately to next step.

Load, read entire file, then execute {nextStepFile}.

---

## SYSTEM SUCCESS/FAILURE METRICS

### SUCCESS:

- All 5 pillar slots have at least 2 candidate angles
- 3–6 Exa searches executed targeting the correct slots (BOFU, Reputation optional, News required)
- Case Study slot sourced from agency-offer.md (not from Exa)
- Reputation slot sourced from reputation-angles.md (not invented from scratch)
- Research brief saved to correct output path with per-slot sections
- Proceeding to concept generation

### FAILURE:

- Any pillar slot with fewer than 2 candidate angles
- All angles from BOFU slots only (missing Reputation/News/Case Study)
- Reputation angles that are actually soft pitches or how-to content
- News angles with no opinion layer
- Writing full concepts or scripts in this step
- Not loading all 4 context documents (ICP, rules, reputation-angles, brand guidelines)
- Proceeding without user approval (collab mode only)
