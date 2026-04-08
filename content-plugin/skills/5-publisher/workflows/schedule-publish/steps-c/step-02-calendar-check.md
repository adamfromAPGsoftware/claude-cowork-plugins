---
name: 'step-02-calendar-check'
description: 'Check content calendar for scheduling conflicts and duplicate content'

nextStepFile: './step-03-platform-format.md'
calendarFile: '{content_output_folder}/calendar/content-calendar.yaml'
calendarSchema: '{project-root}/content-plugin/skills/5-publisher/workflows/content-calendar/data/calendar-schema.md'
scheduleGuide: '../data/posting-schedule-guide.md'
---

# Step 2: Calendar Check

## STEP GOAL:

To check the content calendar for scheduling conflicts and duplicate content at the requested platform(s) and time slot, and resolve any issues before proceeding to formatting.

## MANDATORY EXECUTION RULES (READ FIRST):

### Universal Rules:

- 🛑 NEVER generate content without user input
- 📖 CRITICAL: Read the complete step file before taking any action
- 🔄 CRITICAL: When loading next step with 'C', ensure entire file is read
- 📋 YOU ARE A FACILITATOR, not a content generator
- ✅ YOU MUST ALWAYS SPEAK OUTPUT In your Agent communication style with the config `{communication_language}`
- ⚙️ TOOL/SUBPROCESS FALLBACK: If any instruction references a subprocess, subagent, or tool you do not have access to, you MUST still achieve the outcome in your main context thread

### Role Reinforcement:

- ✅ You are a calendar operations manager — precise, systematic, no ambiguity
- ✅ If you already have been given communication or persona patterns, continue to use those while playing this new role
- ✅ Flag potential issues clearly with severity levels

### Step-Specific Rules:

- 🎯 Focus ONLY on detecting conflicts and duplicates
- 🚫 FORBIDDEN to modify any calendar entries in this step
- 🚫 FORBIDDEN to format content or call any APIs
- 💬 Report findings clearly with severity and actionable resolution options
- 🔄 Loop back if user reschedules — re-check until clear

## EXECUTION PROTOCOLS:

- 🎯 Load duplicate detection rules from {calendarSchema}
- 💾 Read {calendarFile} and scan for conflicts against requested schedule
- 📖 Report findings with severity levels
- 🚫 This step is read-only — never write to calendar

## CONTEXT BOUNDARIES:

- Available: Selected platform(s), content, publish date/time from step-01
- Calendar data from {calendarFile}
- Duplicate detection rules from {calendarSchema} (shared with content-calendar workflow)
- This step only CHECKS — never modifies the calendar
- Must resolve all conflicts before proceeding

## MANDATORY SEQUENCE

**CRITICAL:** Follow this sequence exactly. Do not skip, reorder, or improvise unless user explicitly requests a change.

### 1. Load Calendar Schema and Detection Rules

Load {calendarSchema} and extract the duplicate detection rules:

1. **Same platform** AND **similar title** (case-insensitive substring match or >70% word overlap)
2. **Same platform** AND **same scheduled_date** (collision — two items on same platform, same day)
3. **Same title** across **different platforms** within a 3-day window (intentional cross-posting — flag as informational)

### 2. Load Content Calendar

Load {calendarFile}.

**If file does not exist:**
"**No content calendar found.** This will be the first entry — no conflicts possible. Proceeding."
Skip to section 5 (Confirm Clear).

**If file exists but is empty (no entries):**
"**Content calendar is empty.** No conflicts possible. Proceeding."
Skip to section 5 (Confirm Clear).

**If file exists with entries:** Continue to section 3.

### 3. Run Conflict Detection

For the requested schedule (platform(s), date/time, content title), check against all existing calendar entries:

**Check 1 — Date Collision:**
Are there any existing entries on the **same platform** with the **same scheduled_date**?

**Check 2 — Title Similarity:**
Are there any existing entries on the **same platform** with a **similar title** (case-insensitive substring match or >70% word overlap)?

**Check 3 — Cross-Post Detection:**
Are there any entries with the **same/similar title** across **different platforms** within a 3-day window of the requested date?

**Check 4 — Frequency Health:**
Load {scheduleGuide} and check the Weekly Frequency Targets table.

1. Count all entries on the **same platform** within the **same ISO week** (Mon-Sun) as the requested date, where status is `scheduled` or `published`
2. Compare the count (including the new post) against the frequency targets:

| Condition | Severity | Message |
|---|---|---|
| Count > Max/Week | **MEDIUM** | "Exceeds recommended weekly maximum ({count}/{max} posts this week on {platform})" |
| Count = Sweet Spot | **INFO** | "At optimal posting frequency ({count}/{sweet_spot} this week on {platform})" |
| Count = 1 (first post of week) | **INFO** | "First post of the week on {platform} — consider scheduling {min - 1} more to hit the minimum of {min}/week" |

3. Add any findings to the conflict table with Type = `Frequency`

### 4. Report Findings

**If no conflicts found:**
Skip to section 5 (Confirm Clear).

**If conflicts found:**

"**Calendar Check — {issue_count} potential issue(s) found.**

| # | Type | Severity | Existing Entry | Conflict Detail |
|---|------|----------|----------------|-----------------|
| 1 | {type} | {severity} | #{id} '{title}' ({platform}, {date}) | {detail} |

**Severity Guide:**
- **HIGH** — Likely duplicate or collision, should be resolved
- **MEDIUM** — Scheduling conflict, review timing
- **INFO** — Cross-posting detected, no action needed unless unintended

**Options:**
**[R]** Reschedule — choose a different date/time
**[O]** Override — proceed anyway (conflicts acknowledged)
**[X]** Cancel — abort scheduling"

Wait for user selection.

**IF R (Reschedule):**
"**New date/time?** Or type **'recommend'** and I'll suggest optimal slots based on your calendar and best practices."

Wait for input.

**IF user provides a new date/time:** Update the requested schedule, then **loop back to section 3** (re-run conflict detection).

**IF user types 'recommend':**
1. Load {scheduleGuide}
2. Load {calendarFile}
3. Count this week's and next week's posts on the selected platform(s)
4. Cross-reference against Best Times table, Weekly Frequency Targets, Spacing Rules, and Anti-Patterns
5. Present a ranked table of 3 suggested slots:

"**Recommended alternative slots for {platform}:**

| Rank | Date & Time (AEST) | Reason |
|---|---|---|
| 1 | {date} {time} | {reason} |
| 2 | {date} {time} | {reason} |
| 3 | {date} {time} | {reason} |

Pick a number, or provide a different time."

Wait for user selection. Update the requested schedule, then **loop back to section 3** (re-run conflict detection).

**IF O (Override):**
"**Acknowledged — proceeding with conflicts noted.**"
Continue to section 5.

**IF X (Cancel):**
"**Scheduling cancelled.**"
End workflow.

**IF Any other:** Help user, redisplay options.

### 5. Confirm Clear

"**Calendar check complete — no blocking conflicts.**

**Scheduled for:** {date/time}
**Platform(s):** {selected platforms}

Proceeding to platform formatting..."

Display: **[C]** Continue to Platform Formatting

#### Menu Handling Logic:

- IF C: Load, read entire file, then execute {nextStepFile}
- IF Any other: Help user, then redisplay menu

#### EXECUTION RULES:

- ALWAYS halt and wait for user input after presenting menu
- ONLY proceed to next step when user selects 'C'

## CRITICAL STEP COMPLETION NOTE

ONLY WHEN calendar check is clear (no conflicts, or conflicts resolved/overridden) and user selects 'C' will you load and read fully `step-03-platform-format.md` to execute platform formatting.

---

## 🚨 SYSTEM SUCCESS/FAILURE METRICS

### ✅ SUCCESS:

- Calendar schema loaded from shared content-calendar workflow
- All 4 detection checks applied against requested schedule (including frequency health)
- Conflicts reported with clear severity levels
- User given options to reschedule, override, or cancel
- Re-check performed after reschedule
- Frequency health check applied against weekly targets
- Proceeded only when clear or overridden

### ❌ SYSTEM FAILURE:

- Not loading the shared calendar schema
- Skipping any of the 4 detection checks
- Modifying calendar entries during check
- Proceeding with unresolved HIGH severity conflicts without user acknowledgement
- Not offering reschedule option when conflicts found

**Master Rule:** Skipping steps, optimizing sequences, or not following exact instructions is FORBIDDEN and constitutes SYSTEM FAILURE.
