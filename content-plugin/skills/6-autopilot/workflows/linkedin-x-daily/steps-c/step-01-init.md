---
name: step-01-init
description: Load autopilot state, advance rotation indices, determine today's pillar and format
nextStep: ./step-02-research.md
---

# Step 1: Initialize

## Goal

Load the current rotation state, advance indices for today's run, and establish the pillar + format + template + CTA type for this cycle.

## Sequence

### 1. Load State

Read `{stateFile}` (autopilot-state.yaml).

Extract:
- `rotation.pillar.sequence` — the full pillar sequence array
- `rotation.pillar.current_index` — index of LAST run (advance this by 1)
- `rotation.format.sequence` — the full format sequence array
- `rotation.format.current_index` — index of LAST run (advance this by 1)
- `history` — the run history array

### 2. Advance Indices

Advance both indices by 1, wrapping at the end of each sequence:

```
new_pillar_index = (current_pillar_index + 1) % len(pillar_sequence)
new_format_index = (current_format_index + 1) % len(format_sequence)
```

Today's pillar = `pillar_sequence[new_pillar_index]`
Today's format = `format_sequence[new_format_index]`

**Do NOT write back to the state file yet** — only update state in step-08 after the full workflow completes.

### 3. Map Pillar to Template + CTA

Read `{pillarData}` (pillar-rotation.md) for full pillar definitions. Map as follows:

| Pillar | LinkedIn Template | CTA Type |
|--------|-------------------|----------|
| personal | Vulnerability Story or Contrarian Anti-List (vary between runs) | none |
| technical | Nurture / Educational | resource-giveaway |
| lead-magnet | Core Template | keyword |
| nurture | Educational with personality | resource-giveaway or none |

For personal pillar, alternate between the two templates based on history: if last personal run used Vulnerability Story, use Contrarian Anti-List today, and vice versa.

### 4. Load Brand Context

Load:
- `{brandVoice}` — brand voice rules (hold in context for step-05 and step-07)
- `{contentICP}` — content ICP profile (hold in context for step-04 and step-07)

### 5. Output Summary

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Today's content generation cycle
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Pillar:    {pillar} (index {new_pillar_index}/{len-1})
Format:    {format} (index {new_format_index}/{len-1})
Template:  {template name}
CTA type:  {none | resource-giveaway | keyword}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Proceeding to research...
```

Then immediately load and execute step-02.
