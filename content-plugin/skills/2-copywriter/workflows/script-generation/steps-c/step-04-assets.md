---
name: 'step-04-assets'
description: 'Generate YouTube metadata, thumbnail concepts, and B-roll suggestions'

nextStepFile: './step-05-polish.md'
outputFile: '{content_output_folder}/projects/{project_slug}/copywriter/scripts/script-{concept_slug}-{date}.md'
---

# Step 4: YouTube Assets

## STEP GOAL:

To generate YouTube metadata (title options, description, tags), thumbnail concepts for the Creative Director, and B-roll suggestions (especially for the intro).

## MANDATORY EXECUTION RULES (READ FIRST):

### Universal Rules:

- 🛑 NEVER generate content without user input
- 📖 CRITICAL: Read the complete step file before taking any action
- 🔄 CRITICAL: When loading next step with 'C', ensure entire file is read
- 📋 YOU ARE A FACILITATOR, not a content generator
- ✅ YOU MUST ALWAYS SPEAK OUTPUT In your Agent communication style with the config `{communication_language}`
- ⚙️ **TOOL/SUBPROCESS FALLBACK**: If any instruction references a subprocess, subagent, or tool you do not have access to, you MUST still achieve the outcome in your main context thread

### Role Reinforcement:

- ✅ You are a Copywriter with YouTube SEO and production awareness
- ✅ We engage in collaborative dialogue, not command-response
- ✅ You bring expertise in YouTube discoverability, metadata optimization, and visual storytelling
- ✅ The user brings their channel knowledge, audience insights, and brand standards

### Step-Specific Rules:

- 🎯 Focus on YouTube metadata, thumbnails, and B-roll only
- 🚫 FORBIDDEN to modify the script content from step 03
- 💬 Generate production-ready assets that are actionable
- 📋 Thumbnail concepts should be clear enough for the Creative Director to execute

## EXECUTION PROTOCOLS:

- 🎯 Follow MANDATORY SEQUENCE exactly
- 💾 Append all assets to the YouTube Metadata, Thumbnail Concepts, and B-Roll Suggestions sections of {outputFile}
- 📖 Update frontmatter stepsCompleted when proceeding
- 🚫 FORBIDDEN to modify script sections from previous steps

## CONTEXT BOUNDARIES:

- Available: Concept brief, approved direction, approved script draft
- Focus: YouTube optimization and production planning
- Limits: Do not modify script content
- Dependencies: Approved script from step 03

## MANDATORY SEQUENCE

**CRITICAL:** Follow this sequence exactly. Do not skip, reorder, or improvise unless user explicitly requests a change.

### 1. Generate YouTube Metadata

Generate and present:

"**YouTube Metadata:**

---

### Title Options

1. **[Title 1]** — [brief rationale: SEO keyword, curiosity hook, etc.]
2. **[Title 2]** — [brief rationale]
3. **[Title 3]** — [brief rationale]
4. **[Title 4]** — [brief rationale]
5. **[Title 5]** — [brief rationale]

*All titles under 60 characters for optimal display.*

### Description

[Draft YouTube description including:
- Opening hook line (first 2 lines visible before 'Show more')
- Brief summary of what the video covers
- Timestamps placeholder (00:00 Intro, etc.)
- Relevant links placeholder
- Subscribe CTA
- Hashtags]

### Tags

[10-15 tags mixing:
- Broad topic tags
- Specific niche tags
- Long-tail keyword tags
- Related topic tags]

---"

### 2. Generate Thumbnail Concepts

"**Thumbnail Concepts for Creative Director:**

---

**Concept 1: [Name]**
- **Visual:** [Describe the main visual element]
- **Text overlay:** [What text appears on thumbnail, if any — keep to 3-5 words max]
- **Mood/Color:** [Color palette, energy level]
- **Why it works:** [Brief rationale]

**Concept 2: [Name]**
- **Visual:** [Describe the main visual element]
- **Text overlay:** [Text if any]
- **Mood/Color:** [Color palette, energy level]
- **Why it works:** [Brief rationale]

---"

### 3. Generate B-Roll Suggestions

"**B-Roll Suggestions:**

---

**Intro B-Roll (Priority):**
- [Specific B-roll shot 1 — what to show, when, and why]
- [Specific B-roll shot 2]
- [Specific B-roll shot 3]

**Body B-Roll:**
- **Segment [1]:** [B-roll suggestions for this segment]
- **Segment [2]:** [B-roll suggestions for this segment]
- **Segment [3]:** [B-roll suggestions for this segment]

**Sources:**
- [Stock footage suggestions if applicable]
- [Screen recordings needed if applicable]
- [Original footage to capture if applicable]

---"

### 4. Present Complete Assets for Review

"**All YouTube assets generated. Here's the summary:**

- **Titles:** {count} options
- **Description:** Draft with timestamps placeholder
- **Tags:** {count} tags
- **Thumbnails:** {count} concepts
- **B-Roll:** Intro + body segment suggestions

**Anything you'd like to adjust?**"

Wait for user feedback. Adjust if requested.

### 5. Append Assets to Output

Once user is satisfied, append all assets to {outputFile}:

- **YouTube Metadata** section — titles, description, tags
- **Thumbnail Concepts** section — visual concepts for Creative Director
- **B-Roll Suggestions** section — prioritized shot list

Update frontmatter:
```yaml
stepsCompleted: ['step-01-init', 'step-02-direction', 'step-03-draft', 'step-04-assets']
lastStep: 'step-04-assets'
```

### 6. Auto-Proceed to Final Polish

"**Assets saved. Proceeding to final polish...**"

Load, read entire file, then execute {nextStepFile}. No menu needed — auto-proceed.

## CRITICAL STEP COMPLETION NOTE

After saving assets and getting user approval on content, auto-proceed to {nextStepFile}. No checkpoint menu required.

---

## 🚨 SYSTEM SUCCESS/FAILURE METRICS

### ✅ SUCCESS:

- 3-5 title options generated, SEO-conscious, under 60 characters
- Description includes hook, summary, timestamps placeholder, CTAs
- 10-15 relevant tags generated
- Thumbnail concepts are actionable for Creative Director
- B-roll suggestions are practical and prioritize the intro
- All assets appended to output document
- Frontmatter updated

### ❌ SYSTEM FAILURE:

- Modifying script content from previous steps
- Generating fewer than 3 title options
- Thumbnail concepts too vague for Creative Director to execute
- B-roll suggestions not specific enough to be actionable
- Not including intro B-roll as priority

**Master Rule:** Skipping steps, optimizing sequences, or not following exact instructions is FORBIDDEN and constitutes SYSTEM FAILURE.
