---
name: 'step-03-view'
description: 'Display filtered calendar entries in a readable format'

actionMenuStepFile: './step-02-action-menu.md'
calendarFile: '{content_output_folder}/calendar/content-calendar.yaml'
---

# Step 3: View/Query Calendar

## STEP GOAL:

Display calendar entries filtered by user-specified criteria (date range, platform, status, or all), then return to the action menu.

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
- ✅ Display data clearly in tabular format

### Step-Specific Rules:

- 🎯 Focus ONLY on reading and displaying calendar entries
- 🚫 FORBIDDEN to modify any calendar entries in this step
- 💬 Present results in clean, scannable tables
- 🚫 FORBIDDEN to skip filter selection

## EXECUTION PROTOCOLS:

- 🎯 Collect filter criteria from user
- 💾 Read {calendarFile} and apply filters
- 📖 Display matching entries in table format
- 🚫 This step is read-only — never write to calendar

## CONTEXT BOUNDARIES:

- Calendar data loaded from {calendarFile}
- This step only READS — never modifies
- Returns to action menu after display
- Filters are optional — user can view all entries

## MANDATORY SEQUENCE

**CRITICAL:** Follow this sequence exactly. Do not skip, reorder, or improvise unless user explicitly requests a change.

### 1. Collect Filter Criteria

"**View Calendar — Select a filter:**

**[A]** All entries — show everything
**[D]** By date range — filter by scheduled/publish date
**[P]** By platform — filter by target platform
**[S]** By status — filter by draft/scheduled/published/cancelled

**Select:** [A] All | [D] Date | [P] Platform | [S] Status"

Wait for user selection.

**IF A:** No filter — display all entries
**IF D:** Ask: "**Enter date range** (format: YYYY-MM-DD to YYYY-MM-DD):" — Wait for input
**IF P:** Ask: "**Enter platform** (e.g., linkedin, youtube, twitter):" — Wait for input
**IF S:** Ask: "**Enter status** (draft, scheduled, published, cancelled):" — Wait for input
**IF Any other:** Help user, redisplay filter menu

### 2. Load and Filter Calendar

Load {calendarFile} and apply the selected filter to the entries array.

**If no entries match the filter:**
"**No entries found** matching your filter criteria."

**If entries exist:**
Proceed to display.

### 3. Display Results

Display matching entries in a table:

"**Calendar Entries** ({count} results{filter description})

| ID | Title | Platform | Type | Status | Scheduled | Project |
|----|-------|----------|------|--------|-----------|---------|
| {id} | {title} | {platform} | {content_type} | {status} | {scheduled_date} | {project_slug} |
| ... | ... | ... | ... | ... | ... | ... |

**Total:** {count} entries"

### 4. Return to Action Menu

"**Returning to action menu...**"

Load, read entire file, then execute {actionMenuStepFile}.

#### Menu Handling Logic:

- After displaying results, immediately load, read entire file, then execute {actionMenuStepFile}

#### EXECUTION RULES:

- This is an auto-return step — after display, return to action menu
- No additional user choice needed at this point

---

## 🚨 SYSTEM SUCCESS/FAILURE METRICS

### ✅ SUCCESS:

- Filter criteria collected from user
- Calendar entries loaded and filtered correctly
- Results displayed in clean table format
- Returned to action menu after display

### ❌ SYSTEM FAILURE:

- Modifying entries during a view operation
- Not applying the selected filter
- Displaying results without table formatting
- Not returning to action menu

**Master Rule:** Skipping steps, optimizing sequences, or not following exact instructions is FORBIDDEN and constitutes SYSTEM FAILURE.
