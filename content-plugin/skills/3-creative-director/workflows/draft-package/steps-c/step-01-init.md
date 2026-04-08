---
name: 'step-01-init'
description: 'Initialize draft package — verify project, load brand config, check content inputs'

nextStepFile: './step-02-content-analysis.md'
brandConfigData: '../../visual-asset-creation/data/brand-config.md'
ctrChecklistData: '../../visual-asset-creation/data/ctr-checklist.md'
promptTemplateData: '../../visual-asset-creation/data/thumbnail-prompt-template.md'
shortFormGuideData: '../../visual-asset-creation/data/short-form-style-guide.md'
---

# Step 1: Initialize

## STEP GOAL:

To verify an active project is set, load brand design tokens and CTR checklist, resolve content input paths, and report what's available for the draft package.

## MANDATORY EXECUTION RULES (READ FIRST):

### Universal Rules:

- 🛑 NEVER generate content without user input
- 📖 CRITICAL: Read the complete step file before taking any action
- 🔄 CRITICAL: When loading next step with 'C', ensure entire file is read
- 📋 YOU ARE A FACILITATOR, not a content generator
- ✅ YOU MUST ALWAYS SPEAK OUTPUT In your Agent communication style with the config `{communication_language}`
- ⚙️ **TOOL/SUBPROCESS FALLBACK**: If any instruction references a subprocess, subagent, or tool you do not have access to, you MUST still achieve the outcome in your main context thread

### Role Reinforcement:

- ✅ You are a thumbnail strategist preparing a package plan
- ✅ We engage in collaborative dialogue, not command-response
- ✅ You bring CTR psychology, keyword expertise, and composition knowledge
- ✅ The user brings their content vision and creative direction

### Step-Specific Rules:

- 🎯 Focus ONLY on initialization — loading config and checking inputs
- 🚫 FORBIDDEN to start any drafting in this step
- 💬 Keep this step efficient — load what's needed and move on
- 📋 Draft Package REQUIRES an active project — cannot run in standalone mode

## EXECUTION PROTOCOLS:

- 🎯 Follow MANDATORY SEQUENCE exactly
- 💾 Store resolved config values as session variables
- 📖 Load brand config and CTR checklist for use in subsequent steps
- 🚫 FORBIDDEN to proceed without an active project

## MANDATORY SEQUENCE

**CRITICAL:** Follow this sequence exactly. Do not skip, reorder, or improvise unless user explicitly requests a change.

### 1. Verify Active Project

Confirm that `{active_project}` is set and not NONE.

**If NONE:** STOP and inform user: "Draft Package requires an active project. Please run [SP] Switch Project to select or create a project first, then return to [DP]."

### 2. Verify CCS Configuration

Confirm that CCS config variables are available:
- `{content_output_folder}`, `{project_folder}`, `{user_name}`, `{communication_language}`, `{reference_photos_folder}`

Resolve the project path: `{project_folder}/{project-slug}/`

### 3. Load Brand Design Tokens

Load and read {brandConfigData} completely. Store brand tokens for use in subsequent steps.

### 4. Load CTR Checklist

Load and read {ctrChecklistData} completely. Store for CTR pre-validation in step 06.

### 5. Verify Reference Photos

Resolve `{reference_photos_folder}` from CCS config and verify the reference photos directory exists with the expected files. Store the resolved path and file list for the generation config section of the package plan.

### 6. Check Content Inputs

Scan the active project folder for available content that can inform the draft:

**Competitive Research:** `{project_folder}/{project-slug}/strategist/research/competitive-research-*.md`
**Storyboard:** `{project_folder}/{project-slug}/video-editor/storyboard/`
**Transcript/Analysis:** `{project_folder}/{project-slug}/video-editor/analysis/`
**Content Brief:** `{project_folder}/{project-slug}/strategist/research/content-concept-*.md`
**Script Generation:** `{project_folder}/{project-slug}/copywriter/scripts/`
**Inspiration Thumbnails:** `{project_folder}/{project-slug}/creative-director/thumbnails/inspiration/`

For each, note whether it exists and what files are available.

### 7. Check for Existing Package Plan

Check if `{project_folder}/{project-slug}/creative-director/thumbnails/package-plan.md` already exists.

- If it exists AND `{workflow_mode}` is `collab`: warn user "An existing package-plan.md was found. Running this workflow will overwrite it. Proceed?"
- If it exists AND `{workflow_mode}` is `auto`: log warning "Existing package-plan.md found — will be overwritten by auto mode" and proceed without halting
- If not: note clean slate

### 8. Present Findings and Auto-Proceed

"**Draft Package initialized.**

**Project:** {project-slug}
**Mode:** {workflow_mode}
**Reference Photos:** {count} loaded from {reference_photos_folder}
**Content Inputs Available:**
- Competitive Research: {count or 'none'}
- Storyboard: {found/not found}
- Transcript: {found/not found}
- Content Brief: {found/not found}
- Script: {found/not found}
- Inspiration Thumbnails: {count or 'none'}

**Proceeding to content analysis...**"

### 9. Auto-Proceed to Content Analysis

Load, read entire file, then execute {nextStepFile}.

## CRITICAL STEP COMPLETION NOTE

ONLY WHEN initialization is complete and project is verified, will you load and read fully `{nextStepFile}` to begin content analysis.

---

## 🚨 SYSTEM SUCCESS/FAILURE METRICS

### ✅ SUCCESS:

- Active project verified
- CCS config loaded
- Brand tokens and CTR checklist loaded
- Reference photos verified
- Content inputs scanned and reported
- Auto-proceeded to step 02

### ❌ SYSTEM FAILURE:

- Proceeding without active project
- Not loading brand config or CTR checklist
- Not checking available content inputs
- Starting drafting work in this step

**Master Rule:** Skipping steps, optimizing sequences, or not following exact instructions is FORBIDDEN and constitutes SYSTEM FAILURE.
