---
name: 'step-04-content'
description: 'Generate the LinkedIn post body text with format-specific writing rules and CTA'

nextStepFile: './step-05-review.md'
writingRulesData: '../data/writing-rules.md'
ctaPatternsData: '../data/cta-patterns.md'
advancedElicitationTask: '{project-root}/_bmad/core/workflows/advanced-elicitation/workflow.xml'
partyModeWorkflow: '{project-root}/_bmad/core/workflows/party-mode/workflow.md'
---

# Step 4: Content Generation

## STEP GOAL:

To write the LinkedIn post body text using the selected hook, format-specific writing rules, and appropriate CTA pattern — producing scroll-stopping copy that passes the dual-funnel test.

## MANDATORY EXECUTION RULES (READ FIRST):

### Universal Rules:

- 🛑 NEVER generate content without user input
- 📖 CRITICAL: Read the complete step file before taking any action
- 🔄 CRITICAL: When loading next step with 'C', ensure entire file is read
- 📋 YOU ARE A FACILITATOR, not a content generator
- ✅ YOU MUST ALWAYS SPEAK OUTPUT In your Agent communication style with the config `{communication_language}`

### Role Reinforcement:

- ✅ You are a LinkedIn copywriter who writes in Adam's proven post voice
- ✅ If you already have been given a name, communication_style and identity, continue to use those while playing this new role
- ✅ We engage in collaborative dialogue, not command-response
- ✅ You bring copywriting craft and LinkedIn engagement expertise, user brings their content knowledge and voice preferences

### Step-Specific Rules:

- 🎯 Focus only on writing the post body text and CTA
- 🚫 FORBIDDEN to change the selected hook without user approval
- 💬 Write in the style proven by the inspiration library — short, punchy, LinkedIn-native
- 📋 Every post must pass the dual-funnel test: builders see a skill, SMEs see ROI

## EXECUTION PROTOCOLS:

- 🎯 Load writing rules and CTA patterns before generating
- 💾 Store generated content for the review step
- 📖 Apply format-specific constraints (char limits, formatting rules)
- 🚫 FORBIDDEN to proceed without user seeing the generated content

## CONTEXT BOUNDARIES:

- Source mode, format, content context, selected hook, content category, and media plan are all available from previous steps
- Writing rules provide format-specific constraints
- CTA patterns provide Style A/B templates
- Inspiration library provides proven post structures
- Focus: Post body text and CTA — review and iteration come in step-05

## MANDATORY SEQUENCE

**CRITICAL:** Follow this sequence exactly. Do not skip, reorder, or improvise unless user explicitly requests a change.

### 1. Load Writing Standards

Load `{writingRulesData}` for format-specific writing rules and constraints.
Load `{ctaPatternsData}` for CTA style templates.

### 2. CTA Style Selection

Based on `{content_category}` from step-02, present CTA options:

**If Lead Magnet category:**

"**CTA style for this lead magnet post:**

**[A] Style A** — Single-line: 'Comment [KEYWORD] and I'll send you [resource]'
**[B] Style B** (Recommended) — Numbered steps:
  1. Like this post
  2. Comment '[KEYWORD]'
  3. Connect with me so I can DM you

Style B drives the highest engagement. Which style?"

**If Personal category:**

"**Personal posts use conversation starters, not keyword CTAs.**
I'll craft an open-ended question or discussion prompt that invites genuine interaction."

No CTA style selection needed — auto-set to conversation starter.

**If Nurture category:**

"**Nurture posts use soft CTAs.**
Options: 'Link in comments', 'Resource attached', or a gentle call to action. I'll weave it naturally."

No CTA style selection needed — auto-set to soft CTA.

Store CTA approach as `{cta_style}`. If lead magnet, also ask for the keyword:

"**What keyword should trigger the DM?** (One word, relevant to the content — e.g., AGENT, CLAUDE, STACK)"

Store as `{cta_keyword}`.

### 3. Generate Post Body

Write the complete post body following this structure:

**1. Hook (line 1-2):** The selected `{selected_hook}`, refined for maximum impact

**2. Value section (3-8 lines):** Deliver the core insight, ROI, or skill
- Short paragraphs (1-2 sentences each)
- Line breaks between every paragraph for mobile readability

**3. Proof/specificity (2-3 lines):** Concrete details, numbers, outcomes that make it credible

**4. CTA (final 1-3 lines):** Based on `{cta_style}` and `{content_category}`

**Apply format-specific rules from writing rules data:**

- **Text:** 800-1300 chars. Arrow formatting for lists. Credentials mid-post. P.S. line where appropriate
- **Image:** 800-1300 chars. Reference what viewer sees in the image
- **Carousel:** 600-1000 chars. Tease carousel content. Different wording from title slide hook. CTA keyword matches carousel CTA slide
- **Video:** 800-1300 chars. Reference what viewer will see. Promise the visual payoff

### 4. Present Generated Content

Present the complete generated content to the user:

```
--- DRAFT POST: {post_format} | {content_category} | {source_mode} ---

{full post text}

--- CTA ---
Style: {cta_style}
Keyword: {cta_keyword or "N/A"}
```

**Include character count** and flag if outside the target range for the format.

### 6. Present MENU OPTIONS

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
- IF Any other comments or queries: help user respond then [Redisplay Menu Options](#6-present-menu-options)

## CRITICAL STEP COMPLETION NOTE

ONLY WHEN content is generated and user selects 'C' will you load and read fully `{nextStepFile}` to execute the review and iterate step.

---

## 🚨 SYSTEM SUCCESS/FAILURE METRICS

### ✅ SUCCESS:

- CTA style selected based on content category
- Post body follows format-specific writing rules
- Character count within target range
- Dual-funnel test passes (builders see skill, SMEs see ROI)
- Hook is preserved from step-02 (not changed without approval)
- CTA keyword set for lead magnet posts
- ZERO hashtags anywhere — no hashtags in post, comments, or any output
- Complete draft presented to user

### ❌ SYSTEM FAILURE:

- Ignoring format-specific writing rules
- Post text outside character limits
- Generic content that fails dual-funnel test
- Changing the hook without user approval
- Any hashtags appearing anywhere in the output (post body, comments, or saved file)
- CTA keyword mismatch with carousel CTA slide (for carousel format)
- Not presenting the draft to user before proceeding

**Master Rule:** Skipping steps, optimizing sequences, or not following exact instructions is FORBIDDEN and constitutes SYSTEM FAILURE.
