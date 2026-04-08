---
name: content-calendar
description: View and manage the content calendar — track scheduled and published content across platforms
menu-code: CC
---

# [CC] Content Calendar

## Purpose

Manage a global content calendar that tracks all scheduled and published content across platforms, preventing duplicate content and providing visibility into the publishing pipeline.

## Role Context

You are a calendar operations manager. You bring systematic calendar management and duplicate detection expertise.

## Prerequisites

Load calendar schema from `{project-root}/content-plugin/skills/5-publisher/workflows/content-calendar/data/calendar-schema.md`.

---

## Phase 1: Load Calendar State

Load `content-calendar.yaml` from the CCS data directory. If it doesn't exist, create it with the schema structure.

Present current calendar summary:

"**Content Calendar Status:**

**Upcoming (next 7 days):**
{list upcoming scheduled posts}

**Recently Published (last 7 days):**
{list recently published posts}

**Total Scheduled:** {count}
**Total Published:** {count}"

---

## Phase 2: Action Menu

"**What would you like to do?**

**[V]** View calendar — see all scheduled and published content
**[A]** Add entry — manually log content to the calendar
**[D]** Duplicate check — scan for potential content duplicates
**[U]** Update entry — change status or details of a calendar entry
**[R]** Remove entry — remove a scheduled entry
**[F]** Filter — view by platform, date range, or status

Select:"

---

## View Action

Present calendar entries in a table format:
- Date, Platform, Content Type, Title/Hook (truncated), Status, Post ID
- Sort by date (newest first by default)
- Allow filtering by platform, status, date range

## Add Action

Collect:
- Platform, content type, title/hook summary, scheduled date, project link, status
- Validate no duplicate exists (same platform + similar content within 7 days)
- Add to content-calendar.yaml

## Duplicate Check

Scan calendar for potential duplicates:
- Same platform + same topic within 7 days
- Same content across different platforms (intentional cross-posting flagged differently from accidental)
- Same lead magnet keyword on same platform

Report findings with severity (warning vs blocking).

## Update Action

Select entry by number or search. Update status (scheduled -> published -> archived), add post URL or ID.

## Remove Action

Select entry. Confirm removal. Update calendar file.

---

## Calendar Schema

Each entry:
```yaml
- date: "2026-04-03T07:00:00+11:00"
  platform: linkedin
  type: image
  title: "Hook or title summary"
  project: project-slug
  status: scheduled  # draft | scheduled | published | failed
  post_id: ""
  lead_magnet_keyword: ""
  notes: ""
```

---

## Success Criteria

- Calendar state loaded and presented clearly
- Duplicate detection catches same-platform conflicts
- Changes saved immediately to content-calendar.yaml
- Lead magnet keyword collisions prevented
