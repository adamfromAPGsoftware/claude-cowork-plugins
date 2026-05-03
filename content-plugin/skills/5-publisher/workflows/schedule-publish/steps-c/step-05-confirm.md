---
name: 'step-05-confirm'
description: 'Update content calendar, create scheduling records, and present final confirmation summary'

calendarFile: '{content_output_folder}/calendar/content-calendar.yaml'
calendarSchema: '{project-root}/content-plugin/skills/5-publisher/workflows/content-calendar/data/calendar-schema.md'
---

# Step 5: Confirm & Update Calendar

## STEP GOAL:

To update the content calendar with new entries for all successfully scheduled posts, create project or standalone scheduling records, and present a final confirmation summary with platform details.

## MANDATORY EXECUTION RULES (READ FIRST):

### Universal Rules:

- 🛑 NEVER generate content without user input
- 📖 CRITICAL: Read the complete step file before taking any action
- 📋 YOU ARE A FACILITATOR, not a content generator
- ✅ YOU MUST ALWAYS SPEAK OUTPUT In your Agent communication style with the config `{communication_language}`
- ⚙️ TOOL/SUBPROCESS FALLBACK: If any instruction references a subprocess, subagent, or tool you do not have access to, you MUST still achieve the outcome in your main context thread

### Role Reinforcement:

- ✅ You are a calendar operations manager — the calendar is the single source of truth
- ✅ If you already have been given communication or persona patterns, continue to use those while playing this new role
- ✅ Every scheduled post must be accounted for on the calendar

### Step-Specific Rules:

- 🎯 Focus ONLY on calendar updates, record creation, and confirmation
- 🚫 FORBIDDEN to call the Buffer MCP in this step — scheduling is complete
- 🚫 FORBIDDEN to skip calendar update — if it's scheduled, it must be on the calendar
- 💬 Present clear, complete confirmation with all details

## EXECUTION PROTOCOLS:

- 🎯 Load calendar schema for entry format
- 💾 Update {calendarFile} with new entries
- 📖 Create scheduling record in project or standalone folder
- 🚫 This is the final step — end workflow after confirmation

## CONTEXT BOUNDARIES:

- Available: Successfully scheduled posts from step 04, platform details, Buffer post IDs, date/time
- Calendar schema from {calendarSchema} (shared with content-calendar workflow)
- Calendar file at {calendarFile}
- Project/standalone mode determines scheduling record location
- This is the FINAL step — workflow ends here

## MANDATORY SEQUENCE

**CRITICAL:** Follow this sequence exactly. Do not skip, reorder, or improvise unless user explicitly requests a change.

### 1. Load Calendar Schema

Load {calendarSchema} to understand the entry format and valid field values for writing new entries.

### 2. Update Content Calendar

Load {calendarFile}.

**If file does not exist:**
- Create the directory structure if needed
- Create {calendarFile} with the empty calendar template from the schema
- Then add entries

**For each successfully scheduled post, add a new entry:**

```yaml
- id: {next auto-increment id}
  title: '{content title}'
  platform: '{platform}'
  content_type: '{content_type}'
  status: 'scheduled'
  scheduled_date: '{scheduled date}'
  publish_date: ''
  project_slug: '{project-slug or empty if standalone}'
  description: '{brief content summary}'
  created_date: '{today}'
```

Update metadata:
```yaml
metadata:
  last_updated: '{today}'
  total_entries: {updated count}
```

Save the updated {calendarFile}.

"**Content calendar updated — {count} new entry/entries added.**"

### 3. Create Scheduling Record

**If in project mode:**

Create or update: `{project_folder}/{project-slug}/publisher/scheduled/scheduled-{date}.yaml`

```yaml
metadata:
  created: '{today}'
  project_slug: '{project-slug}'
  scheduled_by: 'schedule-publish workflow'

scheduled_items:
  - platform: '{platform}'
    account: '{account handle}'
    scheduled_date: '{date}'
    scheduled_time: '{time}'
    buffer_post_id: '{id from Buffer MCP response}'
    content_title: '{title}'
    content_type: '{content_type}'
    status: 'scheduled'
    calendar_entry_id: {calendar entry id}
```

"**Project scheduling record created at** `{record path}`"

**If in standalone mode:**

Create or update: `{standalone_folder}/{date}-scheduled/scheduled.yaml`

Use the same schema as project mode, omitting `project_slug`.

"**Standalone scheduling record created at** `{record path}`"

### 4. Present Final Confirmation

"**Scheduling complete.**

---

**Summary:**

| # | Platform | Account | Scheduled For | Buffer Post ID | Calendar ID |
|---|----------|---------|---------------|----------------|-------------|
| 1 | {platform} | @{handle} | {date} {time} | {buffer_post_id} | #{calendar_id} |

**Files updated:**
- Content calendar: `{calendarFile}` — {count} new entries
- Scheduling record: `{record path}`

**Content title:** {title}
**Scheduled by:** schedule-publish workflow
**Date:** {today}

---

**All done. Your content is scheduled and accounted for on the calendar.**"

### 5. Workflow Complete

This is the final step. No further steps to load.

"**Workflow complete — returning to agent menu.**"

---

## 🚨 SYSTEM SUCCESS/FAILURE METRICS

### ✅ SUCCESS:

- Calendar schema loaded from shared content-calendar workflow
- Content calendar updated with correct entry format and valid field values
- Metadata (last_updated, total_entries) updated accurately
- Scheduling record created in correct location (project or standalone)
- Confirmation summary displayed with all platform details, Buffer post IDs, and calendar IDs
- Workflow ended cleanly

### ❌ SYSTEM FAILURE:

- Not updating the content calendar
- Writing entries that don't match the shared schema format
- Not creating scheduling record
- Missing Buffer post IDs or calendar references in confirmation
- Calling Buffer MCP in this step
- Not ending the workflow

**Master Rule:** Skipping steps, optimizing sequences, or not following exact instructions is FORBIDDEN and constitutes SYSTEM FAILURE.
