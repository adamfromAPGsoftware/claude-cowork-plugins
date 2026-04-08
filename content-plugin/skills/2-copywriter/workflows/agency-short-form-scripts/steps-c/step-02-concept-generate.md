---
name: 'step-02-concept-generate'
description: 'Slot-based concept selection — generate 2-3 candidates per pillar slot, score per slot, pick the best per slot'

nextStepFile: './step-03-script-write.md'
---

# Step 2: Concept Generation — One Concept Per Pillar Slot

## STEP GOAL:

Using the per-slot research candidates from step-01, generate 2–3 developed concepts per pillar slot, score each slot's candidates against the **slot-appropriate scoring rubric**, and select the strongest concept per slot. Output: exactly 5 concepts, one per slot (SF-01 through SF-05).

## MANDATORY EXECUTION RULES (READ FIRST):

### Universal Rules:

- CRITICAL: Read the complete step file before taking any action
- CRITICAL: When loading next step with 'C', ensure entire file is read
- YOU MUST ALWAYS SPEAK OUTPUT in your Agent communication style with the config `{communication_language}`

### Step-Specific Rules:

- Focus ONLY on concept generation and selection — do NOT write scripts yet
- FORBIDDEN to write full scripts in this step
- **COLLAB mode:** Present concepts to user for approval before proceeding
- **AUTO mode:** Auto-approve the best concept per slot and proceed immediately
- Each concept must be a self-contained story — NOT a vague topic
- A concept MUST match its assigned pillar slot — swapping slots is FORBIDDEN
- The Reputation slot (SF-03) MUST NOT have a hard keyword CTA
- The News slot (SF-05) MUST NOT have a hard keyword CTA

## MANDATORY SEQUENCE

### 1. Review Research Brief

Reference the research brief from step-01. Note the 2–3 candidate angles per slot.

### 2. Develop Concepts Per Slot

For each slot, expand each candidate angle into a full concept. Every concept must include:

| Field | Description |
|-------|-------------|
| **Concept title** | Punchy, descriptive title for the video |
| **Pillar slot** | BOFU-A / BOFU-B / Reputation / Case-Study / News |
| **Research angle** | Which step-01 candidate this builds on |
| **Core thesis** | 1 sentence — the single insight this video delivers |
| **Hook line** | Draft hook using the slot-appropriate hook format |
| **Hook format** | Pain Interrupt / Result Reveal / News Anchor / Opinion Statement / Credibility Reveal |
| **ICP / Audience state** | Ready (BOFU) / Stranger + Warm (Reputation, News) / Warm + Ready (Case Study) |
| **offer bridge** | How does this lead to audit interest? ("N/A" for Reputation slot) |
| **CTA plan** | AUDIT / WASTE / AI / RESULTS / none / soft — per slot rules |
| **Value pillar** | SaaS Waste / Efficiency / AI Enablement / Case Study / News Commentary / Reputation |
| **Suggested duration** | Punchy (15–20s) / Standard (22–30s) / Deep (35–45s) |
| **MG visual concept** | 1–2 sentence description of the primary visual |
| **Emotional angle** | Fear / Frustration / Hope / Curiosity / Respect |

### 3. Score Concepts — Per Slot Rubric

Score each candidate within its slot using the **slot-appropriate rubric** (1–5 scale per criterion):

#### BOFU A and BOFU B Rubric

| Criterion | Weight | What to Assess |
|-----------|--------|----------------|
| **BOFU Relevance** | 30% | Does this directly address an SME decision-maker pain point? Would a business owner stop scrolling? |
| **Offer Connection** | 25% | How naturally does this lead to a keyword CTA? Forced = 1, seamless = 5 |
| **Hook Strength** | 25% | Is the hook specific, surprising, or emotionally triggering? Generic = 1, scroll-stopping = 5 |
| **Freshness / Angle Novelty** | 20% | Is this a fresh take or something we've done before? (Check memories for repeat metrics/hooks) |

**Formula:** (BOFU × 0.30) + (Offer × 0.25) + (Hook × 0.25) + (Freshness × 0.20) = Total

---

#### Reputation Slot Rubric (SF-03)

| Criterion | Weight | What to Assess |
|-----------|--------|----------------|
| **Hook Strength** | 35% | Is the opinion strong enough to stop a stranger? Bland = 1, genuinely surprising or contrarian = 5 |
| **Opinion Clarity** | 35% | Is there a clear, specific take? Vague = 1, sharp and defensible = 5 |
| **Credibility Anchor** | 30% | Does the concept include a natural credibility signal? None = 1, compelling first-person proof = 5 |

**Formula:** (Hook × 0.35) + (Opinion × 0.35) + (Credibility × 0.30) = Total

**Automatic disqualifiers for Reputation:**
- Any soft pitch toward the $3K audit — disqualified
- A how-to or educational format — disqualified (that's BOFU, not Reputation)
- No credibility anchor — score cap at 2.0

---

#### Case Study Slot Rubric (SF-04)

| Criterion | Weight | What to Assess |
|-----------|--------|----------------|
| **Specificity of Transformation** | 35% | Does this have a clear before/after with at least 1 specific metric? Generic = 1, concrete numbers = 5 |
| **ICP Relatability** | 35% | Would an SME owner in this industry see themselves in this story? Niche = 1, broad SME appeal = 5 |
| **Offer Connection** | 30% | Does this naturally close toward "Comment RESULTS"? Forced = 1, seamless = 5 |

**Formula:** (Specificity × 0.35) + (Relatability × 0.35) + (Offer × 0.30) = Total

---

#### News Slot Rubric (SF-05)

| Criterion | Weight | What to Assess |
|-----------|--------|----------------|
| **Timeliness** | 35% | How fresh is the news hook? Evergreen = 1, published this week = 5 |
| **Opinion Angle** | 35% | Does Adam have a specific, opinionated take — not just a summary? No take = 1, clear contrarian angle = 5 |
| **Hook Strength** | 30% | Is the opening line attention-grabbing? Generic = 1, scroll-stopping = 5 |

**Formula:** (Timeliness × 0.35) + (Opinion × 0.35) + (Hook × 0.30) = Total

---

### 4. Select Best Concept Per Slot

For each of the 5 slots:
- Rank the 2–3 candidates by their slot rubric score
- Select the highest-scoring concept
- If two candidates score within 0.2 of each other, flag for user review (collab) or pick the one with better hook strength (auto)

**Duration assignment (after slot selection):**
- Assign durations according to pillar duration guidance from agency-script-rules.md
- Ensure overall batch targets approximately: 2 Punchy + 2 Standard + 1 Deep
- Duration is secondary to slot assignment — never change a concept's slot to hit a duration target

### 5. Present Concepts for Approval

"**5 Agency Short-Form Concepts — One Per Pillar Slot**

---

**SF-01 [BOFU A]: {Title}**
- **Slot:** BOFU A | **Hook format:** {format} — "{draft hook line}"
- **Core thesis:** {1 sentence}
- **Value pillar:** {pillar}
- **Duration:** {Punchy / Standard / Deep} ({X}s target)
- **ICP pain point:** {specific pain point}
- **Offer bridge:** {how this leads to audit}
- **CTA:** Comment {KEYWORD} — {lead magnet}
- **MG visual:** {visual concept}
- **Slot score:** {weighted score}/5.0

**SF-02 [BOFU B]: {Title}**
...

**SF-03 [Reputation]: {Title}**
- **Slot:** Reputation | **Hook format:** Opinion Statement / Credibility Reveal
- **Core thesis:** {1 sentence — the take}
- **Duration:** Punchy (15–20s)
- **Credibility anchor:** {the anchor used}
- **CTA:** {none / soft prompt}
- **Slot score:** {weighted score}/5.0

**SF-04 [Case Study]: {Title}**
...

**SF-05 [News]: {Title}**
...

---

**Batch validity check:**
- Slots covered: SF-01 ✓ SF-02 ✓ SF-03 ✓ SF-04 ✓ SF-05 ✓
- Reputation script has no hard keyword CTA: {yes/no}
- News script has no hard keyword CTA: {yes/no}
- Duration mix: {count} Punchy + {count} Standard + {count} Deep (target: ~2+2+1)

**Rejected candidates per slot:**
| Slot | Candidate | Score | Reason Not Selected |
|------|-----------|-------|---------------------|
| BOFU-A | {title} | {score} | {reason} |
| Reputation | {title} | {score} | {reason} |
| ... | ... | ... | ... |

[R] Revise a concept | [S] Swap to a rejected candidate (same slot only) | [C] Approve all and continue"

### 6. Handle Approval

**If `{execution_mode}` = `auto`:**
- Auto-approve the highest-scoring concept per slot without waiting for user input
- Log: "**Auto mode:** 5 concepts auto-approved — one per pillar slot."
- Proceed immediately to next step

**If `{execution_mode}` = `collab`:**
- **[R]** — User wants to revise: ask which concept and what to change
- **[S]** — User wants to swap: show rejected candidates for **that slot only** — cannot swap across slots
- **[C]** — User approves: proceed to next step
- Only proceed when user selects [C]

Update output frontmatter with `stepsCompleted: ['step-01-research', 'step-02-concept-generate']`.

Load, read entire file, then execute {nextStepFile}.

---

## SYSTEM SUCCESS/FAILURE METRICS

### SUCCESS:

- Exactly 5 concepts generated — one per pillar slot (SF-01 through SF-05)
- Each concept scored using the slot-appropriate rubric (not a single shared rubric)
- Reputation concept has no hard keyword CTA and passes opinion + credibility checks
- News concept has a fresh news source AND a specific opinion angle
- Case Study concept has at least one specific metric and a clear before/after
- Duration mix approximately matches 2 Punchy + 2 Standard + 1 Deep
- User has reviewed and approved all 5 (collab) or auto-approved (auto)

### FAILURE:

- Writing full scripts in this step
- Generating fewer than 5 or more than 5 final concepts
- Using the same scoring rubric for all slots (Reputation must use its own rubric)
- Putting a soft-pitch concept in the Reputation slot
- Assigning a hard keyword CTA to Reputation or News slots
- Swapping a concept into a different slot to hit a duration target
- Proceeding without user approval (collab mode only)
