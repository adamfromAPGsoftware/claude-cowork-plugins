---
name: analyse-content
description: Ingest video content and extract thumbnail angles, hooks, and visual direction
web_bundle: true
---

# Analyse Content

**Goal:** Ingest available project content (storyboard, transcript, content brief, script) and extract the strongest thumbnail angles, visual hooks, emotional peaks, and curiosity gap opportunities — without committing to the full Draft Package pipeline.

**Your Role:** You are a content analyst partnering with the user to identify the most compelling thumbnail-worthy moments. You bring expertise in visual hooks, transformation moments, and curiosity gaps. The user brings their knowledge of what the content is really about.

**Meta-Context:** This is a standalone analysis step. Its output (`content-analysis.md`) can feed into [DP] Draft Package or [VA] Visual Assets, or be used as a reference for from-scratch thumbnail generation.

---

## WORKFLOW ARCHITECTURE

This is a single-file workflow — no step files needed. Follow the mandatory sequence below.

### Critical Rules (NO EXCEPTIONS)

- 🛑 NEVER generate titles or prompts — that happens in [DP] or [VA]
- 📖 Focus on extracting angles and hooks, not on composition or generation
- 💬 Present findings clearly and ask user to select/modify angles
- ✅ Communicate in your Agent communication style with `{communication_language}`

---

## INITIALIZATION SEQUENCE

### 1. Module Configuration Loading

Load and read full config from `{project-root}/config.yaml`:
- `user_name`, `communication_language`, `output_folder`
- `content_output_folder`, `project_folder`, `standalone_folder`

### 2. Project Verification

Verify `{active_project}` is set and not NONE. If NONE:
"**An active project is required for content analysis.** Run [SP] Switch Project to select or create a project first."
STOP.

---

## MANDATORY SEQUENCE

### 1. Discover Content Inputs

Scan the active project folder for available content:

**Check these locations (in priority order):**
1. `{project_folder}/{project-slug}/copywriter/scripts/` — Script drafts (contain thumbnail concepts section)
2. `{project_folder}/{project-slug}/video-editor/analysis/` — Storyboard, visual analysis, transcripts
3. `{project_folder}/{project-slug}/video-editor/clips/` — Clip metadata
4. `{project_folder}/{project-slug}/video-ingest/` — Raw video ingest outputs (transcripts, analysis)

**Report what was found:**

"**Content Discovery for {project-slug}:**

| Source | Status | Location |
|--------|--------|----------|
| Script | {found/not found} | {path or —} |
| Storyboard | {found/not found} | {path or —} |
| Transcript | {found/not found} | {path or —} |
| Visual Analysis | {found/not found} | {path or —} |
| Content Brief | {found/not found} | {path or —} |

{N} content sources available for analysis."

### 2. Load and Analyse Content

**If content inputs exist:**

Load content inputs in priority order:
1. **Content brief** (if available) — has the target audience, angles, positioning
2. **Script** (if available) — has the narrative hooks and thumbnail concepts
3. **Storyboard** (if available) — has visual scene breakdowns
4. **Transcript** (if available) — has the raw spoken content

**Summarize, don't dump.** Extract key sections rather than loading full transcripts into context:
- From content brief: logline, target audience, hooks, angles
- From script: thumbnail concepts section (if present), key hooks, transformation claims
- From storyboard: key visual scenes, emotional peaks
- From transcript: strongest quotes, topic transitions, "aha" moments

**If NO content inputs available — switch to manual mode:**

"**No content inputs found in this project.** Let's build the angles from scratch.

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

**For each angle, extract:**
- **Angle name** — short descriptive label (e.g., "Shocked by results", "Tool comparison", "Before/After")
- **Hook** — the curiosity gap or emotional trigger
- **Expression suggestion** — what face/emotion matches this angle
- **Text overlay idea** — the short punchy text that could appear on the thumbnail (<12 characters)
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

**Select which angles to develop further:**
- Type numbers (e.g., `1,2,4`) to select specific angles
- Type `all` to use all angles
- Or describe a new angle to add"

Wait for user selection.

### 5. Save Analysis

Save the selected angles to `{project_folder}/{project-slug}/creative-director/thumbnails/content-analysis.md`:

```markdown
---
project: {project-slug}
date: {date}
sources: [{list of content sources used}]
---

# Content Analysis — Thumbnail Angles

## Selected Angles

### Angle 1: {angle name}
- **Hook:** {hook}
- **Expression:** {expression}
- **Text Idea:** {text} ({char count} chars)
- **Visual Direction:** {visual}

### Angle 2: ...
{repeat for each selected angle}

## Content Summary
{brief summary of what was analysed}
```

Confirm: "**Analysis saved** to `{output path}`"

### 6. Next Steps

"**What would you like to do next?**

- **[DP]** Draft Package — develop these angles into full title/thumbnail combos with keyword research, CTR pre-validation, and YouTube description
- **[VA]** Visual Assets — jump straight to thumbnail generation using these angles as direction
- **[D]** Done — exit this workflow"

Wait for user selection.

#### Menu Handling Logic:
- IF DP: Load and execute `{project-root}/content-plugin/skills/3-creative-director/workflows/draft-package/workflow.md`
- IF VA: Load and execute `{project-root}/content-plugin/skills/3-creative-director/workflows/visual-asset-creation/workflow.md`
- IF D: End workflow session

---

## SYSTEM SUCCESS/FAILURE METRICS

### SUCCESS:
- Available content discovered and loaded
- 3-5 thumbnail angles extracted with hooks, expressions, text ideas, visual direction
- User selected which angles to develop
- Analysis saved to content-analysis.md
- Next steps offered

### FAILURE:
- Writing titles or prompts in this workflow
- Not presenting angles for user selection
- Proceeding without user selecting angles
- Not saving the analysis to file
