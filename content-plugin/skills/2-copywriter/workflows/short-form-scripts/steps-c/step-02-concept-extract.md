---
name: 'step-02-concept-extract'
description: 'Analyse long-form transcript to identify 5 best repurposable angles for short-form videos'

nextStepFile: './step-03-script-write.md'
---

# Step 2: Concept Extraction — Identify 5 Repurposable Angles

## STEP GOAL:

Analyse the long-form transcript, visual analysis, and audio analysis to identify the 5 best self-contained concepts that can be repurposed as short-form vertical videos.

## MANDATORY EXECUTION RULES (READ FIRST):

### Universal Rules:

- 📖 CRITICAL: Read the complete step file before taking any action
- 🔄 CRITICAL: When loading next step with 'C', ensure entire file is read
- ✅ YOU MUST ALWAYS SPEAK OUTPUT in your Agent communication style with the config `{communication_language}`

### Step-Specific Rules:

- 🎯 Focus ONLY on concept identification — do NOT write scripts yet
- 🚫 FORBIDDEN to write full scripts in this step
- 📋 **COLLAB mode:** Present concepts to user for approval before proceeding
- 📋 **AUTO mode:** Auto-approve the best 5 concepts and proceed immediately
- 🎯 Each concept must be a self-contained story — NOT a clip from the middle of a thought

## MANDATORY SEQUENCE

### 1. Analyse Transcript for Concept Candidates

Scan the full long-form transcript for segments that meet these criteria:

**Concept Signals (prioritise in this order):**

1. **Emotional peaks** — Sections where audio energy is high (from audio-analysis.json), speaker pace increases, or language becomes emphatic
2. **Story arcs / build journeys** — Mini-stories with setup → conflict → resolution that fit in 22-45 seconds. Prioritise segments where the body video shows a real build/demo journey: opening a tool, running a process, getting a result. Cross-reference `visual-analysis.json` for consecutive `screen-share` or `mixed-pip` segments that form a narrative arc.
3. **Quotable statements** — Concise, punchy insights that stand alone without context (look for declarative sentences with strong opinions)
4. **Tool demos / how-to moments** — Practical demonstrations that show a result (cross-reference with visual-analysis.json for screen recording segments)
5. **Pain point articulation** — Moments where the speaker names a specific frustration the ICP feels
6. **Unique insights** — Counter-intuitive claims, surprising data points, or original frameworks
7. **Free tool/resource mentions** — Moments where a free tool, template, or resource is named (13/15 top performers mention "free")

**For each candidate, note:**
- Core thesis (1 sentence)
- Source timestamp range (start–end in transcript)
- Why it works as standalone short-form
- **Angle type:** Story / Tool-Focus / Concept / Value-Drop / Before/After (see Angle Diversity in script-rules.md)
- **Target ICP:** Primary (TOFU) if angle is Story / Tool-Focus / Concept / Value-Drop; Secondary (BOFU) if Before/After. If no natural BOFU moment exists in the transcript, identify the closest pain-point moment and note it as a candidate for Before/After reframe using known metrics from the Language Register Guide in `icp-profiles.md`
- **Emotional register:** Curious / Energised / Pragmatic / Relieved / Challenged (match to angle type via the ICP matrix in `icp-profiles.md`)
- Complexity level: Simple (one insight) / Medium (demo or story) / Complex (step-by-step or framework)
- Suggested duration category: Punchy (15–20s) / Standard (22–30s) / Deep (35–45s) — based on complexity
- Estimated word count at 3.5 wps average
- Audio energy level at that point (from audio-analysis.json)
- **Body video moments** (Story-type only): 2–4 specific body video timestamps with descriptions of what's visible on screen. For non-Story types: "N/A"

### 2. Apply Diversity Filter

From all candidates, select the **5 best** ensuring:

- **No duplicate angles** — Each concept covers a different topic/insight
- **Angle diversity** — Minimum **1 Story** + minimum **1 Tool-Focus** angle type. If the body video has 3+ tool interaction segments in visual-analysis.json, target 2 Story. Fallback: if story candidates are weak (few build/demo moments in the body video), allow 1 Story + 2 Tool-Focus + 2 Concept.
- **Spread across source** — Concepts should come from different sections of the long-form video, not all from one segment
- **ICP relevance** — Each concept must resonate with at least one ICP segment
- **ICP diversity** — Minimum **1 Before/After (Secondary ICP)** concept per batch. If no natural BOFU moment exists in the transcript, assign the weakest TOFU concept as the Secondary slot and reframe it as Before/After using the Language Register Guide in `icp-profiles.md`
- **Emotional register diversity** — Minimum **2 distinct emotional registers** across the 5 concepts

### 3. Assign Hook Angles

For each of the 5 selected concepts, draft a **hook angle** — the first 3-5 seconds that will stop the scroll:

Hook angle types (data-backed, ordered by frequency in top 15):
- **Product Drop (dominant):** "[Company] just [dropped/launched] [Product]"
- **Elimination:** "You don't need to [pay for X] anymore"
- **Pain Interrupt:** "Stop [doing wrong thing]"
- **Step-by-Step Tease:** "Here's how to [outcome], step by step"
- **Result Reveal:** "This [tool/technique] saved me [metric]"

### 4. Identify Reference Frames for MG Generation

For each concept, scan the visual-analysis.json to find:
- Relevant screen recordings or tool demos from the long-form video
- Keyframe timestamps that could be extracted as reference images for Hera MG prompts
- Note: These frames are NOT used directly — they feed Hera MG generation as reference images

### 5. Present Concepts for Approval

Present all 5 concepts in a structured format:

"**5 Short-Form Video Concepts Extracted**

---

**SF-01: {Title}**
- **Hook angle:** {hook type} — "{draft hook line}"
- **Core thesis:** {1 sentence}
- **Source:** {timestamp range} ({segment name})
- **Duration category:** {Punchy / Standard / Deep} ({X}s target, ~{W} words)
- **Reference frames for MG:** {list of keyframe timestamps with descriptions for Hera MG generation}
- **Angle type:** {Story / Tool-Focus / Concept / Value-Drop / Before/After}
- **Target ICP:** {Primary (TOFU) / Secondary (BOFU)}
- **Emotional register:** {Curious / Energised / Pragmatic / Relieved / Challenged}
- **Body video moments:** {Story-type: list of 2–4 timestamps with descriptions | Non-Story: N/A}
- **Type:** {concept signal type}

**SF-02: {Title}**
...

---

**Diversity check:**
- Angle types: {list — must include at least 1 Story + 1 Tool-Focus}
- Signal types: {list}
- Source segments: {list}
- ICP coverage: {N} Primary + {N} Secondary (must be ≥1 Secondary)
- Emotional registers: {list} (must have ≥2 distinct)
- Before/After concept: SF-{NN}
- Duration mix: {count} Punchy + {count} Standard + {count} Deep (target: 1 + 3 + 1)

[R] Revise a concept | [S] Swap a concept for a different candidate | [C] Approve all and continue"

### 6. Handle Approval

**If `{execution_mode}` = `auto`:**
- Auto-approve the 5 best concepts without waiting for user input
- Log: "**Auto mode:** 5 concepts auto-approved based on best-case analysis."
- Proceed immediately to next step

**If `{execution_mode}` = `collab`:**
- **[R]** — User wants to revise: ask which concept and what to change
- **[S]** — User wants to swap: show next-best candidate for that slot
- **[C]** — User approves: proceed to next step
- Only proceed when user selects [C]

Update output frontmatter with `stepsCompleted: ['step-01-init', 'step-02-concept-extract']`.

Load, read entire file, then execute {nextStepFile}.

---

## 🚨 SYSTEM SUCCESS/FAILURE METRICS

### ✅ SUCCESS:

- 5 concepts identified with diversity across angles, source segments, and ICP relevance
- Each concept has a hook angle, source timestamps, and reference frames for MG generation
- Each concept card includes `Target ICP` and `Emotional register` fields
- Diversity check shows ≥1 Secondary ICP (Before/After) concept and ≥2 distinct emotional registers
- User has reviewed and approved all 5 concepts (collab) or auto-approved (auto)
- No duplicate angles

### ❌ SYSTEM FAILURE:

- Writing full scripts in this step
- Presenting fewer than 5 concepts
- All concepts from the same section of the long-form video
- Proceeding without user approval (collab mode only)
- All 5 concepts are Primary ICP (no Secondary ICP / Before/After concept)
- Concept cards missing `Target ICP` or `Emotional register` fields
