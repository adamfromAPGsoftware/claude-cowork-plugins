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

Load and read {dataFile} in full before making ANY template assignment. The library contains two distinct groups:

**Caption and overlay templates** (used for speaker segments and transitions):
- `PowerCaption` — Word-by-word keyword burst captions (primary caption template for ALL speaker segments)
- `BRollOverlay` — B-roll with text overlay
- `SubtleZoom` — Slow zoom on speaker with caption
- `SocialProofStack` — Statistics/testimonials display

**Showcase templates — 41 components across 7 categories** (used for MG slots — read ALL of these):
- **Number/Metric:** `NumberCountUp`, `MetricCard`, `StatSplitCard`, `ProgressRing`, `ROICalculator`
- **Text/Statement:** `BoldStatement`, `CinematicReveal`, `FullscreenTitleCard`, `TextRevealMask`, `ParagraphReveal`
- **List/Sequential:** `ChecklistReveal`, `SequentialPillBuild`, `StackedPillsReveal`
- **Concept/Diagram:** `FlowchartAnimation`, `TransformationArrow`, `SVGLineTimeline`, `TimelineStep`
- **Logo/Tool:** `ToolLogoGrid`, `AIPulseIcon`, `GlowingIconPop`
- **Comparison/Proof:** `ComparisonTable`, `BeforeAfterSplit`, `SplitScreenReveal`, `ProofQuote`
- **Additional components** listed in the full template-library.md — read the complete file

**CRITICAL:** You MUST read and consider ALL 41 showcase components before assigning any MG slot. Defaulting to the same 3-4 templates without consulting the full library is a system failure — it produces visually monotonous storyboards and requires manual re-runs to fix.

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

### 4. MG Slot Template Selection Protocol

Before building the section template assignments table, resolve every `[MG-X]` trigger point in the script or Visual Asset Source Map. For each MG slot:

**4a. Classify intent** — label each slot with one of: `number | list | statement | concept | logo | comparison | interface`

**4b. Select showcase candidate** — use the MG Slot Classification → Template Mapping table in the template library to get the ordered candidate list for that intent. Default to the first candidate.

**4c. Apply Reuse Cap gate** — tally how many times each showcase template has already been assigned in this storyboard:
- If the intro cap (2 uses) would be exceeded → reject this candidate; move to the next in the list.
- If the full-video cap (3 uses) would be exceeded → same action.
- If two consecutive MG slots (separated only by a speaker segment) would use the same template → reject; pick the next candidate.
- Body ROI running-total counters (`ROICalculator` / `NumberCountUp`) are **exempt** from the cap — they may repeat once per chapter as a continuous narrative device.

**4d. Hera eligibility check** — if and only if intent is `interface`, check all three eligibility conditions from the template library's "Hera Eligibility Rules" section:
  1. Subject is a named coding tool or AI interface
  2. Motion requires a live UI (zoom, typing, logs, clicking)
  3. A reference image exists or can be obtained

  If all three pass → set `hera: true` in the Visual Asset Source Map row and `visual_type: motion-graphic`.
  If any fails → assign the best showcase template instead.

**4e. Record selection** — update the Visual Asset Source Map row with:
  - `visual_type: showcase-mg` (or `motion-graphic` for approved Hera slots)
  - `template: {ComponentName}` (exact showcase component name, or `MotionGraphic` for Hera)
  - `hera: true/false`
  - `notes:` why cap was triggered (if applicable), why Hera was approved/rejected

Verify that total Hera-approved slots in the intro ≤ 3. If exceeded, demote the least-essential interface slots to showcase templates.

**4f. Prop Content Extraction Protocol (run after 4e for every showcase-mg slot)**

Three gates that must all pass before the prop assignment is written to the storyboard:

**Gate 1 — API Contract Validation (HARD BLOCK)**

Read the selected component's `.tsx` source file to extract its TypeScript `Props` type. The prop names and value shapes you assign MUST match exactly. Common failures to catch before they reach the storyboard:
- Invented prop names that don't exist in the `Props` type (e.g., passing `before`/`after` when the component expects `leftLabel`/`rightLabel`; passing `text`/`weight`/`color` when the component expects `line1`/`line2`/`highlightWord`)
- Wrong value shape (e.g., `{ left: {...}, right: {...} }` when the component expects `stats: Stat[]`)
- Passing a `style` or other prop that does not appear in the `Props` type — it will silently be ignored
- Component is `React.FC` with no props generic (e.g., `export const FlowchartAnimation: React.FC = () => {`) — this means it accepts ZERO custom props and all content is hardcoded. Do NOT assign this component to a slot that requires custom content. Choose a different component that accepts the required props.

**BLOCK and pick a different component if any prop name or shape cannot be matched to the TypeScript Props type.**

**Gate 2 — Transcript Anchor Extraction**

For every prop value that represents spoken content (numbers, labels, claim text, tool names):
1. Locate the anchor word(s) in the transcript JSON (`words[].word`) and record the `start` timestamp
2. Convert to frame: `anchorFrame = Math.round(anchorTimestamp × fps)`
3. The MG `startFrame` MUST satisfy: `anchorFrame - 30 ≤ startFrame ≤ anchorFrame + 120`
   (fires no more than 0.5s before the word, no more than 2s after)
4. For cards covering multiple spoken claims (e.g., StatSplitCard with two different stats),
   align `startFrame` to the FIRST anchor; set `durationInFrames` so the card stays visible for
   at least 60 frames (1s) after the LAST anchor timestamp
5. Record both anchor words and their timestamps in the `notes` field of the Visual Asset Source Map row

**Gate 3 — Concept Complexity Gate (Type D intent only)**

If intent is `concept` and you selected a full diagram component (FlowchartAnimation, SVGLineTimeline, multi-node TransformationArrow):
- The concept MUST have been verbally explained by the speaker before or during the MG window
- Bridge/tease moments where the speaker merely names or teases a concept ("and that's where X comes in", "this is called Y") require a simple name-reveal component instead: BoldStatement, TextRevealMask, or CinematicReveal
- Full concept diagrams are reserved for body sections where the speaker explicitly walks through each element
- If the speaker has NOT yet said "let me explain", "here's how it works", "the structure looks like", or equivalent → BLOCK the diagram; assign a statement-type template instead

**4g. MG Description Quality Gate (HARD BLOCK — run after 4e and 4f for every MG slot)**

This gate prevents vague MG specs from reaching the storyboard. Vague specs require manual re-runs. All three checks below must pass before the slot is written to the storyboard.

**Check 1 — Hera Prompt Quality (applies when `hera: true`)**

The Hera prompt MUST follow the 5-part structure and be ≥100 words total:
1. **Subject:** The specific named interface or scene (e.g., "Claude chat interface with Projects sidebar visible")
2. **Motion:** What animates and how (e.g., "camera slowly zooms into the input field as typed text appears character-by-character at the cursor")
3. **Style:** Visual treatment (e.g., "dark UI theme with warm cream chat area, soft ambient glow on active elements")
4. **Color:** Exact hex codes from `tool-visual-reference.md` (e.g., "primary accent #D97757 terracotta, background #2B2A27")
5. **Duration hint:** Seconds and pacing note (e.g., "3.5 seconds total, zoom begins at 0.5s mark, typing visible from 1s")

A single sentence like "Shows the Claude interface being used" is a SYSTEM FAILURE. A vague "UI mockup of the tool" is a SYSTEM FAILURE.

MUST also specify: `reference_image_url` (library Supabase URL) or `image_source: frame-extract` with a resolved path. No reference image = HARD BLOCK — demote to showcase template instead.

**Check 2 — Showcase Typed Props (applies when `visual_type: showcase-mg`)**

The slot MUST have a `showcaseProps` object with prop keys matching the component's TypeScript Props type exactly (verified in Gate 1 of section 4f). Values must be concrete and render-ready — not free-text descriptions:

- ❌ BAD: `notes: "Shows some relevant automation stat"`
- ✅ GOOD: `showcaseProps: { value: "$5,500", label: "Claude Plugin Deal Closed", accentColor: "#2D6A4F" }`

FAIL if the slot's only documentation is a free-text description in the `notes` column without a `showcaseProps` object.

**Check 3 — Template Diversity Documentation**

For every MG slot, record in the Visual Asset Source Map `notes` field which 2-3 candidate templates were considered (from the mapping table in step 4b) and a one-line reason why the chosen template wins. This prevents the agent from defaulting to the same 4 components video-after-video.

- ❌ BAD: `notes: "BoldStatement"` (no consideration documented)
- ✅ GOOD: `notes: "Considered: BoldStatement (statement intent), TextRevealMask (more cinematic for hook), CinematicReveal. Selected CinematicReveal — hook moment benefits from reveal tension."`

FAIL if the notes field contains no candidate comparison.

### 5a. Assign Templates to Sections

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

### 5b. Present for Brief Review

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
- Assigning Hera to a slot whose intent is `number`, `list`, `statement`, `concept`, `logo`, or `comparison` — those are showcase-only
- Assigning Hera to an `interface` slot without verifying all three eligibility conditions
- Assigning a showcase template that would breach the Reuse Cap (> 2 in intro, > 3 in video, or same template in adjacent MG slots)
- Not recording `hera: true/false` in the Visual Asset Source Map row for each MG slot
- Approving more than 3 Hera slots in the intro
- Hera MG prompt is fewer than 100 words or missing the 5-part structure (subject/motion/style/color/duration)
- Hera MG missing a reference image path — demote to showcase template instead
- Showcase MG has free-text description in `notes` column instead of a typed `showcaseProps` object
- Not documenting 2-3 candidate templates considered per slot in the Visual Asset Source Map notes
- Not reading the full template-library.md before making assignments (defaulting to the same 4 templates)
