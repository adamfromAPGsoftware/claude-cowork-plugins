---
name: post-publish-pipeline
description: Collect inputs and launch the parallel post-publish pipeline to auto-generate all derivative content from a published YouTube video
---

# Post-Publish Pipeline [PP]

**Goal:** After a long-form YouTube video is published, auto-generate all derivative content in parallel — 5 short-form scripts, blog post, email draft, LinkedIn lead magnet post, and Instagram carousel — by collecting inputs and launching the Python orchestrator.

**Your Role:** You are the distribution logistics brain. You collect the YouTube URL and scheduling preferences, validate the project has all required source material, then hand off to the Python orchestrator for parallel execution. This workflow is intentionally thin — it's the UX layer.

---

## MANDATORY SEQUENCE

### 1. Collect YouTube URL

"**Post-Publish Pipeline — Let's generate all derivative content.**

I need a few details to kick this off:

**YouTube URL** — the published video URL:"

Wait for user to provide the URL. Validate it looks like a YouTube URL (contains `youtube.com/watch` or `youtu.be/`). Store as `{youtube_url}`.

### 2. Confirm Active Project

Load `{project-root}/content-plugin/data/active-project.yaml` and read the current `slug` and `title`.

"**Active project:** {title} (`{slug}`)

Is this the correct project? [Y]es / [N]o — provide different slug"

- If **Y** or affirmative: store `{project_slug}` = slug from active-project.yaml
- If **N**: ask for the correct slug, validate the project folder exists at `{project-root}/content/projects/{slug}/`, store as `{project_slug}`

### 3. Validate Project Content

Check that the project folder has minimum required content for the pipeline:

**Required:**
- `{project_folder}/{project_slug}/` — project folder exists
- At least one transcript file: `video-editor/analysis/*/transcript.json`

**Recommended (warn if missing but don't block):**
- Content concept: `strategist/ideation/content-concept-*.md`
- Video script: `copywriter/scripts/script-*.md`
- Visual analysis: `video-editor/analysis/*/visual-analysis.json`
- Audio analysis: `video-editor/analysis/*/audio-analysis.json`

"**Project content check:**
- ✅ Project folder exists
- ✅ Transcript found: {filename}
- {✅ or ⚠️} Content concept: {found or 'missing — blog/email quality may be reduced'}
- {✅ or ⚠️} Video script: {found or 'missing — short-form scripts may be limited'}
- {✅ or ⚠️} Visual analysis: {found or 'missing — short-form B-roll plans will be limited'}
- {✅ or ⚠️} Audio analysis: {found or 'missing — short-form pacing analysis unavailable'}"

If the project folder or transcript doesn't exist, halt: "❌ Cannot proceed — project folder or transcript missing. Run the video pipeline first."

### 4. Schedule Preferences

"**When should LinkedIn and Instagram posts be scheduled?**

Default: **tomorrow at 7:00 AM local time**

[D]efault — tomorrow 7am
[C]ustom — provide ISO datetime (e.g., 2026-03-13T07:00:00+11:00)
[S]eparate — different times for LinkedIn and Instagram"

- If **D**: calculate tomorrow 7am in local timezone, store as `{schedule_at}`
- If **C**: get datetime from user, store as `{schedule_at}`
- If **S**: get LinkedIn time as `{linkedin_at}` and Instagram time as `{instagram_at}`

### 5. Confirm and Launch

"**Post-Publish Pipeline — Ready to launch**

| Setting | Value |
|---------|-------|
| YouTube URL | `{youtube_url}` |
| Project | {title} (`{project_slug}`) |
| LinkedIn schedule | {schedule time} |
| Instagram schedule | {schedule time} |
| Tasks | shorts, blog, email, linkedin, instagram |

This will run **4 parallel lanes** generating all derivative content automatically.

**[G]o** — launch the pipeline
**[S]kip tasks** — skip specific tasks (e.g., 'skip shorts linkedin')
**[C]ancel** — abort"

- If **G**: proceed to step 6
- If **S**: ask which tasks to skip, store as `{skip_tasks}`, then re-present confirmation
- If **C**: "Pipeline cancelled." — return to menu

### 6. Launch Python Orchestrator

Build and execute the command:

```bash
python3 {project-root}/content-plugin/skills/5-publisher/workflows/post-publish-pipeline/scripts/ccs-post-publish.py "{youtube_url}" --slug {project_slug} {schedule_flags} {skip_flags}
```

Where:
- `{schedule_flags}` = `--schedule-at {schedule_at}` OR `--linkedin-at {linkedin_at} --instagram-at {instagram_at}`
- `{skip_flags}` = `--skip {space-separated skip tasks}` if any tasks are being skipped

Run this command and stream the output to the user.

### 7. Report Results

After the script completes, read `{project-root}/content/projects/{project_slug}/post-publish-status.yaml` and present a summary:

"**Post-Publish Pipeline — Complete**

| Task | Status | Duration |
|------|--------|----------|
| Short-form scripts | {status} | {duration or '-'} |
| Blog publish | {status} | {duration or '-'} |
| Email draft | {status} | {duration or '-'} |
| LinkedIn lead magnet | {status} | {duration or '-'} |
| LinkedIn schedule | {status} | {duration or '-'} |
| Instagram carousel | {status} | {duration or '-'} |
| Instagram schedule | {status} | {duration or '-'} |

{If any failures: '⚠️ Some tasks failed. You can re-run with `--resume` to retry failed tasks.'}
{If all success: '✅ All derivative content generated and scheduled successfully.'}"

---

## NOTES

- The Python script handles all parallel execution, retries, and state tracking
- Each task runs as a separate `claude -p` subprocess with YOLO mode
- The status YAML file persists state for `--resume` support
- Individual tasks can be skipped with `--skip` or retried with `--resume`
