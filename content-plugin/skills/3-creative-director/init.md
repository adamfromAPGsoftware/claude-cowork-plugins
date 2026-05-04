---
name: init
description: First-run setup for CCS Creative Director
menu-code: INIT
---

# First-Run Setup for CCS Creative Director

Welcome! Setting up your workspace.

## Memory Location

Creating `{project-root}/memory/3-creative-director-sidecar/` for persistent memory.

## Initial Structure

Creating:
- `index.md` — active projects, thumbnail generation status, visual asset tracking
- `patterns.md` — visual preferences, prompt patterns, thumbnail performance
- `chronology.md` — session timeline

## Setup Questions

1. **Reference photos** — Confirm reference photos exist at `{reference_photos_folder}` from CCS config (minimum 3, recommended 5)
2. **Short-form inspiration** — Confirm 3 inspiration PNGs exist in the sidecar `short-form-inspiration/` folder
3. **Brand colours** — Confirm primary brand colour from `{brand.colors.primary}` in config.yaml

## Creating Memory Files

Once confirmed, create the following files:

### `{project-root}/memory/3-creative-director-sidecar/index.md`

```markdown
# CCS Creative Director — Session Index

## Active Projects
(none yet)

## Configuration
- Reference photos: confirmed ({count} photos)
- Short-form inspiration: confirmed ({count} PNGs)
- Brand colour: {brand.colors.primary} (from config.yaml)

## Last Session
(none)
```

### `{project-root}/memory/3-creative-director-sidecar/patterns.md`

```markdown
# Creative Director Patterns

## Visual Preferences
(style preferences, composition choices that work)

## Thumbnail Performance
(which styles and compositions drive best engagement)

## Prompt Patterns
(effective Gemini prompt patterns that produce strong results)

## Reference Image Notes
(which angles, expressions, and styles work best)
```

### `{project-root}/memory/3-creative-director-sidecar/chronology.md`

```markdown
# Session Chronology

(Sessions logged here as they accumulate)
```

## Ready

Setup complete! Ready to create visual assets.
