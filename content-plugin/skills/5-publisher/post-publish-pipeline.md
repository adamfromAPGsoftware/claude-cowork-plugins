---
name: post-publish-pipeline
description: Auto-generate all derivative content from a published YouTube video
menu-code: PP
---

# [PP] Post-Publish Pipeline

## Purpose

After a long-form YouTube video is published, auto-generate all derivative content in parallel — 5 short-form scripts, blog post, ConvertKit email, LinkedIn lead magnet post, and Instagram carousel — by collecting inputs and launching the Python orchestrator.

## Role Context

You are the distribution logistics brain. Collect the YouTube URL and scheduling preferences, validate the project has all required source material, then hand off to the Python orchestrator for parallel execution. This workflow is intentionally thin — it's the UX layer.

---

## Phase 1: Collect YouTube URL

"**Post-Publish Pipeline — Let's generate all derivative content.**

**YouTube URL** — the published video URL:"

Validate URL contains `youtube.com/watch` or `youtu.be/`.

## Phase 2: Confirm Active Project

Load `{project-root}/_bmad/ccs/active-project.yaml`. Confirm slug and title with user.

## Phase 3: Validate Project Content

Check project folder has minimum required content:

**Required:**
- Project folder exists
- At least one transcript file in `video-editor/analysis/`

**Recommended (warn but don't block):**
- Content concept in `strategist/ideation/`
- Video script in `copywriter/scripts/`
- Visual analysis in `video-editor/analysis/`
- Audio analysis in `video-editor/analysis/`

Present validation summary.

## Phase 4: Schedule Preferences

"**When should LinkedIn and Instagram posts be scheduled?**

[D]efault — tomorrow 7am
[C]ustom — provide ISO datetime
[S]eparate — different times for LinkedIn and Instagram"

## Phase 5: Confirm and Launch

Present summary table and confirm:

"**[G]o** — launch the pipeline
**[S]kip tasks** — skip specific tasks
**[C]ancel** — abort"

## Phase 6: Launch Python Orchestrator

```bash
python3 {project-root}/content-plugin/skills/5-publisher/workflows/post-publish-pipeline/scripts/ccs-post-publish.py \
    "{youtube_url}" \
    --slug {project_slug} \
    {schedule_flags} \
    {skip_flags}
```

Stream output to user.

## Phase 7: Report Results

Read `post-publish-status.yaml` and present:

| Task | Status | Duration |
|------|--------|----------|
| Short-form scripts | {status} | {duration} |
| Blog publish | {status} | {duration} |
| Email draft | {status} | {duration} |
| LinkedIn lead magnet | {status} | {duration} |
| LinkedIn schedule | {status} | {duration} |
| Instagram carousel | {status} | {duration} |
| Instagram schedule | {status} | {duration} |

---

## Notes

- The Python script handles parallel execution, retries, and state tracking
- Each task runs as a separate `claude -p` subprocess
- Status YAML file persists state for `--resume` support
- Individual tasks can be skipped or retried
