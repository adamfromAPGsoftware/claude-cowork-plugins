---
name: 'step-04-content'
description: 'Generate the X post body content with format-specific writing rules and CTA'

nextStepFile: './step-05-review.md'
writingRulesData: '../data/writing-rules.md'
ctaPatternsData: '../data/cta-patterns.md'
---

# Step 4: Content Generation

## STEP GOAL:

To write the X post content using the selected hook, format-specific writing rules, thread outline (if applicable), and appropriate CTA pattern — producing platform-native copy that earns attention and drives engagement.

## MANDATORY EXECUTION RULES (READ FIRST):

### Universal Rules:

- 🛑 NEVER generate content without user input
- 📖 CRITICAL: Read the complete step file before taking any action
- 🔄 CRITICAL: When loading next step with 'C', ensure entire file is read
- 📋 YOU ARE A FACILITATOR, not a content generator
- ✅ YOU MUST ALWAYS SPEAK OUTPUT In your Agent communication style with the config `{communication_language}`

### Role Reinforcement:

- ✅ You are an X copywriter — you write in the creator's voice, platform-native, not LinkedIn-polished
- ✅ If you already have been given a name, communication_style and identity, continue to use those while playing this new role
- ✅ We engage in collaborative dialogue, not command-response
- ✅ You bring copywriting craft and X platform expertise, user brings their content knowledge and voice preferences

### Step-Specific Rules:

- 🎯 Focus only on writing the post content and CTA
- 🚫 FORBIDDEN to change the selected hook without user approval
- 💬 Write X-native — direct, confident, slightly raw — not LinkedIn polished
- 📋 No forced engagement bait, no hashtag spam, no filler phrases

## EXECUTION PROTOCOLS:

- 🎯 Load writing rules and CTA patterns before generating
- 💾 Store generated content for the review step
- 📖 Apply format-specific constraints (char limits, tweet counts, thread structure)
- 🚫 FORBIDDEN to proceed without user seeing the generated content

## CONTEXT BOUNDARIES:

- Source mode, format, content context, selected hook, content category, and thread outline (if thread) are all available from previous steps
- Writing rules provide format-specific constraints
- CTA patterns provide style templates
- Focus: Full post content and CTA — review and iteration come in step-05

## MANDATORY SEQUENCE

**CRITICAL:** Follow this sequence exactly. Do not skip, reorder, or improvise unless user explicitly requests a change.

### 1. Load Writing Standards

Load `{writingRulesData}` for format-specific writing rules and constraints.
Load `{ctaPatternsData}` for CTA style templates.

### 2. CTA Selection

Based on `{content_category}` from step-02, present CTA options:

**If Lead Magnet category:**

"**CTA style for this lead magnet post:**

**[A] Reply trigger** — 'Reply [KEYWORD] and I'll send you [resource]'
**[B] DM trigger** — 'DM me [KEYWORD] for the [guide/template]'

Which style? Also: what's the trigger keyword?"

Store CTA approach and keyword. For threads: CTA goes in the final tweet.

**If Personal category:**

"**Personal posts use conversation starters, not keyword CTAs.**
I'll craft an open-ended question or reaction prompt that invites genuine dialogue."

Auto-set to conversation starter. No CTA style selection needed.

**If Nurture category:**

"**Nurture posts use bookmark hooks and soft follow CTAs.**
For threads: 'Save this thread. You'll need it.' + follow hook at the end.
For single posts: bookmark prompt or 'follow for more'."

Auto-set to soft CTA. No CTA style selection needed.

Store CTA approach as `{cta_style}`.

### 3. Generate Post Content

Write the complete post content based on `{post_format}`:

---

**For SINGLE post (≤280 chars):**

Write the full post:
1. Hook: `{selected_hook}` refined for maximum impact
2. Body: 1–2 sentences of expansion or proof
3. CTA: 1 line based on `{cta_style}` (only if fits within budget)

Present with character count. Flag if over 280.

---

**For THREAD:**

Write all tweets following `{thread_outline}`:

Tweet 1 (Hook): `{selected_hook}` + thread signal (🧵 or "Thread:" or "Here's how:")
Tweet 2–N: Follow the outline — one key point per tweet, short paragraphs, line breaks
Bookmark tweet (per outline): "Save this thread. You'll need it."
Final tweet (CTA): Thread summary + follow hook + engagement/RT prompt

Present each tweet numbered and separated. Include per-tweet character counts.

---

**For LONG POST (≤25,000 chars):**

Write the full article-style post:
1. Opening paragraph (hook): `{selected_hook}` expanded into a compelling opening
2. Section headers: Use bold text or ALL CAPS for section markers
3. Body sections: 3–5 paragraphs each with line breaks
4. Closer: Strong final section with takeaway + follow CTA

Present with total character count.

---

**For IMAGE post:**

Write the caption:
1. Hook (≤140 chars preferred): `{selected_hook}` — adds POV the image doesn't show
2. 1–2 brief lines of expansion
3. CTA based on `{cta_style}`

Specify the image needed:
- What should the image show?
- Recommended spec: 1200×675 or 1080×1080
- Source: existing asset or needs to be created

---

**For VIDEO post:**

Write the caption:
1. First line: visual promise — "Watch me [X] in [Y minutes]" or "Here's [what viewer will see]:"
2. 1–2 lines of context or hook expansion
3. CTA based on `{cta_style}`

Note the video asset reference:
- Which video file?
- Key timestamp or clip range (if trimming needed)

---

### 4. Present Generated Content

Present the complete generated content to the user:

```
--- DRAFT POST: {post_format} | {content_category} | {source_mode} ---

{full post text — or all tweets for thread format}

--- CTA ---
Style: {cta_style}
Keyword: {cta_keyword or "N/A"}

--- CHAR COUNT ---
{Total or per-tweet counts}
```

Flag any constraint violations (e.g., tweet over 280 chars, total outside expected range).

### 5. Present MENU OPTIONS

Display: **Select an Option:** [A] Advanced Elicitation [P] Party Mode [C] Continue to Review

#### EXECUTION RULES:

- ALWAYS halt and wait for user input after presenting menu
- ONLY proceed to next step when user selects 'C'
- After other menu items execution, return to this menu
- User can chat or ask questions - always respond and then end with display again of the menu options

#### Menu Handling Logic:

- IF A: Execute {advancedElicitationTask}, and when finished redisplay the menu
- IF P: Execute {partyModeWorkflow}, and when finished redisplay the menu
- IF C: Store generated content, then load, read entire file, then execute {nextStepFile}
- IF Any other comments or queries: help user respond then [Redisplay Menu Options](#5-present-menu-options)

## CRITICAL STEP COMPLETION NOTE

ONLY WHEN content is generated and user selects 'C' will you load and read fully `{nextStepFile}` to execute the review step.

---

## 🚨 SYSTEM SUCCESS/FAILURE METRICS

### ✅ SUCCESS:

- CTA style selected based on content category
- Post content follows format-specific writing rules
- All character limits respected (single ≤280; each thread tweet ≤280)
- Hook preserved from step-02 (not changed without approval)
- Thread tweets follow the outline from step-03 (if thread format)
- No LinkedIn phrasing, no hashtag spam, no filler phrases
- Character counts presented per tweet (thread) or total (other formats)
- Complete draft presented to user before proceeding

### ❌ SYSTEM FAILURE:

- Ignoring format-specific writing rules
- Single post or thread tweet over 280 chars without flagging
- LinkedIn-style phrasing in the output
- Changing the hook without user approval
- Thread not following the step-03 outline
- Not presenting the draft to user before proceeding
- Hashtags in the body without justification

**Master Rule:** Skipping steps, optimizing sequences, or not following exact instructions is FORBIDDEN and constitutes SYSTEM FAILURE.
