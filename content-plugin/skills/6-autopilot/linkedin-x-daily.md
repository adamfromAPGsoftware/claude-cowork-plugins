---
name: linkedin-x-daily
description: Run the daily LinkedIn + X content generation cycle
menu-code: LX
---

# [LX] LinkedIn + X Daily

## Purpose

Run the full daily content generation cycle for LinkedIn and X. Researches, drafts, quality-checks, and saves to the review queue. Does NOT post — everything waits for [RQ] approval.

## Execution

Load and execute the workflow at:
`{project-root}/content-plugin/skills/6-autopilot/workflows/linkedin-x-daily/workflow.md`

Follow all 8 steps in sequence:
1. Init — load state, determine pillar + format
2. Research — YouTube-first check, then trend research
3. Analytics — pull post performance
4. Ideate — select topic and angle
5. Draft — write LinkedIn + X posts
6. Visual — generate or select asset
7. Quality gate — brand voice + anti-AI filter
8. Queue — save drafts, update state, notify

Run all steps end-to-end. In automated (scheduled) mode, make best-case decisions without pausing. In manual mode, present each step's output and allow overrides.
