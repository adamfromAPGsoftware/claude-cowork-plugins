# Package Plan Template

Use this template when compiling the package-plan.md file in step 07.

---

```markdown
# Thumbnail Package Plan

**Project:** {project-slug}
**Created:** {date}
**Combos:** {count}
**Average CTR Pre-Score:** {average}/7

---

## Keyword Summary

**High-Signal Keywords:** {comma-separated list}
**Rising/Breakout Terms:** {comma-separated list}
**Selected for Titles:** {comma-separated list}
**SEO Tags:** {comma-separated list for YouTube description}

---

## Combo Definitions

### Combo 1: {angle name}

**Title:** {full title}
**Title Characters:** {count}
**Text Overlay:** {text overlay}
**Text Characters:** {count}
**Keywords Used:** {which keywords integrated}
**CTR Pre-Score:** {X}/7

**Composition:**

| Element | Position | Description |
|---------|----------|-------------|
| Face | {position} | {expression direction} |
| Object/Context | {position} | {description} |
| Text | {position} | "{EXACT TEXT}" in {colour} {font style} |

**Background:** {specific background description}

**Full Prompt:**
```
{complete image prompt for fal-ai/nano-banana-2 — this is the source of truth for generation}
```

**CTR Pre-Validation:**

| # | Check | Score | Notes |
|---|-------|-------|-------|
| 1 | Text character count | {score} | {notes} |
| 2 | 3-element composition | {score} | {notes} |
| 3 | Curiosity gap | {score} | {notes} |
| 4 | Title-thumbnail coherence | {score} | {notes} |
| 5 | Mobile readability | {score} | {notes} |
| 6 | Emotional trigger | {score} | {notes} |
| 7 | ICP relevance | {score} | {notes} |

---

### Combo 2: {angle name}

{repeat structure}

---

### Combo 3: {angle name}

{repeat structure}

---

## YouTube Description

**Timestamp Source:** {storyboard | visual-analysis | transcript | none}

```
{full YouTube description text}
```

---

## Skool Classroom

**Lesson Title:** {skool lesson title}

**Description:**

{full Skool description — formatted with emojis, bold headers, → bullets, and key links}

---

## Generation Config

**Reference Photos:**
- Folder: {reference_photos_folder}
- Files: {ordered list of reference photo filenames — foundation image first}

**Inspiration Thumbnails:**
- Folder: {project_folder}/{project-slug}/creative-director/thumbnails/inspiration/
- Files: {list of inspiration thumbnail filenames, or 'none'}

**Output:**
- Folder: {project_folder}/{project-slug}/creative-director/thumbnails/generated/
- Naming: combo-{NN}-{slug}.png

**Execution Rules:**
- Sequential generation only (never parallel)
- Maximum 5 combos per batch
- If a combo fails, continue to next
- Run CTR validation on every generated combo
- Compare post-generation CTR against pre-scores above
```

---

## Template Notes

- The `Full Prompt` section for each combo is the **exact** text passed to the generation script — do NOT modify during generation
- Manual edits to this file are honoured — if the user edits titles, prompts, or compositions between draft and generation, the generation step uses the edited values
- The Generation Config section tells the thumbnail generation step where to find inputs and where to save outputs
- CTR Pre-Validation scores are compared against post-generation scores to flag any quality drops
