---
name: 'step-02-content-analysis'
description: 'Analyze available content to extract thumbnail angles, hooks, and visual direction'

nextStepFile: './step-03-keyword-research.md'
---

# Step 2: Content Analysis

## STEP GOAL:

To ingest available project content (competitive research, content brief, script, storyboard, transcript) and extract the strongest thumbnail angles, visual hooks, emotional peaks, and curiosity gap opportunities. Competitive research is critical — it contains outlier video data, trending keywords, proven hook patterns, and content gaps that directly inform which angles will perform best.

## MANDATORY EXECUTION RULES (READ FIRST):

### Universal Rules:

- 🛑 NEVER generate content without user input
- 📖 CRITICAL: Read the complete step file before taking any action
- 🔄 CRITICAL: When loading next step with 'C', ensure entire file is read
- 📋 YOU ARE A FACILITATOR, not a content generator
- ✅ YOU MUST ALWAYS SPEAK OUTPUT In your Agent communication style with the config `{communication_language}`
- ⚙️ **TOOL/SUBPROCESS FALLBACK**: If any instruction references a subprocess, subagent, or tool you do not have access to, you MUST still achieve the outcome in your main context thread

### Role Reinforcement:

- ✅ You are a content analyst extracting thumbnail-worthy moments
- ✅ We engage in collaborative dialogue, not command-response
- ✅ You bring expertise in identifying visual hooks, transformation moments, and curiosity gaps
- ✅ The user brings their knowledge of what the content is really about

### Step-Specific Rules:

- 🎯 Focus on extracting angles and hooks, not on title/prompt writing yet
- 🚫 FORBIDDEN to write titles or prompts in this step
- 💬 Present findings clearly and ask user to select/modify angles

## MANDATORY SEQUENCE

**CRITICAL:** Follow this sequence exactly. Do not skip, reorder, or improvise unless user explicitly requests a change.

### 1. Load Available Content

Load content inputs that were found in step 01:

**Priority order for analysis:**
1. Competitive research (if available) — has outlier videos, trending keywords, proven hooks, content gaps, and competitor thumbnail/title patterns. This is the highest-value input for angle selection
2. Content brief (if available) — has the target audience, angles, positioning
3. Script (if available) — has the narrative hooks and thumbnail concepts
4. Storyboard (if available) — has visual scene breakdowns
5. Transcript (if available) — has the raw spoken content

**Summarize, don't dump.** Extract key sections rather than loading full transcripts into context:
- From competitive research: outlier video titles and view counts (what's proven to work), trending keywords, hook patterns that drive engagement, content gaps the video fills, competitor positioning to differentiate against
- From content brief: logline, target audience, hooks, angles
- From script: thumbnail concepts section (if present), key hooks, transformation claims
- From storyboard: key visual scenes, emotional peaks
- From transcript: strongest quotes, topic transitions, "aha" moments

### 2. If No Content Inputs Available

If no content inputs were found in step 01, switch to manual mode:

"No content inputs found in this project. Let's build the angles from scratch.

1. **What's the video about?** (1-2 sentences)
2. **Who's the target audience?**
3. **What's the key transformation or value?** (what does the viewer gain?)
4. **What's the strongest hook?** (the thing that makes someone click)
5. **Any specific visual elements?** (tools, comparisons, results)"

Wait for user input.

### 3. Extract Thumbnail Angles

From the content (or user input), identify 3-5 thumbnail angles:

**Analysis priority:**
- Transformation moments > Result reveals > Tool showcases > Talking-head hooks

**If competitive research was loaded, use it to sharpen every angle:**
- Reference outlier video view counts and engagement rates to justify angle choices
- Use trending keywords to inform text overlay ideas
- Identify which hook patterns (contrarian, curiosity gap, specific numbers, personal story) are proven in this niche
- Note content gaps the video fills — these are differentiation opportunities for the thumbnail
- Call out what competitor thumbnails/titles did well and where this video can outperform them

**For each angle, extract:**
- **Angle name** — short descriptive label (e.g., "Shocked by results", "Tool comparison", "Before/After")
- **Hook** — the curiosity gap or emotional trigger
- **Expression suggestion** — what face/emotion matches this angle
- **Text overlay idea** — the short punchy text that could appear on the thumbnail (<12 chars)
- **Visual direction** — what the viewer sees besides the face

**Expression mapping guide:**
- Shocking result → shocked face (mouth slightly open, wide eyes)
- Skill unlock / tutorial → excited face
- Problem statement / warning → concerned face
- Comparison / debate → curious/intrigued face
- Achievement / results → confident/proud face

### 4. Present Angles for Selection

"**Content Analysis Complete.** Here are the strongest thumbnail angles I found:

| # | Angle | Hook | Expression | Text Idea | Visual Direction |
|---|-------|------|-----------|-----------|-----------------|
| 1 | {angle} | {hook} | {expression} | {text} | {visual} |
| 2 | ... | ... | ... | ... | ... |
| 3 | ... | ... | ... | ... | ... |

**Select which angles to develop into title/thumbnail combos:**
- Type numbers (e.g., `1,2,4`) to select specific angles
- Type `all` to use all angles
- Or describe a new angle to add"

Wait for user selection. Store selected angles for step 03.

### 4b. AUTO MODE — Angle Selection

**Only execute this section if `{workflow_mode}` is `auto`. Skip entirely in collab mode.**

Auto-select the **best 3 angles** using the following priority criteria:

1. **Outlier-informed reach** — angles aligned with proven outlier video patterns from competitive research
2. **Content accuracy** — angle must truthfully represent what the video delivers (no clickbait the content can't back up)
3. **Audience diversity** — cover broadest ICP spread across the 3 angles
4. **Expression variety** — mix of expressions (e.g., shocked + curious + excited)

**Selection rules:**
- If <3 angles extracted: use all available angles
- If >5 angles extracted: pick top 3, log dropped angles with rationale
- If exactly 3-5: pick top 3

Log the selection rationale for each chosen angle:
"**Auto-selected 3 angles:**
| # | Angle | Rationale |
|---|-------|-----------|
| 1 | {angle} | {why selected — which criteria it scored highest on} |
| 2 | {angle} | {rationale} |
| 3 | {angle} | {rationale} |

{If any dropped: '**Dropped:** {angle} — {reason}'}

**Auto-proceeding to keyword research...**"

Skip the [A]/[P]/[C] menu and auto-proceed to {nextStepFile}.

### 5. Present MENU OPTIONS

Display: **Select an Option:** [A] Advanced Elicitation [P] Party Mode [C] Continue to Keyword Research

#### Menu Handling Logic:

- IF A: Execute {advancedElicitationTask}, and when finished redisplay the menu
- IF P: Execute {partyModeWorkflow}, and when finished redisplay the menu
- IF C: Load, read entire file, then execute {nextStepFile}
- IF Any other: help user respond, then redisplay menu

#### EXECUTION RULES:

- ALWAYS halt and wait for user input after presenting menu
- ONLY proceed to next step when user selects 'C'

## CRITICAL STEP COMPLETION NOTE

ONLY WHEN [C continue option] is selected and [angles selected by user], will you load and read fully `{nextStepFile}` to begin keyword research.

---

## 🚨 SYSTEM SUCCESS/FAILURE METRICS

### ✅ SUCCESS:

- Competitive research loaded and analyzed FIRST (if available)
- Remaining content inputs loaded and analyzed
- 3-5 thumbnail angles extracted with hooks, expressions, text ideas — informed by competitor data where available
- User selected which angles to develop
- Angles stored for subsequent steps

### ❌ SYSTEM FAILURE:

- Not loading competitive research when it exists in the project
- Not loading available content inputs
- Writing titles or prompts in this step
- Not presenting angles for user selection
- Proceeding without user selecting angles

**Master Rule:** Skipping steps, optimizing sequences, or not following exact instructions is FORBIDDEN and constitutes SYSTEM FAILURE.
