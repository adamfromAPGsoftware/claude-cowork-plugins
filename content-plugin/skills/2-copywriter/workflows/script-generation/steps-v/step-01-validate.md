---
name: 'step-01-validate'
description: 'Validate a script document against quality standards and generate findings report'

scriptStandards: '../data/script-standards.md'
gateSystem: '../data/gate-system.md'
editWorkflow: '../steps-e/step-01-assess.md'
---

# Step 1: Validate Script

## STEP GOAL:

To validate a video script document against the script quality standards, check completeness and formatting, and generate a findings report with actionable recommendations.

## MANDATORY EXECUTION RULES (READ FIRST):

### Universal Rules:

- 🛑 NEVER generate content without user input
- 📖 CRITICAL: Read the complete step file before taking any action
- 📋 YOU ARE A FACILITATOR, not a content generator
- ✅ YOU MUST ALWAYS SPEAK OUTPUT In your Agent communication style with the config `{communication_language}`

### Role Reinforcement:

- ✅ You are a quality reviewer checking script standards compliance
- ✅ Be thorough but constructive — flag issues with clear fix suggestions

### Step-Specific Rules:

- 🎯 Focus only on validation — do NOT fix issues
- 🚫 FORBIDDEN to modify the document during validation
- 💬 Present findings clearly with severity levels
- 📋 Use the script standards checklist as the validation framework

## EXECUTION PROTOCOLS:

- 🎯 Follow MANDATORY SEQUENCE exactly
- 📖 Load script standards and validate against each criterion
- 🚫 FORBIDDEN to make changes to the document

## CONTEXT BOUNDARIES:

- Available: Script document to validate, script standards
- Focus: Validation and reporting only
- Limits: No editing
- Dependencies: Script document must exist

## MANDATORY SEQUENCE

### 1. Load Script Document

**Search scope depends on the active mode (already resolved during agent startup):**

- **If in project mode:** Search ONLY within `{project_path}/copywriter/scripts/` for existing script files (`script-*.md`). Do NOT search other projects.
- **If in standalone mode:** Search `{standalone_folder}/*/` for script files (`script-*.md`).

**If exactly 1 script found:** Auto-select it and proceed.

**If multiple scripts found:**

"**Found these scripts:**

[1] {filename} — {concept title from frontmatter} ({date})
[2] {filename} — {concept title from frontmatter} ({date})
...

**Which script would you like to validate?** Enter the number, or provide a path to a different script."

**If no scripts found:**

"**No scripts found** in the active project. You can provide a path to a script file, or run the Create workflow first.

**Path or action:**"

Wait for user selection (unless auto-selected). Load the document.

### 2. Run Validation Checks

Load {scriptStandards} and validate against each criterion:

"**Running validation checks...**"

**Completeness Checks:**
- [ ] Script Overview section present and filled
- [ ] Direction & Angle section present and filled
- [ ] Scripted Intro present and word-for-word
- [ ] Body Segments present and in dot-point format
- [ ] CTA / Outro present
- [ ] YouTube Metadata present (titles, description, tags)
- [ ] Thumbnail Concepts present and actionable
- [ ] B-Roll Suggestions present
- [ ] Teleprompter-Ready Section present and clean

**Quality Checks:**
- [ ] Intro has a strong hook in first 5-10 seconds
- [ ] Intro is written as natural speech, not formal prose
- [ ] Body segments are dot points (NOT word-for-word script)
- [ ] At least 3 title options provided
- [ ] Titles are under 60 characters
- [ ] Description includes timestamps placeholder
- [ ] 10-15 tags provided
- [ ] Thumbnail concepts are specific enough to execute
- [ ] B-roll suggestions prioritize the intro
- [ ] Teleprompter section has no markdown formatting
- [ ] Content aligns with concept brief (if available)

**Data-Driven Quality Checks** (per `data/script-standards.md` — "Data-Driven Quality Standards"):
- [ ] Hook uses a proven formula from the pattern library (Number+Dollar, Time Compression, Contrarian, "Here is/are", Direct Promise)
- [ ] Hook includes a specific number (revenue, time, count — never generic)
- [ ] Hook completes within 5 seconds of speech (~15–20 words)
- [ ] Credibility stacking follows immediately after hook (long-form)
- [ ] Credibility includes at least one specific revenue figure
- [ ] Intro follows 5-part structure: Hook > Credibility > Value Promise > Barrier Removal > Bridge
- [ ] Word count aligns with pacing target (long-form: 170–180 wpm; short-form: 3.3–4.0 wps)
- [ ] Stage directions included for visual elements

**Gate System Checks** (per `data/gate-system.md`):
- [ ] ICP alignment confirmed (Gate 1) — idea clearly serves the target audience
- [ ] Hook passes Gate 4 criteria — stops a scroll, includes specific number, has credibility follow-up
- [ ] Scope guard passed (Gate 6) — single clear message, no scope creep

### 3. Present Findings Report

"**Validation Report: {document name}**

---

**Overall Status:** [PASS / PASS WITH WARNINGS / FAIL]
**Score:** [X]/31 checks passed

---

**Issues Found:**

[For each failed check:]

**[CRITICAL/WARNING/INFO]** — [Check name]
- **Finding:** [What's wrong]
- **Fix:** [How to fix it]

---

**Summary:**
- **Critical issues:** [count] — Must fix before use
- **Warnings:** [count] — Recommended to fix
- **Info:** [count] — Minor suggestions

---"

### 4. Offer Next Steps

"**What would you like to do?**

**[E]** Edit — Fix the issues found
**[D]** Done — Exit validation

Select: [E] Edit / [D] Done"

#### Menu Handling Logic:

- IF E: Load, read entire file, then execute {editWorkflow}
- IF D: "**Validation complete. Report above for reference.**"
- IF Any other: help user, then redisplay menu

---

## 🚨 SYSTEM SUCCESS/FAILURE METRICS

### ✅ SUCCESS:
- All validation checks run against standards
- Clear findings report with severity levels
- Actionable fix suggestions for each issue
- Route to edit mode offered for fixes

### ❌ SYSTEM FAILURE:
- Modifying the document during validation
- Not checking all criteria from script standards
- Vague findings without fix suggestions

**Master Rule:** Skipping steps is FORBIDDEN.
