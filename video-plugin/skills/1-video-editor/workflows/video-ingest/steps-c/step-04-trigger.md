---
name: 'step-04-trigger'
description: 'Trigger Audio Analysis pipeline for each registered video and report completion'
---

# Step 4: Trigger Analysis Pipeline

## STEP GOAL:

To trigger the Audio Analysis workflow for each registered video in the correct processing order (body first, then intro, then outro) and report pipeline status on completion.

## MANDATORY EXECUTION RULES (READ FIRST):

### Universal Rules:

- 🛑 NEVER trigger pipeline for unregistered or unconfirmed files
- 📖 CRITICAL: Read the complete step file before taking any action
- ⚙️ TOOL/SUBPROCESS FALLBACK: If any instruction references a subprocess, subagent, or tool you do not have access to, you MUST still achieve the outcome in your main context thread
- ✅ YOU MUST ALWAYS SPEAK OUTPUT In your Agent communication style with the config `{communication_language}`

### Role Reinforcement:

- ✅ You are a video pipeline operator executing confirmed pipeline triggers
- ✅ Communication style: concise, status-report, mechanical and factual
- ✅ Report each trigger action and its result

### Step-Specific Rules:

- 🎯 Focus ONLY on triggering the Audio Analysis workflow in correct order
- 🚫 FORBIDDEN to re-register or modify YAML files at this stage
- 💬 Report each trigger action as it happens
- 📋 This is the FINAL step — no next step after this

## EXECUTION PROTOCOLS:

- 🎯 Follow the MANDATORY SEQUENCE exactly
- 💾 Update each video's YAML status from 'registered' to 'pipeline_triggered'
- 📖 Report completion summary when all triggers are fired
- 🚫 FORBIDDEN to skip any confirmed video in the trigger sequence

## CONTEXT BOUNDARIES:

- Available context: Confirmed registration data from step 3
- Focus: Pipeline triggering and status reporting only
- Limits: Only trigger Audio Analysis — do NOT trigger downstream workflows (Transcription, Visual Analysis, etc.)
- Dependencies: Step 3 must have completed with user confirmation

## MANDATORY SEQUENCE

**CRITICAL:** Follow this sequence exactly. Do not skip, reorder, or improvise unless user explicitly requests a change.

### 1. Prepare Trigger Queue

Build the trigger queue from confirmed registrations:

**Order rules:**
1. Process projects in the order they were registered
2. Within each project, follow processing order: Body (1) → Intro (2) → Outro (3)
3. For each file, trigger the PROXY version for analysis (Audio Analysis, Transcription, Visual Analysis) — proxy files are smaller and faster for API calls. Raw files are reserved for final cut application only. If no proxy exists for a file, fall back to the raw version.

"**Trigger queue prepared.**

| # | Project | File | Type | Order |
|---|---------|------|------|-------|
| 1 | {project} | {filename} | Body | 1 |
| 2 | {project} | {filename} | Intro | 2 |
{...}

**Triggering Audio Analysis pipeline...**"

### 2. Trigger Audio Analysis for Each Video

For each video in the trigger queue:

1. **Update YAML status** — Set `status: 'pipeline_triggered'` and `triggered_at: '{timestamp}'`
2. **Trigger Audio Analysis workflow** — Invoke the Audio Analysis workflow with the video's metadata YAML path
3. **Report result:**

"**[{queue-position}/{total}]** Triggered Audio Analysis for `{filename}` ({content-type}) — {success/failed}"

**If a trigger fails:**
- Log the failure in the video's YAML: `status: 'trigger_failed'`, `error: '{reason}'`
- Report the failure but continue with remaining videos
- Do NOT halt the entire queue for a single failure

### 3. Report Completion Summary

"**Pipeline Trigger Complete.**

---

**Results:**
- **Total triggered:** {success-count}/{total-count}
- **Successful:** {success-count}
- **Failed:** {fail-count}

{If failures:}
**Failed triggers:**
| # | File | Error |
|---|------|-------|
| 1 | {filename} | {error-reason} |

---

**Next in pipeline:** Audio Analysis → Transcription → Visual Analysis → Video Clipping

**Recommended next step:** Monitor Audio Analysis progress for project `{project-name}`.

---

**Video Ingest workflow complete.**"

### 4. End Workflow

This is the final step. No further steps to load.

The workflow is complete when all triggers have been fired and the completion summary has been reported.

---

## 🚨 SYSTEM SUCCESS/FAILURE METRICS

### ✅ SUCCESS:

- Trigger queue built in correct processing order (body first)
- Audio Analysis triggered for each confirmed RAW video
- YAML status updated to 'pipeline_triggered' for each triggered video
- Failed triggers logged but did not halt the queue
- Completion summary reported with success/failure counts
- Workflow ended gracefully

### ❌ SYSTEM FAILURE:

- Triggering pipeline for unconfirmed files
- Wrong processing order (intro before body)
- Triggering raw files instead of proxy files for analysis
- Halting entire queue due to single failure
- Not updating YAML status after trigger
- Not reporting completion summary

**Master Rule:** Skipping steps, optimizing sequences, or not following exact instructions is FORBIDDEN and constitutes SYSTEM FAILURE.
