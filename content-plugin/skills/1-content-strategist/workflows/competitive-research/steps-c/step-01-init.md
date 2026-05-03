---
name: 'step-01-init'
description: 'Load sidecar config, detect project context, and select research mode'

trendStepFile: './step-02a-trend-scan.md'
validationStepFile: './step-02b-idea-search.md'
outputFile: '{output_path}/competitive-research-{date}.md'
templateFile: '../templates/report-template.md'
sidecarFile: '../sidecar/config.yaml'
---

# Step 1: Initialization & Mode Selection

## STEP GOAL:

To load persistent configuration (niche scope, competitor channels), detect the active project context for output routing, and present the user with a mode selection — Trend Discovery or Idea Validation — before routing to the appropriate next step.

## MANDATORY EXECUTION RULES (READ FIRST):

### Universal Rules:

- 🛑 NEVER generate content without user input
- 📖 CRITICAL: Read the complete step file before taking any action
- 🔄 CRITICAL: When loading next step with 'C', ensure entire file is read
- 📋 YOU ARE A FACILITATOR, not a content generator
- ✅ YOU MUST ALWAYS SPEAK OUTPUT in your Agent communication style with the config `{communication_language}`
- ⚙️ TOOL/SUBPROCESS FALLBACK: If any instruction references a subprocess, subagent, or tool you do not have access to, you MUST still achieve the outcome in your main context thread

### Role Reinforcement:

- ✅ You are a competitive intelligence analyst and YouTube content strategist
- ✅ If you already have been given a name, communication_style, and identity, continue to use those while playing this new role
- ✅ You bring expertise in data analysis, trend identification, and competitive positioning
- ✅ The user brings their domain knowledge, creative vision, and channel context

### Step-Specific Rules:

- 🎯 Focus ONLY on loading config, detecting project, and getting mode selection
- 🚫 FORBIDDEN to start any data gathering or analysis in this step
- 💬 Be concise — this is setup, not exploration
- 📋 Validate sidecar has at least one competitor configured before proceeding

## EXECUTION PROTOCOLS:

- 🎯 Follow the MANDATORY SEQUENCE exactly
- 💾 Create the output report file from template
- 📖 Update output frontmatter with init context
- 🚫 FORBIDDEN to load next step until mode is selected

## CONTEXT BOUNDARIES:

- Available: CCS module config (loaded by workflow.md), sidecar config
- Focus: Configuration loading and mode selection only
- Limits: No data gathering, no analysis, no YouTube API calls
- Dependencies: CCS config must be loaded, sidecar must exist

## MANDATORY SEQUENCE

**CRITICAL:** Follow this sequence exactly. Do not skip, reorder, or improvise unless user explicitly requests a change.

### 1. Validate MCP Connectivity

Confirm that the YouTube MCP is available by calling `mcp__youtube__searchVideos` with a test query. The YouTube MCP is a platform-level MCP — no API key or `.env` entry is needed.

**If YouTube MCP is unavailable:**

"**YouTube MCP not connected.** Check your Claude Code MCP settings and ensure the YouTube MCP server is enabled."

STOP — do not proceed.

### 2. Load Sidecar Configuration

Load and read {sidecarFile}. Extract and store:

- `niche` — the content space to analyse
- `competitors` — list of channels with names and IDs
- `defaults` — timeframe_days, min_outlier_score, max_transcripts, video_limit_per_channel

**Soft validation:** If `niche_scan.keywords` is empty or `niche_scan.enabled` is false, display a warning (but do NOT block):

"**Note:** Niche-wide keyword scanning is disabled or has no keywords configured. The workflow will skip niche scanning. To enable, update `sidecar/config.yaml`."

**Validate:** At least one competitor must have a non-empty `channel_id`. If none are configured, inform the user:

"Your competitor list is empty. Please update `sidecar/config.yaml` with at least one competitor channel before running this workflow."

Then STOP — do not proceed.

### 3. Detect Project Context

Check the active project context from the CCS module:

- Load `{project_folder}/_index.yaml` if it exists
- Check for `last_active_project` in the Content Strategist sidecar memory
- If an active project exists: set `output_path` to `{project_folder}/{project-slug}/strategist/research/`
- If no active project: set `output_path` to `{standalone_folder}/{date}-competitive-research/`

Display the detected context:

"**Competitive Research — Ready**

**Niche:** {niche}
**Competitors:** {list competitor names}
**Project:** {project name or 'Standalone mode'}
**Output:** {output_path}"

### 4. Create Output Report

Create the output report file from {templateFile} at {outputFile}.

Populate frontmatter with:
- `date`: current date
- `user_name`: from config
- `niche`: from sidecar
- `project_slug`: from project context (or 'standalone')

### 5. Present Mode Selection

"**Select your research mode:**

**[T] Trend Discovery** — Scan competitor channels + niche-wide keyword trends for outlier videos, trending topics, and content gaps
**[V] Idea Validation** — Evaluate a specific video idea against the current competitive landscape

Select: [T] / [V]"

### 6. Present MENU OPTIONS

#### Menu Handling Logic:

- IF T: Update output frontmatter with `mode: 'trend-discovery'` and `stepsCompleted: ['step-01-init']`, then load, read entire file, then execute {trendStepFile}
- IF V: Ask user "**What's your video idea?** Describe the topic, angle, or title you're considering." Store the response, update output frontmatter with `mode: 'idea-validation'`, `videoIdea: [user's idea]`, and `stepsCompleted: ['step-01-init']`, then load, read entire file, then execute {validationStepFile}
- IF Any other: help user respond then redisplay mode selection

#### EXECUTION RULES:

- ALWAYS halt and wait for user input after presenting mode selection
- Branching options load different steps based on user choice
- If user selects V, gather their video idea BEFORE proceeding

## CRITICAL STEP COMPLETION NOTE

ONLY WHEN the user selects T or V (and provides their video idea if V) will you update the output file and load the appropriate next step file.

---

## 🚨 SYSTEM SUCCESS/FAILURE METRICS

### ✅ SUCCESS:

- YouTube MCP connectivity validated
- Sidecar config loaded with valid competitors
- Project context detected and output path resolved
- Output report file created from template
- User selected mode (T or V)
- Video idea captured (if validation mode)
- Correct next step file loaded based on mode

### ❌ SYSTEM FAILURE:

- Proceeding without validating YouTube MCP connectivity
- Proceeding without valid competitors in sidecar
- Not detecting project context
- Not creating the output report file
- Loading the wrong next step for the selected mode
- Starting data gathering or analysis in this step

**Master Rule:** Skipping steps, optimizing sequences, or not following exact instructions is FORBIDDEN and constitutes SYSTEM FAILURE.
