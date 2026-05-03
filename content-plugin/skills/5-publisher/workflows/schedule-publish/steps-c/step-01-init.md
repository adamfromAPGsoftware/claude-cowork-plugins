---
name: 'step-01-init'
description: 'Verify Buffer connection, fetch connected channels, locate approved content, and gather scheduling inputs'

nextStepFile: './step-02-calendar-check.md'
scheduleGuide: '../data/posting-schedule-guide.md'
---

# Step 1: Initialize & Verify

## STEP GOAL:

To verify the Buffer MCP connection, fetch the user's connected social channels, locate approved content for scheduling, and gather all required inputs (platforms, timing) before proceeding to calendar checks.

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
- 🚫 FORBIDDEN to proceed if Buffer MCP connection fails
- 💬 Approach: Systematic verification before gathering inputs

## EXECUTION PROTOCOLS:

- 🎯 Follow the MANDATORY SEQUENCE exactly
- 💾 Collect and hold all inputs in context for next steps
- 📖 Verify all prerequisites before gathering user inputs
- 🚫 Do not proceed past verification if Buffer connection fails

## CONTEXT BOUNDARIES:

- Available context: CCS config loaded by workflow.md, project/standalone mode from startup-protocol
- Focus: Buffer verification, channel discovery, content location, input gathering
- Limits: Do NOT check calendar, format content, or call scheduling API
- Dependencies: Buffer MCP availability (platform-level — no env var required)

## MANDATORY SEQUENCE

**CRITICAL:** Follow this sequence exactly. Do not skip, reorder, or improvise unless user explicitly requests a change.

### 1. Verify Buffer MCP Connection

The Buffer MCP is connected at the platform level — no API key or `.env` entry is required. Proceed directly to fetching channels. If the MCP call fails, halt and report the error.

### 2. Fetch Connected Channels

Call the Buffer MCP to fetch connected channels:

**MCP Call:**
```
mcp__buffer__use_buffer_api(action: "listChannels")
```

This returns an array of connected social channels with platform name, channel ID, and handle.

**If connection fails (error or no response):**
"**Buffer MCP connection failed.** Please check:
- Is the Buffer MCP connected in Claude Code settings?
- Run `/content:0-setup` and verify Buffer MCP connectivity."

**STOP — do not proceed.**

**If connection succeeds but no channels returned:**
"**No social channels connected to Buffer.** Please connect at least one social account in your [Buffer dashboard](https://buffer.com) before scheduling content."

**STOP — do not proceed.**

**If connection succeeds with channels:**
"**Buffer connection verified.**

**Connected channels:**

| # | Platform | Account | Channel ID |
|---|----------|---------|------------|
| 1 | {platform} | @{handle/name} | {channelId} |

Which channel(s) would you like to schedule to? (Enter numbers, comma-separated)"

Wait for user selection. Store the selected `channelId` values for use in step 04.

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
**Platform(s):** {selected platforms and channels}
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

ONLY WHEN all inputs are gathered (channels selected, content located, timing confirmed) and user selects 'C' will you load and read fully `step-02-calendar-check.md` to execute the calendar check.

---

## 🚨 SYSTEM SUCCESS/FAILURE METRICS

### ✅ SUCCESS:

- Buffer MCP connection confirmed working
- Connected social channels fetched and presented
- User selected target platform(s)
- Approved content located and loaded
- Publish date/time confirmed
- All inputs summarised and confirmed with user
- Timing recommendation offered when user requests guidance

### ❌ SYSTEM FAILURE:

- Proceeding without attempting Buffer MCP connectivity check
- Not fetching connected channels from Buffer
- Skipping content discovery
- Not confirming all inputs with user before proceeding
- Attempting to format or schedule in this step

**Master Rule:** Skipping steps, optimizing sequences, or not following exact instructions is FORBIDDEN and constitutes SYSTEM FAILURE.
