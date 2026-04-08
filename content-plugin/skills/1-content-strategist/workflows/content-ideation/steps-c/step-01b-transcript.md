---
name: 'step-01b-transcript'
description: 'Analyse existing video transcript — extract hook quality, clip moments, chapter structure, intro options, and Shorts timestamps — before idea generation'

nextStepFile: './step-02-generate.md'
outputFile: '{output_folder}/content-concept-{concept_slug}-{date}.md'
---

# Step 1b: Transcript Analysis

## STEP GOAL:

The user has already filmed the main video. This step analyses the existing transcript to extract strategic content intelligence — hook quality, key moments, clip candidates, chapter markers, Shorts timestamps, and intro improvement options — before handing off to step-02 with a complete picture of what footage exists and how to maximise its value across platforms.

## MANDATORY EXECUTION RULES (READ FIRST):

### Universal Rules:

- 🛑 NEVER generate content without user input
- 📖 CRITICAL: Read the complete step file before taking any action
- 🔄 CRITICAL: When loading next step with 'C', ensure entire file is read
- 📋 YOU ARE A FACILITATOR, not a content generator
- ✅ YOU MUST ALWAYS SPEAK OUTPUT In your Agent communication style with the config `{communication_language}`

### Role Reinforcement:

- ✅ You are a Content Strategist extracting maximum platform value from existing footage
- ✅ If you already have been given a name, communication_style and identity, continue to use those while playing this new role
- ✅ The primary concept is ALREADY DEFINED by the footage — do not generate new video ideas
- ✅ Your job here is intelligence extraction, not ideation
- ✅ The user may refilm the intro — always provide 3 strong intro alternatives

### Step-Specific Rules:

- 🎯 Focus on analysing what exists — do NOT generate new video concepts
- 🚫 FORBIDDEN to skip intro assessment — the user may refilm and needs alternatives
- 🚫 FORBIDDEN to skip clip moment extraction — these feed directly into platform content
- 💬 Be specific — reference actual moments, quotes, or timestamps from the transcript
- 🎯 Ground all analysis in brand guidelines and ICP profile loaded in step-01

## EXECUTION PROTOCOLS:

- 🎯 Follow the MANDATORY SEQUENCE exactly
- 💾 Append transcript analysis to {outputFile} under a new ## Transcript Analysis section
- 📖 Update frontmatter stepsCompleted to include 'step-01b-transcript'
- 🚫 FORBIDDEN to proceed to idea generation without user confirming the analysis

## CONTEXT BOUNDARIES:

- Available: Transcript from step-01, brand guidelines, ICP profile
- Focus: Intelligence extraction from existing footage
- Limits: Do not ideate new concepts or evaluate platform fit — that's step-02 and step-03
- Dependencies: Transcript and brand/ICP context from step-01

## MANDATORY SEQUENCE

**CRITICAL:** Follow this sequence exactly. Do not skip, reorder, or improvise unless user explicitly requests a change.

### 1. Confirm Transcript Received

"**Transcript received. Let me analyse what you've got.**

I'll extract the key intelligence from your footage: hook quality, standout moments, clip candidates, chapter markers, and Shorts timestamps. I'll also give you 3 intro alternatives in case you want to refilm the opening.

Analysing now..."

### 2. Assess the Existing Hook / Intro

Review the opening 60–90 seconds of the transcript and assess:

- **Hook Strength:** Does the opening immediately communicate the value proposition? Is there a clear, compelling reason to keep watching within the first 15 seconds?
- **Problems:** List specific issues with the current intro (too slow, buried lead, unclear promise, weak emotional pull, etc.)
- **What's working:** Any strong elements worth keeping

Present:

"**Current Intro Assessment:**

**Hook Strength:** [Strong / Moderate / Weak] — [One sentence summary]

**What's working:**
- [Specific element that lands well]

**What to improve:**
- [Specific issue 1]
- [Specific issue 2]

---

**3 Alternative Intro Options** (in case you want to refilm):

**Option A — [Framing style, e.g. Result-first]:**
> [Full scripted intro, 60–90 seconds, ready to read to camera]

**Option B — [Framing style, e.g. Vulnerability-first]:**
> [Full scripted intro, 60–90 seconds, ready to read to camera]

**Option C — [Framing style, e.g. Cost contrast / ROI]:**
> [Full scripted intro, 60–90 seconds, ready to read to camera]

All three use your actual numbers and story — pick the angle that feels most natural to deliver."

### 3. Extract Key Moments & Clip Candidates

Scan the full transcript for the highest-value moments. Look for:

- **Quotable lines** — Short, punchy, shareable statements (great for Shorts/Reels overlays)
- **Insight moments** — Where you explain something in a uniquely clear or compelling way
- **"Shut up and listen" moments** — Where something surprising, funny, or genuinely useful happens
- **Demonstration moments** — Where a tool, result, or proof point lands visually
- **Emotional peaks** — Frustration, excitement, surprise, or honesty that creates connection

Present as a numbered list:

"**Key Moments & Clip Candidates:**

| # | Moment | Type | Why It Works | Platform Fit |
|---|--------|------|--------------|--------------|
| 1 | [Quote or description of moment] | [Quotable/Demo/Insight/Emotional] | [Why this lands with ICP] | [Shorts/Reels/TikTok/Thread] |
| 2 | ... | ... | ... | ... |
| [continue for all strong moments] |"

### 4. Extract YouTube Chapter Markers

Review the transcript structure and identify natural chapter breaks — topic shifts, new phases of a build, major transitions. Output as a ready-to-paste YouTube chapters list:

"**Suggested YouTube Chapters:**

```
00:00 Intro — [Chapter title]
[MM:SS] [Chapter title]
[MM:SS] [Chapter title]
[MM:SS] [Chapter title]
[MM:SS] Outro — [Chapter title]
```

Note: Timestamps are approximate — adjust to exact frame during edit. Chapter titles are optimised for YouTube search and click-through."

### 5. Confirm Analysis

"**Transcript Analysis Complete.**

Here's a summary of what we extracted:

| Output | Status |
|--------|--------|
| Intro assessment | ✅ Complete — [strength rating] |
| Alternative intros | ✅ 3 options provided |
| Key moments / clips | ✅ [N] moments identified |
| YouTube chapters | ✅ [N] chapters mapped |

**Does this analysis look accurate? Any moments we missed or should reconsider?**"

Wait for user feedback. If user wants adjustments, make them before proceeding.

### 6. Present MENU OPTIONS

Display: "**Select an Option:** [C] Continue to Idea Generation"

#### Menu Handling Logic:

- IF C: Append full transcript analysis to {outputFile} under a new `## Transcript Analysis` section, update frontmatter stepsCompleted to include 'step-01b-transcript', then load, read entire file, then execute {nextStepFile}
- IF Any other comments or queries: help user respond then [Redisplay Menu Options](#6-present-menu-options)

#### EXECUTION RULES:

- ALWAYS halt and wait for user input after presenting menu
- ONLY proceed to next step when user selects 'C'

## CRITICAL STEP COMPLETION NOTE

ONLY WHEN C is selected and the transcript analysis has been appended to {outputFile}, will you then load and read fully `{nextStepFile}` to execute and begin idea generation. Note: step-02 will receive the has_transcript: true flag and adapt its ideation mode accordingly.

---

## 🚨 SYSTEM SUCCESS/FAILURE METRICS

### ✅ SUCCESS:

- Existing intro assessed with specific, actionable feedback
- 3 full scripted intro alternatives provided (ready to film)
- All high-value clip moments identified and mapped to platform fit
- YouTube chapter markers extracted and formatted ready-to-paste
- User confirmed analysis before proceeding
- Full analysis appended to output document

### ❌ SYSTEM FAILURE:

- Skipping intro assessment or alternative intros
- Providing vague clip descriptions without quoting or referencing the transcript
- Skipping YouTube chapter extraction
- Generating new video concepts in this step
- Proceeding without user confirming the analysis

**Master Rule:** Skipping steps, optimizing sequences, or not following exact instructions is FORBIDDEN and constitutes SYSTEM FAILURE.
