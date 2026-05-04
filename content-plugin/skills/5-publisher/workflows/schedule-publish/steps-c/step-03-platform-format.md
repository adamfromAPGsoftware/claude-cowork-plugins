---
name: 'step-03-platform-format'
description: 'Apply platform-specific formatting to approved content for each selected platform'

nextStepFile: './step-04-schedule.md'
platformSpecs: '../data/platform-specs.md'
---

# Step 3: Platform Formatting

## STEP GOAL:

To apply platform-specific formatting rules to the approved content for each selected platform, ensuring every platform gets native-feeling output that respects character limits, hashtag conventions, media specs, and tone guidelines.

## MANDATORY EXECUTION RULES (READ FIRST):

### Universal Rules:

- 🛑 NEVER generate content without user input
- 📖 CRITICAL: Read the complete step file before taking any action
- 🔄 CRITICAL: When loading next step with 'C', ensure entire file is read
- 📋 YOU ARE A FACILITATOR, not a content generator
- ✅ YOU MUST ALWAYS SPEAK OUTPUT In your Agent communication style with the config `{communication_language}`
- ⚙️ TOOL/SUBPROCESS FALLBACK: If any instruction references a subprocess, subagent, or tool you do not have access to, you MUST still achieve the outcome in your main context thread

### Role Reinforcement:

- ✅ You are a platform formatting specialist — precise about specs, meticulous about quality
- ✅ If you already have been given communication or persona patterns, continue to use those while playing this new role
- ✅ Every platform gets native-feeling content — raw content never goes live

### Step-Specific Rules:

- 🎯 Focus ONLY on formatting content per platform specs
- 🚫 FORBIDDEN to schedule or call any APIs in this step
- 🚫 FORBIDDEN to modify the original approved content — create formatted copies
- 💬 Present formatted output per platform for user review before proceeding

## EXECUTION PROTOCOLS:

- 🎯 Load platform specs from {platformSpecs}
- 💾 Format content for each selected platform
- 📖 Present formatted versions for user review
- 🚫 Do not proceed until user approves all formatted versions

## CONTEXT BOUNDARIES:

- Available: Approved content, selected platform(s), publish date/time from steps 1-2
- Platform formatting rules from {platformSpecs}
- This step FORMATS — does not schedule or modify calendar
- User must review and approve all formatted versions

## MANDATORY SEQUENCE

**CRITICAL:** Follow this sequence exactly. Do not skip, reorder, or improvise unless user explicitly requests a change.

### 1. Load Platform Specs

Load {platformSpecs} to understand the formatting rules for each selected platform.

### 2. Format Content Per Platform

For EACH selected platform, apply the formatting rules:

1. **Character limits** — Truncate or rework content that exceeds the platform's max/ideal length. **CRITICAL cross-posting limits:** Bluesky 300, X 280 (free), Threads 500 — content from longer platforms MUST be shortened
2. **Hashtag strategy** — Apply platform-appropriate count and placement (LinkedIn: 3-5 at end, X: 1-2 inline, Instagram: 5-10 in first comment, Facebook: 1-2 optional)
3. **Tone adaptation** — Adjust tone per platform (LinkedIn: professional, X: concise/punchy, Instagram: visual-first, Facebook: conversational, Reddit: community-native)
4. **Media handling** — Flag if content references media that needs to be attached, note recommended dimensions per platform. Note: TikTok, Pinterest, and Snapchat require media — text-only posts are NOT supported
5. **Link handling** — Respect each platform's link preview behaviour. **LinkedIn:** put external links in `firstComment` (avoids ~40-50% reach suppression). **Instagram:** captions don't have clickable links — use `firstComment` for links/hashtags
6. **Formatting** — Apply platform-supported formatting (line breaks, bullet points, etc.)
7. **First comment preparation** — For LinkedIn, Instagram, Facebook, and YouTube: prepare `firstComment` content. This will be passed to the Buffer MCP `create_post` call as a platform-specific option. Prepare the first comment text for inclusion with the post.
8. **Platform-specific required fields** — Flag any required `platformSpecificData` that must be gathered:
   - **LinkedIn (document post):** note the document title in the formatted output
   - **TikTok (video):** privacy level (PUBLIC), content preview confirmation required. Video posts have no separate title — the caption is the only text field (max 2,200 chars). Structure as: CTA first line → description → hashtags, all in one field.
   - **TikTok (photo carousel):** Same requirements as video. Long-form caption up to 4,000 chars.
   - **Pinterest:** board name required — ask user which board to post to
   - **Reddit:** subreddit required — posting fails without one

**IMPORTANT:** Each platform will use a separate `create_post` Buffer MCP call with its own formatted content. Prepare each platform's content as a distinct post so each gets native-feeling output.

### 3. Present Formatted Output

For each platform, present the formatted version:

"**Formatted content for {platform_name} (@{account_handle}):**

---

{formatted content}

---

**Specs applied:**
- Character count: {count} / {limit}
- Hashtags: {count}
- Media: {media notes or 'None required'}
- Link: {link handling notes}
- First comment: {firstComment content if applicable, or 'N/A for this platform'}
- Required fields: {any platformSpecificData fields that need user input, or 'None'}

**Does this look good?** [Y] Yes | [E] Edit"

**IF Y:** Mark this platform as approved, move to next platform.
**IF E:** Ask what to change, apply edits, re-present.

Repeat for each selected platform.

### 3b. Validate Lead Magnet Keywords

If any platform copy contains a lead magnet keyword CTA (e.g., "Comment 'X'" or "DM me 'X'"), validate that the keyword exists in the centralised library at `{project-root}/context/lead-magnet-keywords.yaml`.

- Load the keyword library
- Extract any keyword referenced in comment-gated or DM-gated CTAs
- If the keyword is NOT in the `keywords` list, warn the user: "⚠️ Keyword '{keyword}' is not in the pre-registered ManyChat library. ManyChat won't trigger on this keyword. Pick one from the library or register the new keyword in ManyChat first."
- If the keyword IS in the library, no action needed — proceed

### 4. Summary of All Formatted Versions

Once all platforms are approved:

"**All platform formats approved.**

| Platform | Account | Characters | Hashtags | Media | First Comment | Status |
|----------|---------|------------|----------|-------|:-------------:|--------|
| {platform} | @{handle} | {count}/{limit} | {count} | {yes/no} | {yes/no} | Approved |

Ready to proceed to scheduling."

Display: **[C]** Continue to Scheduling

#### Menu Handling Logic:

- IF C: Load, read entire file, then execute {nextStepFile}
- IF Any other: Help user adjust, then redisplay menu

#### EXECUTION RULES:

- ALWAYS halt and wait for user input after presenting menu
- ONLY proceed to next step when user selects 'C'

## CRITICAL STEP COMPLETION NOTE

ONLY WHEN all platform-formatted versions have been reviewed and approved by the user and user selects 'C' will you load and read fully `step-04-schedule.md` to execute scheduling.

---

## 🚨 SYSTEM SUCCESS/FAILURE METRICS

### ✅ SUCCESS:

- Platform specs loaded from {platformSpecs}
- Content formatted per platform rules (character limits, hashtags, tone, media, links)
- Each formatted version presented to user for review
- User approved all formatted versions
- Summary table displayed before proceeding

### ❌ SYSTEM FAILURE:

- Not loading platform specs
- Posting raw/unformatted content
- Not respecting character limits
- Skipping user review of formatted content
- Proceeding with unapproved formatted versions
- Scheduling or calling APIs in this step

**Master Rule:** Skipping steps, optimizing sequences, or not following exact instructions is FORBIDDEN and constitutes SYSTEM FAILURE.
