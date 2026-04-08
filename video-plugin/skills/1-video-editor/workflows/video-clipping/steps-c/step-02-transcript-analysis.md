---
name: 'step-02-transcript-analysis'
description: 'Analyze transcript against required script and optional ICP to identify repetitions, retakes, and irrelevant content — primary intelligence for all content cut decisions'

nextStepFile: './step-03-audio-precision.md'
outputFile: '{project_folder}/{project-slug}/video-editor/clips/{video-id}-clip-plan.md'
---

# Step 2: Transcript Content Analysis

## STEP GOAL:

Analyze the transcript to identify repetitive sections (especially intro retakes), off-script tangents, and content not relevant to the ICP — auto-deciding which cuts to apply using flow-based scoring and confidence gating. Transcript-vs-script comparison is the PRIMARY intelligence for deciding WHAT to cut.

## MANDATORY EXECUTION RULES (READ FIRST):

### Universal Rules:

- 📖 CRITICAL: Read the complete step file before taking any action
- 🔄 CRITICAL: When loading next step, ensure entire file is read
- 📋 This step uses LLM analysis to auto-decide content cuts using flow-based scoring
- ✅ YOU MUST ALWAYS SPEAK OUTPUT In your Agent communication style with the config `{communication_language}`

### Role Reinforcement:

- ✅ You are a video editing automation assistant performing content analysis
- ✅ You bring expertise in identifying redundancy, repetition, and content relevance
- ✅ Be conservative — when in doubt, AUTO_REJECT the cut (keep the content)

### Step-Specific Rules:

- 🎯 Focus ONLY on transcript content analysis — no audio work in this step
- 🚫 FORBIDDEN to proceed without generating findings (even if findings are "no issues found")
- 🚫 FORBIDDEN to reference audio analysis data or silence boundaries — this step runs BEFORE audio precision
- ✅ All cuts are AUTO-DECIDED based on confidence — no user review step
- ✅ Script is REQUIRED — loaded from `script_path` in clip plan frontmatter
- ✅ Each cut MUST include: timestamp range, transcript excerpt, reason, and decision (AUTO_APPROVED / AUTO_REJECTED)

## EXECUTION PROTOCOLS:

- 🎯 Follow MANDATORY SEQUENCE exactly
- 💾 Append content cleanup findings to {outputFile}
- 📖 Update frontmatter stepsCompleted when complete
- 🚫 This is an auto-proceed step — no user interaction

## CONTEXT BOUNDARIES:

- Step 1 provided: transcript JSON, required script (`script_path` in frontmatter), optional ICP/content concept
- No prior audio cleanup — this step runs FIRST after initialization
- Transcript contains word-level timestamps
- Script is the intended content — REQUIRED for transcript comparison
- ICP/content concept (if available) defines audience and relevance criteria
- All cut boundaries use raw transcript timestamps — audio precision refinement in step 3 handles boundary snapping

## MANDATORY SEQUENCE

**CRITICAL:** Follow this sequence exactly. Do not skip, reorder, or improvise.

### 1. Load Transcript Data

Load the transcript JSON file identified in step 1.

Extract:
- Full transcript text with word-level timestamps
- Speaker segments (if available)
- Sentence boundaries with timestamps

"**Running transcript content analysis...**"

### 2. Load Reference Documents

**Script (from copywriter) — REQUIRED:**
- Load the script from `script_path` in the clip plan frontmatter
- Extract the intended structure: sections, key points, talking points
- Note: The script represents what SHOULD be in the video

**Content Concept / ICP (from strategist):**
- If available: Load the content concept
- Extract: target audience, key messages, value propositions, content goals
- Note: This defines what is RELEVANT to the audience

**If ICP is not available:**
"ℹ️ No ICP reference available. Analysis will use script comparison and repetition detection (no ICP relevance check)."

### 2b. Content-Type-Specific Analysis Mode

The analysis approach differs significantly by content type. Intros and short-form scripts are delivered near-verbatim — the script is a close match. Body/main content is much looser — the creator regularly diverges from the script with valuable elaborations, ad-libs, and tangents that should be kept.

**Intro / Short-Form (`content_type = intro` or video ID matches `sf-{NN}`):**
- Script comparison is **strict** — transcript should closely match the script
- Off-script content is a stronger signal for potential cuts
- Section-specific scoring adjustments apply:

| Intro Section | Timing | Scoring Rule |
|---------------|--------|-------------|
| **Hook** | 0–5s | NEVER cut — every word is critical. Auto-reject any proposed cut in this range. |
| **Credibility** | 5–25s | Cut only dead air — rapid-fire delivery should be preserved. Higher threshold for semantic repetition (keep both phrasings unless identical). |
| **Value promise** | 25–50s | Allow natural pauses. Standard scoring applies. |
| **Bridge** | 50–70s | Standard clipping rules apply. |

The confidence threshold for AUTO_APPROVED cuts in the 0–25s range should be treated as if it were one level lower (High → Medium, Medium → Low).

**Body / Main (`content_type = main`):**
- Script comparison is **informational only** — the creator frequently and intentionally diverges from the script
- 🚫 FORBIDDEN to cut content just because it's off-script. Off-script paragraphs are expected and often the best parts
- Focus ONLY on **mechanical delivery issues**: false starts, stuttering, repeated attempts at the same sentence, dead rambling (circling the same point without adding value)
- The script is used as a loose reference to understand the topic and intended structure — NOT as a cut-list generator
- When in doubt about body content: **KEEP IT**

### 3. Repetition Detection

Analyze the transcript for repetitive content:

**3a. Exact Repetitions (Retakes) — Flow-Based Selection**
- Identify sections where the same sentence or phrase appears multiple times
- These are especially common in intros where the creator records multiple takes
- For each retake cluster, evaluate every take using **flow-based scoring**:
  1. **Transition smoothness (50%):** Does content before flow naturally into this take? Does this take flow naturally into content after the *last* take in the cluster?
  2. **Delivery quality (30%):** Fewest fillers, fewest false starts, most confident delivery
  3. **Completeness (20%):** Full thought expressed? Incomplete takes are disqualified
- If script reference is available: bonus for the take closest to scripted content
- Select the highest-scoring take, mark all others for removal

**3b. Semantic Repetitions**
- Identify sections where the same idea is expressed differently
- These are common when the creator rephrases or restarts a thought
- For each semantic repetition:
  - Identify the repeated concept
  - Flag the weaker expression for removal
- **Body/main caveat:** Only flag if the repetition is clearly unintentional (creator circling back to the same point within 30 seconds). Intentional callbacks, reframing for emphasis, or building on an idea from a different angle are NOT repetitions — keep them.

**3c. False Starts and Abandoned Sentences**
- Identify sentences that start but are cut off and restarted
- Flag the false start for removal, keep the completed version

**3d. Stuttering and Dead Rambling (Body/Main Focus)**
- Identify sections where the creator is visibly struggling: repeated "um"/"uh" clusters, restarting the same phrase 2-3 times in quick succession, trailing off without completing a thought
- These are mechanical delivery issues, not content issues — safe to cut regardless of content type

### 4. Script Comparison

**Intro / Short-Form mode:**
Compare transcript sections against the original script:

**4a. Off-Script Content**
- Identify sections in the transcript that do not correspond to any part of the script
- Classify each as:
  - **Tangent** — unrelated to the script's goals
  - **Elaboration** — related but not scripted (may be valuable, flag with lower confidence)
  - **Ad-lib** — spontaneous but on-topic (likely keep, flag only if excessive)

**4b. Missing Script Content**
- Identify script sections that were NOT covered in the transcript
- Note these as informational (not cuts, but useful for the creator to know)

---

**Body / Main mode:**
Script comparison is **informational only** — used for context, NOT for generating cuts:

**4a. Script Coverage Map (Informational)**
- Map which script sections were covered in the transcript and which were skipped
- Note any sections covered in a different order than scripted
- This is for the creator's awareness only — no cuts generated from this

**4b. Off-Script Content — DO NOT CUT**
- Log off-script sections for informational purposes only
- Classify as Tangent / Elaboration / Ad-lib (same as intro mode)
- 🚫 NEVER auto-approve cuts of off-script body content — the creator diverges from the script intentionally and these sections are often the most authentic, valuable content

### 5. ICP Relevance Scoring (If ICP Available)

Score transcript sections against the ICP/content concept:

- For each major section of the transcript:
  - Does it serve the target audience?
  - Does it deliver on the key messages?
  - Does it support the content goals?
- Flag sections with LOW relevance score for potential removal
- Be CONSERVATIVE — only flag clearly irrelevant content
- **Body/main:** Even stricter — only flag content that is genuinely off-topic for the video (e.g., unrelated personal anecdotes), NOT content that explores the topic from a different angle than scripted

### 6. Compile and Auto-Decide Content Cuts

Compile all findings into a structured list, then apply confidence-gated auto-decision:

For each identified cut:
- **ID:** Sequential number (C1, C2, C3...)
- **Type:** Repetition / False Start / Stutter / Dead Ramble / Off-Script / Low Relevance
- **Confidence:** High / Medium / Low
- **Timestamp:** Start — End
- **Duration:** Seconds
- **Transcript Excerpt:** The actual words (first 100 characters)
- **Reason:** Clear explanation of why this is flagged for removal
- **Context:** What comes before and after

**Confidence-Gated Auto-Decision (Intro / Short-Form):**

- **High confidence** (clear retakes, obvious false starts, exact repetitions) → `AUTO_APPROVED`
- **Medium confidence** (semantic repetitions, tangents) → `AUTO_APPROVED` only if removing creates a clean transition between surrounding content; otherwise `AUTO_REJECTED`
- **Low confidence** (borderline, ad-libs, elaborations) → `AUTO_REJECTED` (conservative — keep the content)

**Confidence-Gated Auto-Decision (Body / Main):**

- **High confidence** (clear retakes, obvious false starts, stuttering clusters, dead rambling) → `AUTO_APPROVED`
- **Medium confidence** (semantic repetitions within 30s) → `AUTO_APPROVED` only if removing creates a clean transition; otherwise `AUTO_REJECTED`
- **Low confidence** (anything else) → `AUTO_REJECTED`
- 🚫 Off-script content → ALWAYS `AUTO_REJECTED` regardless of confidence (informational only)
- 🚫 ICP low-relevance → ALWAYS `AUTO_REJECTED` unless genuinely off-topic for the entire video

For each cut, set:
- **Decision:** `AUTO_APPROVED` or `AUTO_REJECTED`

### 7. Record Raw Transcript Timestamps

Record raw transcript timestamps for each cut. Audio precision refinement (step 3) will snap these to natural cut boundaries using audio analysis data.

For each AUTO_APPROVED cut, record:
- Raw start timestamp (from transcript word-level data)
- Raw end timestamp (from transcript word-level data)
- These are approximate boundaries — step 3 will refine them to the nearest silence/breath edge for clean audio transitions

### 8. Append Content Cleanup Findings to Clip Plan

Update the **Content Cleanup Findings** section of {outputFile}:

```markdown
## Content Cleanup Findings

**Analysis Performed:**
- Repetition detection: ✅
- Script comparison: ✅
- ICP relevance scoring: {✅ / ⏭️ Skipped — no ICP available}

**Summary:**
- Total cuts identified: {count}
- Auto-approved: {approved_count} ({approved_seconds}s)
- Auto-rejected (kept): {rejected_count} ({rejected_seconds}s)
- By type: {repetitions: N, false starts: N, off-script: N, low relevance: N}

**Content Cuts (Auto-Decided):**

| ID | Type | Confidence | Decision | Start | End | Duration | Excerpt | Reason |
|----|------|------------|----------|-------|-----|----------|---------|--------|
| C1 | Repetition | High | AUTO_APPROVED | 00:15.234 | 00:22.456 | 7.2s | "So today we're going to talk about..." | Retake — same intro repeated, take 2 of 3 |
| C2 | Repetition | High | AUTO_APPROVED | 00:22.890 | 00:29.123 | 6.2s | "So today we're going to talk about..." | Retake — same intro repeated, take 3 of 3 (keeping take 1) |
| C3 | False Start | High | AUTO_APPROVED | 01:45.678 | 01:47.890 | 2.2s | "The thing about this is—" | Abandoned sentence, restarted at 01:48.100 |
| ... | ... | ... | ... | ... | ... | ... | ... | ... |

{If script comparison was performed:}
**Missing Script Sections (Informational):**
- {section name} — Not covered in transcript
```

Update frontmatter: append `'step-02-transcript-analysis'` to `stepsCompleted`.

### 9. Auto-Proceed to Audio Precision

"**Transcript analysis complete. {count} cuts identified, {approved_count} auto-approved ({approved_seconds}s), {rejected_count} auto-rejected (kept).**

**Breakdown:**
- Repetitions: {count}
- False starts: {count}
- Off-script: {count}
- Low relevance: {count}

**Proceeding to audio precision & cleanup...**"

Load, read entire file, then execute {nextStepFile}.

---

## 🚨 SYSTEM SUCCESS/FAILURE METRICS

### ✅ SUCCESS:

- Content-type-specific analysis mode applied (intro/short-form = strict script match; body/main = mechanical cleanup only)
- Transcript fully analyzed for repetitions using flow-based scoring
- Retake clusters evaluated with transition smoothness (50%), delivery quality (30%), completeness (20%)
- Script comparison performed — strict for intro/short-form, informational-only for body/main
- Body/main off-script content kept (NOT cut) — divergence from script is expected and valuable
- ICP relevance scoring performed (if ICP available)
- Each cut has: ID, type, confidence, decision (AUTO_APPROVED/AUTO_REJECTED), timestamps, excerpt, reason
- Raw transcript timestamps recorded for each cut — no audio boundary snapping in this step
- Findings appended to clip plan in structured table
- Conservative approach — low confidence cuts AUTO_REJECTED (kept)
- Auto-proceeded to audio precision step (step 3)

### ❌ SYSTEM FAILURE:

- Cutting off-script body/main content (the creator intentionally diverges — these are often the best parts)
- AUTO_APPROVED on off-script or low-relevance cuts for body/main content
- Not detecting obvious repetitions (especially intro retakes)
- AUTO_APPROVED on low-confidence cuts (must be conservative)
- Missing timestamps or rationale on cuts
- Referencing audio analysis data or silence boundaries (audio precision is step 3)
- Performing audio analysis in this step (that is step 3)
- Asking user for input (this is a fully autonomous step)
- Proceeding without a script (script is REQUIRED)

**Master Rule:** Script is REQUIRED but its role varies by content type. For intros and short-form, transcript-vs-script comparison drives content cuts. For body/main, the script is informational context only — cuts focus exclusively on mechanical delivery issues (false starts, stuttering, dead rambling, exact retakes). Off-script body content is NEVER cut. All cut boundaries use raw transcript timestamps — audio precision refinement in step 3 handles boundary snapping.
