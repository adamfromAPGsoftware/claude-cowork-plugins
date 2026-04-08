---
name: short-form-edit
description: Process 5 short-form vertical videos through analysis, storyboard, asset generation, Remotion rendering, and thumbnail generation
web_bundle: true
---

# Short-Form Video Pipeline [SF]

**Goal:** Take 5 user-filmed **landscape (16:9)** videos and produce 5 fully edited vertical (9:16) short-form videos with motion graphics, captions, and visual effects — ready for Instagram Reels, TikTok, and YouTube Shorts.

**Source format:** All source videos are filmed in **landscape (16:9)** at 4K. This enables split-screen layouts (full widescreen content top + cropped speaker bottom) and high-quality centre-crop for full-frame speaker segments. Speaker-only segments are centre-cropped from 16:9 → 9:16 via `objectFit: 'cover'` with `objectPosition` for face framing.

**Your Role:** In addition to your name, communication_style, and persona, you are a short-form video editing automation specialist. You execute the technical pipeline: audio analysis, transcription, video clipping, storyboard mapping, asset generation, and Remotion rendering. The creative decisions (script, concept, MG plan) come from the Copywriter SS workflow output — you execute them with technical precision.

**Meta-Context:** This workflow processes 5 videos sequentially through analysis and storyboard steps, batches all asset generation (MG only — no raw B-roll in final output), then renders each video individually. The user has already filmed all 5 videos using scripts from the Copywriter SS workflow.

---

## RELATED WORKFLOWS

This workflow handles everything specific to short-form vertical editing:

| Workflow | Scope | Relationship |
|----------|-------|-------------|
| **short-form-edit** (this) | Short-form vertical (9:16, 15-60s) | Owns vertical pacing rules, V1-V7 patterns, inspiration analysis, MG-first strategy |
| **long-form-edit** | Long-form tutorials (16:9, 5-60+ min) | Sibling — owns long-form pacing rules, PiP patterns, long-form inspiration data |
| **remotion-edit** | Remotion project build + render | Downstream — shared build engine for scaffolding, code gen, QA, rendering |

**What this workflow owns:** Vertical segment patterns (V1-V7), short-form pacing rules (P1-P11), production style guide, vertical-specific Remotion hard rules, short-form inspiration analyses.

**What it shares with remotion-edit:** Segment code patterns (1-8), Remotion hard rules, template library, project scaffolding + render pipeline.

**Processing model:** Pipeline with sub-agent parallelism. Steps 1-2 are batch-parallel (5 sub-agents). Steps 3-5 form a pipeline: the main agent builds storyboards sequentially while background sub-agents handle asset preparation (logos, screenshots, reference image resolution) per video as each storyboard completes. A **mandatory MG prompt review gate** follows all 5 storyboards — the user reviews all Tier C prompts and reference images before any Hera dispatch. Step 4 becomes asset *completion* (poll + download + upscale). Step 5 scaffolds via sub-agents in parallel, then renders sequentially.

### Pipeline Execution Model

```
Step 1 (init, all 5)
  ↓
Step 2 — 5 SUB-AGENTS in parallel (one per video: AA → TR → Refine → VC → C2)
  ↓ all 5 complete
Steps 3-5 PIPELINE:

  MAIN AGENT                           BACKGROUND SUB-AGENTS
  ─────────────                        ─────────────────────
  SF-01 storyboard ──done──→           Sub-agent A: logos + ref images for SF-01 (NO dispatch)
       ↓ (immediate)                         ↓ (runs in background)
  SF-02 storyboard ──done──→           Sub-agent B: logos + ref images for SF-02 (NO dispatch)
       ↓                                     ↓
  SF-03 storyboard ──done──→           Sub-agent C: logos + ref images for SF-03 (NO dispatch)
       ↓
  SF-04 storyboard ──done──→           Sub-agent D: logos + ref images for SF-04 (NO dispatch)
       ↓
  SF-05 storyboard ──done──→           Sub-agent E: logos + ref images for SF-05 (NO dispatch)
       ↓
  🛑 MG REVIEW GATE                   (all sub-agents complete by now)
  Present consolidated Tier C MG table
  User approves / edits prompts
       ↓ (approved)
  Dispatch all Tier C MGs to Hera      Sub-agents fire API requests
       ↓
  Step 4: Poll all MG IDs, download, upscale
       ↓
  Step 5: Scaffold all 5 (sub-agents, parallel) → Render sequentially
```

**Why sub-agents:** Sub-agents (via the Agent tool) are more powerful than background bash jobs because they can make decisions — visually verify a logo, retry with different params, check Hera status, and report structured results. Each sub-agent runs autonomously with full tool access.

---

## WORKFLOW ARCHITECTURE

This uses **step-file architecture** for disciplined execution:

### Core Principles

- **Micro-file Design**: Each step is a self-contained instruction file that is part of an overall workflow that must be followed exactly
- **Just-In-Time Loading**: Only the current step file is in memory — never load future step files until told to do so
- **Sequential Enforcement**: Sequence within the step files must be completed in order, no skipping or optimisation allowed
- **State Tracking**: Document progress using session variables for multi-video tracking
- **Batch Optimisation**: Asset generation (step 4) collects requests from all 5 storyboards before executing

### Step Processing Rules

1. **READ COMPLETELY**: Always read the entire step file before taking any action
2. **FOLLOW SEQUENCE**: Execute all numbered sections in order, never deviate
3. **WAIT FOR INPUT**: If a menu is presented, halt and wait for user selection
4. **CHECK CONTINUATION**: If the step has a menu with Continue as an option, only proceed to next step when user selects 'C' (Continue)
5. **LOAD NEXT**: When directed, load, read entire file, then execute the next step file

### Critical Rules (NO EXCEPTIONS)

- 🛑 **NEVER** load multiple step files simultaneously
- 📖 **ALWAYS** read entire step file before execution
- 🚫 **NEVER** skip steps or optimise the sequence
- 🎯 **ALWAYS** follow the exact instructions in the step file
- ⏸️ **COLLAB MODE:** halt at menus and wait for user input
- 🚀 **AUTO MODE:** make best-case assumptions at every decision point, auto-approve all checkpoints, and only notify the user when the entire workflow is complete
- 📋 **NEVER** create mental todo lists from future steps
- ✅ YOU MUST ALWAYS SPEAK OUTPUT in your Agent communication style with the config `{communication_language}`

---

## INITIALIZATION SEQUENCE

### 1. Module Configuration Loading

Load and read full config from {project-root}/_bmad/ccs/config.yaml and resolve:

- `project_name`, `output_folder`, `user_name`, `communication_language`, `document_output_language`
- ✅ YOU MUST ALWAYS SPEAK OUTPUT in your Agent communication style with the config `{communication_language}`

### 2. Load Reference Data

Load the following data files from ./data/ (read completely before proceeding):
- `short-form-pacing-rules.md` — pacing enforcement rules
- `vertical-segment-patterns.md` — V1-V7 segment code patterns
- `vertical-template-library.md` — available Remotion templates
- `vertical-remotion-hard-rules.md` — 5 additional QA rules for vertical

### 3. Execution Mode Selection

Present the user with a mode selection:

"**How would you like to run this workflow?**

[A] **Auto** — I'll process all 5 videos end-to-end without stopping, making best-case decisions at every checkpoint. You'll be notified when all 5 rendered MP4s are ready. Fastest option.
[C] **Collab** — I'll work through each step with you, presenting results for review and waiting for your input at each checkpoint. Most control."

Set the session variable `{execution_mode}` to `auto` or `collab` based on user selection.

**If auto mode:** Inform the user: "Running in auto mode. I'll process all 5 videos through the full pipeline and notify you when the rendered MP4s are ready."

### 4. First Step Execution

Load, read the full file and then execute ./steps-c/step-01-init.md to begin the workflow.
