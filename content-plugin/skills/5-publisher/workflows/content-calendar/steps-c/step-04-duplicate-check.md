---
name: 'step-04-duplicate-check'
description: 'Scan calendar entries for duplicate or overlapping content and report findings'

actionMenuStepFile: './step-02-action-menu.md'
calendarFile: '{content_output_folder}/calendar/content-calendar.yaml'
calendarSchema: '../data/calendar-schema.md'
---

# Step 4: Duplicate Check

## STEP GOAL:

Scan all calendar entries for duplicate or overlapping content using the duplicate detection rules defined in the schema, and report findings to the user.

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
- ✅ Flag potential issues clearly with severity levels

### Step-Specific Rules:

- 🎯 Focus ONLY on detecting and reporting duplicates
- 🚫 FORBIDDEN to modify any calendar entries in this step
- 💬 Report findings with clear severity and actionable details
- 🚫 FORBIDDEN to auto-resolve duplicates — report only

## EXECUTION PROTOCOLS:

- 🎯 Load duplicate detection rules from {calendarSchema}
- 💾 Read {calendarFile} and scan all entries
- 📖 Report findings with severity levels
- 🚫 This step is read-only — never write to calendar

## CONTEXT BOUNDARIES:

- Calendar data loaded from {calendarFile}
- Duplicate detection rules defined in {calendarSchema}
- This step only REPORTS — never modifies
- Returns to action menu after reporting
- User can optionally filter the scan scope

## MANDATORY SEQUENCE

**CRITICAL:** Follow this sequence exactly. Do not skip, reorder, or improvise unless user explicitly requests a change.

### 1. Load Duplicate Detection Rules

Load {calendarSchema} and extract the duplicate detection rules:

1. **Same platform** AND **similar title** (case-insensitive substring match or >70% word overlap)
2. **Same platform** AND **same scheduled_date** (collision — two items on same platform, same day)
3. **Same title** across **different platforms** within a 3-day window (intentional cross-posting — flag as informational)

### 2. Optional Scope Filter

"**Duplicate Check — would you like to narrow the scan?**

**[A]** Scan all entries
**[P]** Scan specific platform only
**[D]** Scan specific date range only

**Select:** [A] All | [P] Platform | [D] Date range"

Wait for user selection.

**IF A:** Scan all entries
**IF P:** Ask for platform, filter entries
**IF D:** Ask for date range, filter entries
**IF Any other:** Help user, redisplay

### 3. Run Duplicate Detection

Load {calendarFile} and apply each detection rule against the scoped entries.

For each pair of entries, check:
- **Rule 1 — Title similarity:** Compare titles case-insensitively. Flag if substring match or >70% word overlap on the same platform.
- **Rule 2 — Date collision:** Flag entries on the same platform with the same scheduled_date.
- **Rule 3 — Cross-post detection:** Flag entries with the same/similar title across different platforms within a 3-day window.

### 4. Report Findings

**If no duplicates found:**

"**Duplicate Check Complete — No issues found.**

Scanned {count} entries. No duplicates or collisions detected."

**If duplicates found:**

"**Duplicate Check Complete — {issue_count} potential issue(s) found.**

| # | Type | Severity | Entry A | Entry B | Detail |
|---|------|----------|---------|---------|--------|
| 1 | Title match | HIGH | #{id_a} '{title_a}' ({platform_a}) | #{id_b} '{title_b}' ({platform_b}) | {detail} |
| 2 | Date collision | MEDIUM | #{id_a} '{title_a}' ({date}) | #{id_b} '{title_b}' ({date}) | Same platform, same day |
| 3 | Cross-post | INFO | #{id_a} '{title_a}' ({platform_a}, {date_a}) | #{id_b} '{title_b}' ({platform_b}, {date_b}) | Similar content within 3 days |

**Severity Guide:**
- **HIGH** — Likely duplicate, should be resolved
- **MEDIUM** — Scheduling collision, review timing
- **INFO** — Intentional cross-posting detected, no action needed unless unintended

**To resolve issues, use [U] Update Entry from the action menu.**"

### 5. Return to Action Menu

"**Returning to action menu...**"

Load, read entire file, then execute {actionMenuStepFile}.

#### Menu Handling Logic:

- After displaying report, immediately load, read entire file, then execute {actionMenuStepFile}

#### EXECUTION RULES:

- This is an auto-return step — after report, return to action menu
- No additional user choice needed at this point

---

## 🚨 SYSTEM SUCCESS/FAILURE METRICS

### ✅ SUCCESS:

- Detection rules loaded from schema
- All entries scanned against all 3 rules
- Findings reported with severity levels
- Clear guidance on resolution provided
- Returned to action menu

### ❌ SYSTEM FAILURE:

- Modifying entries during duplicate check
- Not applying all 3 detection rules
- Reporting without severity levels
- Auto-resolving duplicates without user action
- Not returning to action menu

**Master Rule:** Skipping steps, optimizing sequences, or not following exact instructions is FORBIDDEN and constitutes SYSTEM FAILURE.
