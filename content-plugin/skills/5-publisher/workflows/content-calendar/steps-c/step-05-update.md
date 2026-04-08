---
name: 'step-05-update'
description: 'Add, modify, or remove calendar entries with schema enforcement and save to YAML'

actionMenuStepFile: './step-02-action-menu.md'
calendarFile: '{content_output_folder}/calendar/content-calendar.yaml'
calendarSchema: '../data/calendar-schema.md'
---

# Step 5: Update Entry

## STEP GOAL:

Add a new calendar entry, modify an existing entry, or remove an entry — enforcing the YAML schema on all writes — then save the updated calendar back to the file.

## MANDATORY EXECUTION RULES (READ FIRST):

### Universal Rules:

- 🛑 NEVER generate content without user input
- 📖 CRITICAL: Read the complete step file before taking any action
- 🔄 CRITICAL: When loading next step with 'C', ensure entire file is read
- 📋 YOU ARE A FACILITATOR, not a content generator
- ✅ YOU MUST ALWAYS SPEAK OUTPUT In your Agent communication style with the config `{communication_language}`

### Role Reinforcement:

- ✅ You are a calendar operations manager — precise, systematic
- ✅ If you already have been given communication or persona patterns, continue to use those while playing this new role
- ✅ Enforce schema strictly — reject invalid data

### Step-Specific Rules:

- 🎯 Focus ONLY on creating, modifying, or removing calendar entries
- 🚫 FORBIDDEN to save entries that violate the schema
- 💬 Confirm all changes with user before writing
- 🚫 FORBIDDEN to write to {calendarFile} without user confirmation

## EXECUTION PROTOCOLS:

- 🎯 Load schema from {calendarSchema} for validation
- 💾 Write changes to {calendarFile} after user confirmation
- 📖 Update metadata.last_updated and metadata.total_entries on every write
- 🚫 FORBIDDEN to write without schema validation

## CONTEXT BOUNDARIES:

- Calendar data loaded from {calendarFile}
- Schema defined in {calendarSchema}
- This step WRITES to the calendar file
- Returns to action menu after save
- All required fields must be present before saving

## MANDATORY SEQUENCE

**CRITICAL:** Follow this sequence exactly. Do not skip, reorder, or improvise unless user explicitly requests a change.

### 1. Load Schema

Load {calendarSchema} to understand required fields, valid values, and entry structure.

### 2. Select Update Operation

"**Update Calendar — Select an operation:**

**[A]** Add new entry
**[M]** Modify existing entry
**[R]** Remove entry

**Select:** [A] Add | [M] Modify | [R] Remove"

Wait for user selection.

### 3a. Add New Entry (IF A selected)

"**Add New Entry — Please provide the following details:**"

Collect each required field interactively:

1. **Title** (required): "**Title:** What is this content called?"
2. **Platform** (required): "**Platform:** Where will this be published? (linkedin, youtube, twitter, instagram, tiktok, facebook, threads, bluesky, pinterest, substack, medium, website, podcast, newsletter)"
3. **Content type** (required): "**Content type:** What format? (video, short-video, article, post, reel, story, carousel, thread, podcast-episode, newsletter-issue, blog-post, infographic, live-stream)"
4. **Status** (required): "**Status:** Current state? (draft, scheduled, published, cancelled)"
5. **Scheduled date** (optional): "**Scheduled date:** When is it planned? (YYYY-MM-DD or leave blank)"
6. **Publish date** (optional): "**Publish date:** When was it published? (YYYY-MM-DD or leave blank)"
7. **Project slug** (optional): "**Project slug:** Which project is this from? (leave blank for standalone)"
8. **Description** (optional): "**Description:** Brief summary of the content? (leave blank to skip)"

**Auto-assign:**
- `id`: Next incremental integer (max existing id + 1, or 1 if empty)
- `created_date`: Today's date

**Validate:**
- All required fields present
- Platform value is in valid list
- Content type value is in valid list
- Status value is in valid list
- Date formats are valid ISO dates (if provided)

**IF validation fails:**
"**Validation error:** {field} has invalid value '{value}'. Valid options: {valid_values}. Please correct."
— Re-collect the invalid field

**IF validation passes:**
Display the complete entry for confirmation:

"**New entry to add:**

```yaml
- id: {id}
  title: '{title}'
  platform: '{platform}'
  content_type: '{content_type}'
  status: '{status}'
  scheduled_date: '{scheduled_date}'
  publish_date: '{publish_date}'
  project_slug: '{project_slug}'
  description: '{description}'
  created_date: '{created_date}'
```

**Confirm add?** [Y] Yes | [N] No (cancel)"

Wait for confirmation.

**IF Y:** Append entry to {calendarFile} entries array, update metadata, proceed to step 5
**IF N:** "**Cancelled.** Returning to action menu." — Load {actionMenuStepFile}

### 3b. Modify Existing Entry (IF M selected)

Load {calendarFile} and display entries as a numbered list:

"**Select entry to modify:**

| # | ID | Title | Platform | Status |
|---|-----|-------|----------|--------|
| 1 | {id} | {title} | {platform} | {status} |
| 2 | {id} | {title} | {platform} | {status} |
| ... |

**Enter entry number:**"

Wait for selection.

"**Modifying entry #{id}: '{title}'**

**Current values:**
```yaml
{display all current field values}
```

**Which field(s) to update?** Enter field name and new value, or 'done' when finished.
Format: `field_name: new_value`
Example: `status: published` or `scheduled_date: 2026-03-15`"

Collect field updates. Validate each against schema. When user enters 'done':

Display the modified entry for confirmation:

"**Updated entry:**

```yaml
{display complete updated entry}
```

**Confirm changes?** [Y] Yes | [N] No (cancel)"

Wait for confirmation.

**IF Y:** Update entry in {calendarFile}, update metadata, proceed to step 5
**IF N:** "**Cancelled.** Returning to action menu." — Load {actionMenuStepFile}

### 3c. Remove Entry (IF R selected)

Load {calendarFile} and display entries as a numbered list (same as 3b).

"**Select entry to remove:**"

Wait for selection.

"**Remove entry #{id}: '{title}' ({platform}, {status})?**

**This action cannot be undone.**

**Confirm removal?** [Y] Yes | [N] No (cancel)"

Wait for confirmation.

**IF Y:** Remove entry from {calendarFile} entries array, update metadata, proceed to step 5
**IF N:** "**Cancelled.** Returning to action menu." — Load {actionMenuStepFile}

### 4. Handle Invalid Operation Selection

**IF Any other input in step 2:**
"**Not recognised.** Please select A, M, or R." — Redisplay operation menu

### 5. Save and Return

After any confirmed write operation:

1. Update `metadata.last_updated` to today's date
2. Update `metadata.total_entries` to current count of entries
3. Write the complete updated YAML to {calendarFile}
4. Confirm: "**Calendar updated.** {operation} complete. Total entries: {total_entries}."

"**Returning to action menu...**"

Load, read entire file, then execute {actionMenuStepFile}.

#### Menu Handling Logic:

- After saving, immediately load, read entire file, then execute {actionMenuStepFile}

#### EXECUTION RULES:

- This is an auto-return step — after save, return to action menu
- Always confirm with user before writing

---

## 🚨 SYSTEM SUCCESS/FAILURE METRICS

### ✅ SUCCESS:

- Schema loaded and enforced on all writes
- All required fields validated before saving
- User confirmed changes before write
- Metadata updated (last_updated, total_entries)
- Calendar file written successfully
- Returned to action menu

### ❌ SYSTEM FAILURE:

- Saving entries that violate schema
- Writing without user confirmation
- Not updating metadata after changes
- Not validating field values against allowed lists
- Losing existing entries during write

**Master Rule:** Skipping steps, optimizing sequences, or not following exact instructions is FORBIDDEN and constitutes SYSTEM FAILURE.
