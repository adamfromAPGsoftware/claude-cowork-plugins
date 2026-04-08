---
name: 'step-04-text-placement'
description: 'Plan caption positions per section, density rules, assign Remotion templates'

nextStepFile: './step-05-timeline-assembly.md'
outputFile: '{project_folder}/{project-slug}/video-editor/storyboard/{video-id}-storyboard.md'
dataFile: '../data/template-library.md'
---

# Step 4: Text Placement Strategy

## STEP GOAL:

Plan caption and text overlay positions for each section, applying density rules (intro: high density, body: standard), and assign Remotion templates from the template library. This determines how text appears on screen relative to speaker position.

## MANDATORY EXECUTION RULES (READ FIRST):

### Universal Rules:

- NEVER generate content without user input
- CRITICAL: Read the complete step file before taking any action
- CRITICAL: When loading next step with 'C', ensure entire file is read
- YOU MUST ALWAYS SPEAK OUTPUT in your Agent communication style with the config `{communication_language}`

### Step-Specific Rules:

- Load template library from {dataFile} before making assignments
- Use speaker position map from step 3 to avoid text overlapping speaker
- Brief user review — then proceed on [C]

## EXECUTION PROTOCOLS:

- 🎯 Load template library, assign templates and caption positions per section using speaker position data
- 💾 Append text placement strategy to {outputFile} on [C] Continue — update stepsCompleted
- 📖 Load {dataFile} before any template assignments

## CONTEXT BOUNDARIES:

- Available context: Speaker position map (step 3), production brief sections, template library
- Focus: Template and caption position assignments only
- Limits: Do NOT build the timeline in this step — that is step 5
- Dependencies: Speaker position map must exist for accurate caption placement

## MANDATORY SEQUENCE

### 1. Load Template Library

Load and read {dataFile} to understand available Remotion templates:
- `PowerCaption` — Word-by-word keyword burst captions (primary caption template for ALL speaker segments)
- `BRollOverlay` — B-roll with text overlay
- `SubtleZoom` — Slow zoom on speaker with caption
- `SocialProofStack` — Statistics/testimonials display

For each template, note: props, visual event contribution, recommended section types.

### 2. Plan Caption Positions per Section

For each section from the production brief:

**Intro sections (high density):**
- PowerCaption for ALL speaker caption segments — 2–3 keyword bursts per section with a highlight word and word-by-word timing sourced from the transcript
- Position: opposite side of speaker (use speaker position map)
- Density: 2–3 bursts per section; targeting keyword phrases not every line of dialogue

**Body sections (standard density):**
- PowerCaption for key phrases and emphasis moments — 2–3 bursts per section
- Position: bottom-center (standard subtitle position) unless speaker position conflicts
- Density: Burst on emphasized points only, not every sentence

**Chapter transitions:**
- Full-screen text card (template: chapter card)
- Duration: 2-3 seconds

Note: Caption positions determined by speaker position map as before — place captions on the opposite side of the speaker.

### 3. Social Proof Check (Run BEFORE Template Assignment)

Before assigning any template, scan the script for social proof content in each section:

- **Trigger signals:** Upwork stats, agency revenue, project counts, platform credentials (Top Rated, Expert Vetted), personal authority numbers.
- **Rule:** If a segment's script references social proof, assign `UpworkProfile` (or another branded template) as the primary template — **do NOT generate a Hera motion graphic for this content**.
- **Rationale:** Branded templates show real, recognisable assets (actual profile screenshot) which build more credibility than a generated graphic. See template-library for the full Social Proof Priority Rule.

### 4. Assign Templates to Sections

For each section, assign primary and secondary templates:

```markdown
## Text Placement Strategy

### Section Template Assignments

| Section | Primary Template | Secondary Template | Caption Position | Density |
|---------|-----------------|-------------------|-----------------|---------|
| Hook | PowerCaption | — | Bottom-left | High |
| Intro-1 | PowerCaption | BRollOverlay | Bottom-right | High |
| Body-1 | PowerCaption | BRollOverlay | Bottom-center | Standard |
...

### Caption Position Rules

- **Speaker left:** Captions placed right
- **Speaker center:** Captions placed bottom-center
- **Speaker not visible:** Captions placed bottom-center
- **B-roll segments:** Use BRollOverlay template or no captions

### Density Rules Applied

- **Hook:** 2–3 PowerCaption keyword bursts (word-by-word reveal)
- **Intro sections:** 2–3 PowerCaption bursts per section, targeting key phrases
- **Body sections:** 2–3 PowerCaption bursts per section on emphasized points only
- **Chapter transitions:** Title card, no speech captions
```

### PowerCaption Burst Planning Rules

When assigning PowerCaption to a section, plan the bursts as follows:
1. **Identify 2–3 keyword phrases** from the script that carry the highest information value for that section
2. **Each burst:** 2–4 ALL CAPS words, with one word designated as the orange highlight (`highlight` prop)
3. **Burst timing:** `startFrame` and `wordOffsets` are sourced from transcript word timestamps in step 5 (caption timing verification) — record the planned phrases in the segment's `notes` field now; exact frame values are computed in step 5
4. **Avoid full dialogue coverage** — PowerCaption is for keyword emphasis, not continuous subtitles

### 5. Present for Brief Review

"**Text Placement Strategy**

{Display the section template assignments table}

Caption positions are based on speaker position map from step 3.

**[C] Continue** — Accept and proceed to timeline assembly

#### Menu Handling Logic:
- IF C: Append text placement strategy to {outputFile}, update frontmatter `stepsCompleted`, then load, read entire file, then execute {nextStepFile}
- IF Any other: Discuss changes, apply, then redisplay [C] Continue

#### EXECUTION RULES:
- ALWAYS halt and wait for user input after presenting menu
- ONLY proceed to next step when user selects 'C'"

---

## SYSTEM SUCCESS/FAILURE METRICS

### SUCCESS:

- Template library loaded and understood
- Caption positions assigned per section using speaker position data
- Density rules applied (intro high, body standard)
- Templates assigned to each section
- Strategy appended to storyboard

### FAILURE:

- Not loading template library before making assignments
- Ignoring speaker position map for caption placement
- Building timeline in this step (that's step 5)
- Assigning a Hera motion graphic to a social proof segment when a branded template (UpworkProfile) is available
