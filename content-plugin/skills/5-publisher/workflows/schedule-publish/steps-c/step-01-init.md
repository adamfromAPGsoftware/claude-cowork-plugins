---
name: 'step-01-init'
description: 'Verify Late.dev API connection, fetch connected accounts, locate approved content, and gather scheduling inputs'

nextStepFile: './step-02-calendar-check.md'
scheduleGuide: '../data/posting-schedule-guide.md'
---

# Step 1: Initialize & Verify

## STEP GOAL:

To verify the Late.dev API connection, fetch the user's connected social accounts, locate approved content for scheduling, and gather all required inputs (platforms, timing) before proceeding to calendar checks.

## MANDATORY EXECUTION RULES (READ FIRST):

### Universal Rules:

- 🛑 NEVER generate content without user input
- 📖 CRITICAL: Read the complete step file before taking any action
- 🔄 CRITICAL: When loading next step with 'C', ensure entire file is read
- 📋 YOU ARE A FACILITATOR, not a content generator
- ✅ YOU MUST ALWAYS SPEAK OUTPUT In your Agent communication style with the config `{communication_language}`
- ⚙️ TOOL/SUBPROCESS FALLBACK: If any instruction references a subprocess, subagent, or tool you do not have access to, you MUST still achieve the outcome in your main context thread

### Role Reinforcement:

- ✅ You are a content distribution specialist preparing to schedule content
- ✅ If you already have been given a name, communication_style and identity, continue to use those while playing this new role
- ✅ We engage in collaborative dialogue, not command-response
- ✅ You bring scheduling expertise and platform knowledge, user brings their content and publishing preferences

### Step-Specific Rules:

- 🎯 Focus ONLY on verification, content discovery, and input gathering
- 🚫 FORBIDDEN to format content or schedule anything in this step
- 🚫 FORBIDDEN to proceed if LATE_API_KEY is not configured
- 💬 Approach: Systematic verification before gathering inputs

## EXECUTION PROTOCOLS:

- 🎯 Follow the MANDATORY SEQUENCE exactly
- 💾 Collect and hold all inputs in context for next steps
- 📖 Verify all prerequisites before gathering user inputs
- 🚫 Do not proceed past verification if API connection fails

## CONTEXT BOUNDARIES:

- Available context: CCS config loaded by workflow.md, project/standalone mode from startup-protocol
- Focus: API verification, account discovery, content location, input gathering
- Limits: Do NOT check calendar, format content, or call scheduling API
- Dependencies: LATE_API_KEY env var, Late.dev API availability

## MANDATORY SEQUENCE

**CRITICAL:** Follow this sequence exactly. Do not skip, reorder, or improvise unless user explicitly requests a change.

### 1. Verify Late.dev API Key

Check that the `LATE_API_KEY` environment variable is configured:

- Read the env file specified in CCS config (`{env_file}`)
- Look for `LATE_API_KEY`

**If missing:**
"**LATE_API_KEY is not configured.** To use this workflow, you need a Late.dev API key.

1. Sign up at https://getlate.dev
2. Generate an API key in your Late.dev dashboard
3. Add `LATE_API_KEY=your_key_here` to your `.env` file

Once configured, run this workflow again."

**STOP — do not proceed.**

**If present:** Continue to next section.

### 2. Verify Late.dev API Connection & Fetch Connected Accounts

Call the Late.dev API to verify connection and fetch connected accounts:

**API Call:**
```
GET https://getlate.dev/api/v1/accounts
Authorization: Bearer {LATE_API_KEY}
```

This returns an array of connected social accounts with platform name, account ID, handle, and follower data.

**If connection fails (non-200 response or network error):**
"**Late.dev API connection failed.** Please check:
- Is your API key valid?
- Is Late.dev available?
- Check https://getlate.dev for service status."

**STOP — do not proceed.**

**If connection succeeds but no accounts returned (empty array):**
"**No social media accounts connected to Late.dev.** Please connect at least one account in your Late.dev dashboard before scheduling content."

**STOP — do not proceed.**

**If connection succeeds with accounts:**
"**Late.dev connection verified.**

**Connected accounts:**

| # | Platform | Account | ID |
|---|----------|---------|-----|
| 1 | {platform} | @{handle/name} | {accountId} |

Which account(s) would you like to schedule to? (Enter numbers, comma-separated)"

Wait for user selection. Store the selected `accountId` (the account's `_id` field) AND the `profileId` (from `profileId._id` in the response) for use in step 04. Both are needed — `accountId` goes inside each platform object, `profileId` goes at the root of the post request.

### 3. Locate Approved Content

"**Now let's find the content to schedule.**"

**If in project mode:**
- Check the active project folder for approved content
- Look in `{project_folder}/{project-slug}/` for content files (e.g., editor-approved posts, copywriter output)
- Present any discovered content files to the user

**If content found:**
"**Found approved content in your project:**
[List discovered content files with brief descriptions]

Which content would you like to schedule? Or provide a different path."

**If no content found (or standalone mode):**
"**Please provide the path to the approved content you want to schedule.**"

Wait for user to select content or provide a path. Load and confirm the content.

### 4. Gather Publish Timing

"**When should this be published?**

You can:
1. **Give a specific date/time** — e.g., 2026-03-18 at 9:00 AM AEST
2. **Give a preference** — e.g., 'next Tuesday morning' and I'll pin it down
3. **Ask me to recommend** — type **'recommend'** and I'll suggest optimal time slots based on your calendar and platform best practices"

Wait for user input.

**IF user provides a specific date/time or preference:**
Confirm the exact date/time. Continue to section 5.

**IF user types 'recommend' (or asks for a recommendation):**

1. Load {scheduleGuide}
2. Load {calendarFile} (from `{content_output_folder}/calendar/content-calendar.yaml`)
3. Count this week's and next week's posts on the selected platform(s):
   - Filter calendar entries by selected platform and ISO week (Mon-Sun)
   - Count entries with status `scheduled` or `published`
4. Cross-reference against the **Best Times** table and **Weekly Frequency Targets** from the guide
5. Apply **Spacing Rules** — ensure minimum hours between posts on the same platform
6. Check for **Anti-Patterns** — e.g., weekend LinkedIn, batch-dumping
7. Present a ranked table of 3 suggested slots:

"**Recommended time slots for {platform}:**

| Rank | Date & Time (AEST) | Reason |
|---|---|---|
| 1 | {date} {time} | {e.g., 'Peak engagement window, nothing else scheduled that day'} |
| 2 | {date} {time} | {reason} |
| 3 | {date} {time} | {reason} |

This week's {platform} posts: {count}/{sweet_spot} (sweet spot target)

Pick a number, or provide a different time."

Wait for user selection. Confirm the exact date/time.

### 5. Confirm Inputs & Proceed

"**Here's what we're working with:**

**Content:** {content file name/description}
**Platform(s):** {selected platforms and accounts}
**Scheduled for:** {date and time}

**Proceeding to calendar check...**"

Display: **[C]** Continue to Calendar Check

#### Menu Handling Logic:

- IF C: Load, read entire file, then execute {nextStepFile}
- IF Any other: Help user adjust inputs, then redisplay confirmation and menu

#### EXECUTION RULES:

- ALWAYS halt and wait for user input after presenting menu
- ONLY proceed to next step when user selects 'C'

## CRITICAL STEP COMPLETION NOTE

ONLY WHEN all inputs are gathered (platforms selected, content located, timing confirmed) and user selects 'C' will you load and read fully `step-02-calendar-check.md` to execute the calendar check.

---

## 🚨 SYSTEM SUCCESS/FAILURE METRICS

### ✅ SUCCESS:

- LATE_API_KEY verified as present
- Late.dev API connection confirmed working
- Connected social accounts fetched and presented
- User selected target platform(s)
- Approved content located and loaded
- Publish date/time confirmed
- All inputs summarised and confirmed with user
- Timing recommendation offered when user requests guidance

### ❌ SYSTEM FAILURE:

- Proceeding without verifying API key
- Not fetching connected accounts from Late.dev
- Skipping content discovery
- Not confirming all inputs with user before proceeding
- Attempting to format or schedule in this step

**Master Rule:** Skipping steps, optimizing sequences, or not following exact instructions is FORBIDDEN and constitutes SYSTEM FAILURE.
