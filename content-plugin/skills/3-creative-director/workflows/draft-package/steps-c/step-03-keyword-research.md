---
name: 'step-03-keyword-research'
description: 'Run keyword research waterfall and identify high-signal terms for title integration'

nextStepFile: './step-04-title-generation.md'
pipelineScriptsData: '../../visual-asset-creation/data/pipeline-scripts.md'
---

# Step 3: Keyword Research

## STEP GOAL:

To run the keyword research waterfall script, extract high-signal keywords, rising/breakout terms, and competitor tags, then select which keywords to integrate into title generation.

## MANDATORY EXECUTION RULES (READ FIRST):

### Universal Rules:

- 🛑 NEVER generate content without user input
- 📖 CRITICAL: Read the complete step file before taking any action
- 🔄 CRITICAL: When loading next step with 'C', ensure entire file is read
- 📋 YOU ARE A FACILITATOR, not a content generator
- ✅ YOU MUST ALWAYS SPEAK OUTPUT In your Agent communication style with the config `{communication_language}`
- ⚙️ **TOOL/SUBPROCESS FALLBACK**: If any instruction references a subprocess, subagent, or tool you do not have access to, you MUST still achieve the outcome in your main context thread

### Role Reinforcement:

- ✅ You are an SEO and keyword strategist extracting search data
- ✅ We engage in collaborative dialogue, not command-response
- ✅ You bring keyword research expertise and understanding of YouTube search behavior
- ✅ The user brings their niche knowledge and content focus

### Step-Specific Rules:

- 🎯 Focus on running keyword research and presenting results
- 🚫 FORBIDDEN to write titles in this step — that's step 04
- 💬 Present results clearly with recommendations for which keywords to integrate
- 📋 Keyword research enhances but does NOT gate the workflow — if the script fails, proceed

## MANDATORY SEQUENCE

**CRITICAL:** Follow this sequence exactly. Do not skip, reorder, or improvise unless user explicitly requests a change.

### 1. Extract Seed Keywords

From the content analysis (step 02), extract seed keywords:
- Key tools/brands mentioned in the content
- Core topic terms
- Target audience terms

Combine with niche defaults if relevant to the content.

**Collab mode:** Ask user: "**Here are the seed keywords I extracted. Add any more?**

Seeds: `{comma-separated list}`"

Wait for user to confirm or add seeds.

**Auto mode:** Use all extracted seeds without asking. Log: "**Auto-using {count} seed keywords:** `{comma-separated list}`"

### 2. Run Keyword Research Script

Load {pipelineScriptsData} for the keyword-research.py CLI reference.

Resolve the output path: `{project_folder}/{project-slug}/creative-director/thumbnails/keyword-research.md`

Check if a content brief exists for the `--brief` flag.

Execute:
```bash
python scripts/keyword-research.py \
    --seeds "{comma-separated seeds}" \
    --output "{project_folder}/{project-slug}/creative-director/thumbnails/keyword-research.md" \
    [--brief "{content-brief-path}"]
```

### 3. Present Results

Load the keyword research report from the output path.

Present the key findings:

"**Keyword Research Results:**

**Layers Active:** {N}/3

**HIGH-SIGNAL Keywords** (appearing in 2+ layers — priority for title wording):
{list of high-signal keywords}

**RISING / BREAKOUT Terms** (trending opportunities):
{list of rising terms}

**Competitor Tags** (what successful videos use):
{top 10 competitor tags}

**Suggested SEO Tags** (for YouTube description):
{list of suggested tags}"

### 4. Select Keywords for Title Integration

"**Which keywords should I integrate into the titles?**

Select HIGH-SIGNAL and RISING terms that fit naturally with your angles. Don't force keywords that break the hook.

Type the keywords to use (comma-separated), or type `all-high` for all high-signal keywords, or `skip` to proceed without keyword integration."

Wait for user selection. Store selected keywords for step 04.

### 4b. AUTO MODE — Keyword Selection

**Only execute this section if `{workflow_mode}` is `auto`. Skip entirely in collab mode.**

Auto-select ALL high-signal keywords (appearing in 2+ layers) plus ALL rising/breakout terms. Log the selection:

"**Auto-selected keywords:**
- **High-signal ({count}):** {comma-separated list}
- **Rising/breakout ({count}):** {comma-separated list}

**Auto-proceeding to title generation...**"

Skip the [A]/[P]/[C] menu and auto-proceed to {nextStepFile}.

### 5. Handle Script Failure

If the keyword research script fails or all layers return empty:

"**Keyword research returned no results.** This doesn't block us — we can still draft strong titles from the content analysis. We'll use content-derived terms for SEO tags instead.

Proceeding to title generation..."

### 6. Present MENU OPTIONS

Display: **Select an Option:** [A] Advanced Elicitation [P] Party Mode [C] Continue to Title Generation

#### Menu Handling Logic:

- IF A: Execute {advancedElicitationTask}, and when finished redisplay the menu
- IF P: Execute {partyModeWorkflow}, and when finished redisplay the menu
- IF C: Load, read entire file, then execute {nextStepFile}
- IF Any other: help user respond, then redisplay menu

#### EXECUTION RULES:

- ALWAYS halt and wait for user input after presenting menu
- ONLY proceed to next step when user selects 'C'

## CRITICAL STEP COMPLETION NOTE

ONLY WHEN [C continue option] is selected and [keyword selection made or skipped], will you load and read fully `{nextStepFile}` to begin title generation.

---

## 🚨 SYSTEM SUCCESS/FAILURE METRICS

### ✅ SUCCESS:

- Seeds extracted and confirmed with user
- Script executed (success or graceful failure)
- Results presented with high-signal, rising, and competitor data
- User selected keywords for title integration (or chose to skip)

### ❌ SYSTEM FAILURE:

- Not presenting seed keywords for user confirmation
- Script failure blocking the entire workflow (should be non-blocking)
- Writing titles in this step
- Not giving user the option to select specific keywords

**Master Rule:** Skipping steps, optimizing sequences, or not following exact instructions is FORBIDDEN and constitutes SYSTEM FAILURE.
