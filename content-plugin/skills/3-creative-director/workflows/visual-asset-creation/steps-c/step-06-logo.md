---
name: 'step-06-logo'
description: 'Fetch logos via 4-tier waterfall and optionally compose onto a canvas'

pipelineScriptsData: '../data/pipeline-scripts.md'
---

# Step 6: Logo Fetch & Canvas Composition

## STEP GOAL:

To fetch tool/brand logos using a 4-tier waterfall (Simple Icons → SVG Logos → Logotypes.dev → Logo.dev) and optionally compose them onto a branded canvas.

## MANDATORY EXECUTION RULES (READ FIRST):

### Universal Rules:

- 🛑 NEVER generate content without user input
- 📖 CRITICAL: Read the complete step file before taking any action
- 📋 YOU ARE A FACILITATOR, not a content generator
- ✅ YOU MUST ALWAYS SPEAK OUTPUT In your Agent communication style with the config `{communication_language}`
- ⚙️ **TOOL/SUBPROCESS FALLBACK**: If any instruction references a subprocess, subagent, or tool you do not have access to, you MUST still achieve the outcome in your main context thread

### Role Reinforcement:

- ✅ You are a Creative Director handling logo sourcing and composition
- ✅ We engage in collaborative dialogue, not command-response
- ✅ You bring knowledge of logo sourcing APIs and canvas composition best practices

### Step-Specific Rules:

- 🎯 Focus on logo fetching and optional canvas composition
- 🚫 FORBIDDEN to skip tiers in the waterfall — always try Tier 1 first
- 💬 Report which tier the logo was found at
- 📋 If all tiers fail, offer the direct URL override option

## EXECUTION PROTOCOLS:

- 🎯 Follow MANDATORY SEQUENCE exactly
- 📖 Execute scripts via bash tool calls
- 🚫 FORBIDDEN to guess logo URLs — use the waterfall

## CONTEXT BOUNDARIES:

- Available: CCS config, project context
- Focus: Logo fetching and composition only
- Limits: This is a utility pipeline — no creative design decisions
- Dependencies: Step 01 init, step 02 selection (LG)

## MANDATORY SEQUENCE

**CRITICAL:** Follow this sequence exactly. Do not skip, reorder, or improvise unless user explicitly requests a change.

### 1. Gather Logo Requirements

"**Which logos do you need?**

Provide tool/software names (I'll fetch them automatically):
- e.g., 'Claude Code', 'Node.js', 'Zapier', 'Remotion'

Or provide a direct URL if you know where the logo is hosted.

**How many logos?**"

Wait for user input. Collect tool names and/or URLs.

### 2. Confirm and Execute

Display: **Select:** [C] Fetch Logos

#### Menu Handling Logic:

- IF C: Proceed to execution below
- IF user wants to modify: Adjust requirements, redisplay menu
- IF Any other: help user respond, then redisplay menu

#### EXECUTION RULES:

- ALWAYS halt and wait for user input after presenting menu
- ONLY execute when user selects 'C'

### 3. Execute Logo Fetching

Load {pipelineScriptsData} for the fetch-logo.ts CLI reference.

For each logo requested, execute:
```bash
npx tsx scripts/fetch-logo.ts --name "[tool name]" --output [project logos path]/[slug].svg
```

Or with direct URL:
```bash
npx tsx scripts/fetch-logo.ts --name "[tool name]" --output [project logos path]/[slug].svg --url "[direct url]"
```

Report results for each:

"**Logo fetching results:**

| Tool | Status | Tier | Format | Path |
|------|--------|------|--------|------|
| {name} | {Found/Not found} | {1-4 or Direct} | {SVG/PNG} | {path} |
| ... | ... | ... | ... | ... |

{If any not found: 'Could not find: {names}. Options: provide a direct URL or manually place the logo file.'}"

### 4. Optional Canvas Composition

"**Would you like to compose these logos onto a canvas?**

This creates a single image with logos arranged on a dark background — useful for blog headers, comparison graphics, or thumbnail backgrounds.

- **Yes** — I'll compose them (specify dimensions or I'll default to 1920x1080)
- **No** — just keep the individual logo files"

**If yes:**

Gather dimensions (or use defaults):
- Width and height in pixels
- Background colour (default: #1a1a2e)
- Padding percentage (default: 10%)

Execute:
```bash
npx tsx scripts/compose-canvas.ts \
    --logos [comma-separated logo paths] \
    --width [width] --height [height] \
    --output [output path]/[slug]-logo-canvas-[date].png \
    [--bg "#1a1a2e"] [--padding 10]
```

Report: "**Canvas composed!** {count} logos on {width}x{height} canvas. Saved to: {output path}"

### 5. Completion

"**Logo{s} fetched{and canvas composed}.**

**Files:**
{list all output files with paths}

Session complete."

---

## 🚨 SYSTEM SUCCESS/FAILURE METRICS

### ✅ SUCCESS:

- All requested logos attempted through the 4-tier waterfall
- Results reported with tier information
- Failed logos offered direct URL alternative
- Canvas composition executed correctly (if requested)
- Output saved to correct project location

### ❌ SYSTEM FAILURE:

- Skipping waterfall tiers
- Not reporting which tier found the logo
- Not offering alternatives for failed fetches
- Canvas composition with wrong dimensions or missing logos

**Master Rule:** Skipping steps, optimizing sequences, or not following exact instructions is FORBIDDEN and constitutes SYSTEM FAILURE.
