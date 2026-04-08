---
name: 'step-01-init'
description: 'Load or initialise the content calendar YAML file and display summary'

nextStepFile: './step-02-action-menu.md'
calendarFile: '{content_output_folder}/calendar/content-calendar.yaml'
calendarSchema: '../data/calendar-schema.md'
---

# Step 1: Initialise Calendar

## STEP GOAL:

Load the existing content-calendar.yaml file, or create an empty one if it doesn't exist, then display a summary of current calendar state before proceeding to the action menu.

## MANDATORY EXECUTION RULES (READ FIRST):

### Universal Rules:

- 🛑 NEVER generate content without user input
- 📖 CRITICAL: Read the complete step file before taking any action
- 🔄 CRITICAL: When loading next step with 'C', ensure entire file is read
- 📋 YOU ARE A FACILITATOR, not a content generator
- ✅ YOU MUST ALWAYS SPEAK OUTPUT In your Agent communication style with the config `{communication_language}`

### Role Reinforcement:

- ✅ You are a calendar operations manager — precise, systematic, no ambiguity
- ✅ If you already have been given communication or persona patterns, continue to use those while playing this new role
- ✅ Organised, brief, status-focused communication

### Step-Specific Rules:

- 🎯 Focus ONLY on loading/creating the calendar and displaying summary
- 🚫 FORBIDDEN to modify any calendar entries in this step
- 💬 Display clear, concise calendar status
- 🚫 FORBIDDEN to proceed without confirming calendar state

## EXECUTION PROTOCOLS:

- 🎯 Load or create calendar YAML file
- 💾 If creating new, use empty template from {calendarSchema}
- 📖 Display summary to user
- 🚫 This is the init step — sets up state for all subsequent actions

## CONTEXT BOUNDARIES:

- Calendar file location: {calendarFile}
- Schema definition: {calendarSchema}
- This step only READS or CREATES — never modifies entries
- No prior workflow output required

## MANDATORY SEQUENCE

**CRITICAL:** Follow this sequence exactly. Do not skip, reorder, or improvise unless user explicitly requests a change.

### 1. Load Calendar Schema

Load {calendarSchema} to understand the YAML structure and valid field values.

### 2. Check for Existing Calendar

Check if {calendarFile} exists:

**IF file exists:**
- Load the complete file
- Parse the YAML content
- Proceed to step 3

**IF file does NOT exist:**
- Create the directory structure if needed
- Create {calendarFile} with the empty calendar template:

```yaml
metadata:
  last_updated: ''
  total_entries: 0

entries: []
```

- Confirm creation: "**Created new content calendar at** `{calendarFile}`"
- Proceed to step 3

**IF file exists but is malformed:**
- Report the error: "**Calendar file found but YAML is malformed.** Would you like me to reinitialise it? This will clear all existing data."
- Wait for user confirmation before reinitialising
- If user declines, exit workflow

### 3. Display Calendar Summary

"**Content Calendar Status**

| Metric | Value |
|--------|-------|
| Total entries | {total_entries} |
| Draft | {count of status=draft} |
| Scheduled | {count of status=scheduled} |
| Published | {count of status=published} |
| Cancelled | {count of status=cancelled} |

**Upcoming (next 7 days):**
{List entries with scheduled_date within 7 days, or 'No upcoming content scheduled'}

**Last updated:** {metadata.last_updated or 'Never'}"

### 4. Auto-Proceed to Action Menu

"**Proceeding to action menu...**"

Load, read entire file, then execute {nextStepFile}.

#### Menu Handling Logic:

- After displaying calendar summary, immediately load, read entire file, then execute {nextStepFile}

#### EXECUTION RULES:

- This is an auto-proceed step with no user menu choices
- Proceed directly to action menu after displaying summary

---

## 🚨 SYSTEM SUCCESS/FAILURE METRICS

### ✅ SUCCESS:

- Calendar file loaded or created successfully
- Summary displayed with accurate counts
- Upcoming items shown
- Auto-proceeded to action menu

### ❌ SYSTEM FAILURE:

- Not checking if file exists before creating
- Modifying entries during init
- Not handling malformed YAML gracefully
- Not displaying summary before proceeding

**Master Rule:** Skipping steps, optimizing sequences, or not following exact instructions is FORBIDDEN and constitutes SYSTEM FAILURE.
