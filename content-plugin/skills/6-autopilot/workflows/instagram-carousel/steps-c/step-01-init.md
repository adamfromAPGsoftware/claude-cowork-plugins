---
name: step-01-init
description: Load IC rotation state, advance topic index, flag if inspiration scrape is needed
nextStep: ./step-02-scrape.md
---

# Step 1: Initialize

## Goal

Load the IC-specific rotation state, advance to today's topic angle, and determine whether the inspiration library needs refreshing before we research and draft.

## Sequence

### 1. Load State

Read `{stateFile}` (autopilot-state.yaml).

Extract the `ic_rotation` block:
- `ic_rotation.topic.sequence` — the 5-angle topic array
- `ic_rotation.topic.current_index` — index of LAST IC run (advance by 1)
- `ic_rotation.inspiration.last_scrape` — ISO date of last Apify scrape
- `ic_rotation.inspiration.scrape_interval_days` — how many days between scrapes (default: 7)

**Do NOT write back to the state file yet** — only update in step-09 after the full workflow completes.

### 2. Advance Topic Index

```
new_index = (current_index + 1) % len(topic_sequence)
```

Today's topic angle = `topic_sequence[new_index]`

### 3. Check Inspiration Staleness

Calculate days since last scrape:
```
days_since_scrape = (today - last_scrape_date).days
needs_scrape = days_since_scrape >= scrape_interval_days OR last_scrape is null
```

Also check if `{inspirationDir}` exists and has any post directories — if empty, `needs_scrape = true` regardless.

### 4. Load Brand Context

Load:
- `{brandVoice}` — brand voice rules + Anti-AI Red Flags filter (hold in context for step-06 and step-08)
- `{contentICP}` — content ICP profile (hold in context for step-05 and step-08)
- `{carouselGuidelines}` — dark mode carousel design rules (hold in context for step-07)

Read `{topicRotation}` and extract the full definition for today's topic angle (Exa queries, preferred CTA keywords, example concepts).

### 5. Output Summary

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Instagram Carousel — IC Cycle
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Topic angle:    {topic_angle} (index {new_index}/4)
Last run:       {last_ic_run_date or 'never'}
Inspiration:    {days_since_scrape}d old — {'REFRESH NEEDED' if needs_scrape else 'OK (using cache)'}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

Then immediately load and execute step-02.
