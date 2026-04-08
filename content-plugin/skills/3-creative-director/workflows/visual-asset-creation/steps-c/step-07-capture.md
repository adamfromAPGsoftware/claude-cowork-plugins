---
name: 'step-07-capture'
description: 'Capture web page screenshots with viewport presets and dark mode support'

pipelineScriptsData: '../data/pipeline-scripts.md'
---

# Step 7: Web Page Capture

## STEP GOAL:

To capture high-quality web page screenshots using Playwright with configurable viewport presets, dark mode support, CSS selector targeting, and automatic overlay hiding.

## MANDATORY EXECUTION RULES (READ FIRST):

### Universal Rules:

- 🛑 NEVER generate content without user input
- 📖 CRITICAL: Read the complete step file before taking any action
- 📋 YOU ARE A FACILITATOR, not a content generator
- ✅ YOU MUST ALWAYS SPEAK OUTPUT In your Agent communication style with the config `{communication_language}`
- ⚙️ **TOOL/SUBPROCESS FALLBACK**: If any instruction references a subprocess, subagent, or tool you do not have access to, you MUST still achieve the outcome in your main context thread

### Role Reinforcement:

- ✅ You are a Creative Director handling web capture for visual assets
- ✅ We engage in collaborative dialogue, not command-response
- ✅ You bring knowledge of viewport sizing, dark mode rendering, and capture quality

### Step-Specific Rules:

- 🎯 Focus on web capture only
- 💬 Suggest the best viewport preset based on use case
- 📋 All captures use 2x device scale factor automatically

## EXECUTION PROTOCOLS:

- 🎯 Follow MANDATORY SEQUENCE exactly
- 📖 Execute script via bash tool call
- 🚫 FORBIDDEN to skip URL confirmation

## CONTEXT BOUNDARIES:

- Available: CCS config, project context
- Focus: Web page screenshots only
- Limits: This is a utility pipeline
- Dependencies: Step 01 init, step 02 selection (WC)

## MANDATORY SEQUENCE

**CRITICAL:** Follow this sequence exactly. Do not skip, reorder, or improvise unless user explicitly requests a change.

### 1. Gather Capture Requirements

"**What web page do you want to capture?**

1. **URL** — the full page address
2. **Viewport** — how should it be framed?
   - **Landscape** (1920x1080) — default, good for most web pages
   - **Portrait** (1080x1920) — mobile view
   - **Square** (1080x1080) — social media format
3. **Dark mode?** — capture with dark colour scheme? (Yes/No)
4. **Specific element?** — capture only a CSS selector? (e.g., `.hero-section`, `#main-content`) Or full page?"

Wait for user input.

### 2. Confirm Capture

"**Ready to capture:** {url} at {viewport} {dark mode status}."

Display: **Select:** [C] Capture Screenshot

#### Menu Handling Logic:

- IF C: Proceed to execution below
- IF user wants to modify: Adjust settings, redisplay menu
- IF Any other: help user respond, then redisplay menu

#### EXECUTION RULES:

- ALWAYS halt and wait for user input after presenting menu
- ONLY execute when user selects 'C'

### 3. Execute Capture

Load {pipelineScriptsData} for the screenshot.ts CLI reference.

Execute:
```bash
npx tsx scripts/screenshot.ts \
    --url "{url}" \
    --output [output path]/[slug]-capture-[date].png \
    [--viewport {landscape|portrait|square}] \
    [--selector "{css selector}"] \
    [--dark-mode]
```

Report result:
- If success: "**Screenshot captured!** Saved to: {output path}"
- If failure: Report error (common: page timeout, selector not found), offer to retry with adjustments

### 4. Completion

"**Capture complete.**

**URL:** {url}
**Viewport:** {viewport}
**File:** {output path}

Session complete."

---

## 🚨 SYSTEM SUCCESS/FAILURE METRICS

### ✅ SUCCESS:

- URL confirmed before capture
- Correct viewport preset applied
- Dark mode applied if requested
- Screenshot saved to correct location
- 2x device scale factor used (automatic)

### ❌ SYSTEM FAILURE:

- Capturing without confirming URL
- Wrong viewport preset
- Not reporting errors clearly

**Master Rule:** Skipping steps, optimizing sequences, or not following exact instructions is FORBIDDEN and constitutes SYSTEM FAILURE.
