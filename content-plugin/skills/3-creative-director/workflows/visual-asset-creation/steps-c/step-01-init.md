---
name: 'step-01-init'
description: 'Initialize visual asset creation — load config, brand tokens, and project context'

nextStepFile: './step-02-select.md'
brandConfigData: '../data/brand-config.md'
---

# Step 1: Initialize

## STEP GOAL:

To load CCS configuration, brand design tokens, and resolve project context so the workflow has everything it needs to generate visual assets in the correct locations with consistent branding.

## MANDATORY EXECUTION RULES (READ FIRST):

### Universal Rules:

- 🛑 NEVER generate content without user input
- 📖 CRITICAL: Read the complete step file before taking any action
- 🔄 CRITICAL: When loading next step with 'C', ensure entire file is read
- 📋 YOU ARE A FACILITATOR, not a content generator
- ✅ YOU MUST ALWAYS SPEAK OUTPUT In your Agent communication style with the config `{communication_language}`
- ⚙️ **TOOL/SUBPROCESS FALLBACK**: If any instruction references a subprocess, subagent, or tool you do not have access to, you MUST still achieve the outcome in your main context thread

### Role Reinforcement:

- ✅ You are a Creative Director and visual asset architect
- ✅ We engage in collaborative dialogue, not command-response
- ✅ You bring visual design expertise, composition knowledge, and platform-specific visual psychology
- ✅ The user brings their content vision, brand knowledge, and creative direction

### Step-Specific Rules:

- 🎯 Focus ONLY on initialization — loading config and resolving context
- 🚫 FORBIDDEN to start any asset creation in this step
- 💬 Keep this step efficient — load what's needed and move on
- 📋 If project context is already active from the agent session, use it

## EXECUTION PROTOCOLS:

- 🎯 Follow MANDATORY SEQUENCE exactly
- 💾 Store resolved config values as session variables
- 📖 Load brand config for use in all subsequent steps
- 🚫 FORBIDDEN to proceed without resolved output paths

## CONTEXT BOUNDARIES:

- Available: CCS config.yaml (already loaded by workflow.md), agent session state
- Focus: Configuration loading, project context resolution, brand token loading
- Limits: Do not create any assets or interact creatively yet
- Dependencies: CCS config must be loaded by workflow.md before this step

## MANDATORY SEQUENCE

**CRITICAL:** Follow this sequence exactly. Do not skip, reorder, or improvise unless user explicitly requests a change.

### 1. Verify CCS Configuration

Confirm that CCS config variables are available from the workflow.md initialization:
- `{content_output_folder}` — base content output path
- `{project_folder}` — project mode output path
- `{standalone_folder}` — standalone mode output path
- `{user_name}` — user's name
- `{communication_language}` — language for output

If any are missing, load {project-root}/_bmad/ccs/config.yaml and resolve them.

### 2. Load Brand Design Tokens

Load and read {brandConfigData} completely. Store brand tokens for use in subsequent steps:
- Company name and author name
- Colour palette (background, brand green, headline, body, CTA, etc.)
- Typography (Inter font, weights)
- Standard dimensions per asset type

### 3. Verify Reference Photos

Resolve `{reference_photos_folder}` from CCS config and verify the reference photos directory exists with the expected files:
- `adam-hero-front.jpg` (foundation — always loaded first)
- `adam-3quarter-left.jpg`
- `adam-3quarter-right.jpg`
- `adam-smiling.jpg`
- `adam-talking.jpg`

Store the resolved path for use in thumbnail and image generation steps.

If any photos are missing, warn the user: "**Warning:** Expected {count} reference photos but found {actual}. Thumbnail identity preservation may be affected."

### 4. Resolve Project Context

**If a project is already active from the agent session:**
- Use the active project's slug and paths
- Resolve output paths:
  - Thumbnails: `{project_folder}/{project-slug}/creative-director/thumbnails/`
  - Inspiration: `{project_folder}/{project-slug}/creative-director/thumbnails/inspiration/`
  - Logos: `{project_folder}/{project-slug}/creative-director/logos/`
  - Carousels: `{project_folder}/{project-slug}/creative-director/carousels/`
- **Auto-create all subdirectories now** (silent, no user interaction required):
  ```bash
  mkdir -p "{project_folder}/{project-slug}/creative-director/thumbnails/inspiration"
  mkdir -p "{project_folder}/{project-slug}/creative-director/logos"
  mkdir -p "{project_folder}/{project-slug}/creative-director/carousels"
  ```

**If no project is active:**
- Note that output will go to standalone paths or user-specified locations
- The asset creation steps will ask for output path if needed

### 5. Check for Script Generation Output (Optional)

Search for recent script generation output in the active project folder (if in project mode):
- Pattern: `{project_folder}/{project-slug}/copywriter/scripts/script-*.md`
- If found: Check for Thumbnail Concepts section — these can inform thumbnail creation
- If not found: No problem — user will provide creative direction directly

**Present findings:**

"**Visual Asset Creation initialized.**

**Brand:** {company} / {author}
**Reference Photos:** {count} loaded from {reference_photos_folder}
**Project:** {project-slug or 'Standalone mode'}

**Folders ready:**
- Thumbnails → `creative-director/thumbnails/`
- Inspiration → `creative-director/thumbnails/inspiration/`  ← drop inspiration images here before thumbnail step
- Logos → `creative-director/logos/`

{If script output found: 'Found script with thumbnail concepts — I can use these as a starting point if you choose thumbnails.'}

**Proceeding to asset type selection...**"

### 6. Auto-Proceed to Asset Selection

Display: "**Proceeding to asset type selection...**"

#### Menu Handling Logic:

- After initialization is complete, immediately load, read entire file, then execute {nextStepFile}

#### EXECUTION RULES:

- This is an initialization step with no user choices
- Proceed directly to next step after setup

## CRITICAL STEP COMPLETION NOTE

ONLY WHEN configuration is loaded, brand tokens are stored, and project context is resolved, will you load and read fully `{nextStepFile}` to execute asset type selection.

---

## 🚨 SYSTEM SUCCESS/FAILURE METRICS

### ✅ SUCCESS:

- CCS config variables resolved
- Brand design tokens loaded from {brandConfigData}
- Reference photos verified and path stored
- Project context resolved (project mode or standalone)
- Output paths determined (thumbnails, inspiration, logos, carousels)
- Subdirectories auto-created silently (thumbnails/inspiration, logos, carousels)
- Folder summary presented to user in init output
- Optional script generation output checked
- Auto-proceeded to step 02

### ❌ SYSTEM FAILURE:

- Not loading brand config
- Not verifying reference photos
- Not resolving output paths
- Starting asset creation in this step
- Blocking on user input when this should auto-proceed
- Not checking for prior script generation output

**Master Rule:** Skipping steps, optimizing sequences, or not following exact instructions is FORBIDDEN and constitutes SYSTEM FAILURE.
