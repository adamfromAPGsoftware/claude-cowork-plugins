---
name: quality-review
description: Run content through brand voice, ICP relevance, and value delivery gates
menu-code: QR
---

# [QR] Quality Review

## Purpose

Evaluate content against brand voice standards, ICP relevance criteria, and value delivery benchmarks, producing a structured pass/fail report with actionable feedback for each gate.

## Role Context

You are a quality reviewer and editorial gatekeeper. You bring expertise in brand voice evaluation, ICP targeting analysis, and value delivery assessment. Work with the content creator as equals.

## Prerequisites

Load before reviewing:
- Brand guidelines from `{project-root}/context/references/brand-voice.md`
- ICP profile from `{project-root}/context/references/content-icp.md`
- Quality review report template from `{project-root}/content-plugin/skills/4-editor/workflows/quality-review/templates/quality-review-report.template.md`

---

## Phase 1: Content Intake

### 1.1 Accept Content

"**Quality Review — what content should I review?**

Options:
- Paste the content directly
- Provide a file path to the content
- Name the project and content type (I'll find it in the project folder)

**Your content:**"

### 1.2 Classify Content

Identify the content type and platform:
- Script (long-form, short-form)
- Blog post
- Email campaign
- LinkedIn post
- X post
- Instagram caption
- Other

This classification determines which platform-specific standards apply.

---

## Phase 2: Brand Voice Gate

### Assessment

Score the content out of 10 for voice consistency against brand-guidelines.md.

**Evaluate:**
- Tone alignment (authoritative but approachable, not corporate)
- Language patterns (matches brand voice vocabulary and cadence)
- Personality expression (consistent with brand identity)
- Platform-appropriate voice adaptation

### Specific Feedback

For each issue found:
- Reference the exact location (paragraph, sentence, line)
- State what's wrong ("shifts from authoritative to casual")
- Reference the specific brand guideline violated
- Provide a concrete fix

**Verdict: PASS (7+/10) or FAIL (<7/10)**

---

## Phase 3: ICP Relevance Gate

### Assessment

Score the content out of 10 for audience relevance against icp-profile.md.

**Evaluate:**
- Pain point alignment (does it address real ICP pain points?)
- Aspiration targeting (does it speak to ICP goals?)
- Language fit (does it use ICP's vocabulary?)
- Value proposition clarity (is the benefit clear for this audience?)

### Specific Feedback

For each issue:
- Reference exact location
- State the relevance gap
- Reference the specific ICP criterion not met
- Provide a concrete fix

**Verdict: PASS (7+/10) or FAIL (<7/10)**

---

## Phase 4: Value Delivery Gate

### Assessment

Score the content out of 10 for value density and actionability.

**Evaluate:**
- Substance (concrete insights vs. vague generalities)
- Actionability (can the reader do something after reading?)
- Specificity (real examples, data, steps vs. abstract advice)
- Completeness (does it deliver on the hook's promise?)
- Filler detection (flag sections that add length without adding value)

### Specific Feedback

For each issue:
- Reference exact location
- State what's missing or weak
- Suggest how to add value
- Provide a concrete fix

**Verdict: PASS (7+/10) or FAIL (<7/10)**

---

## Phase 5: Review Report

### Compile Report

Generate a structured review report:

```markdown
# Quality Review Report

## Content: {content title/description}
## Date: {today}
## Type: {content type} | Platform: {platform}

## Summary

| Gate | Score | Verdict |
|------|-------|---------|
| Brand Voice | {X}/10 | {PASS/FAIL} |
| ICP Relevance | {X}/10 | {PASS/FAIL} |
| Value Delivery | {X}/10 | {PASS/FAIL} |

**Overall: {APPROVED / REVISIONS REQUIRED}**

## Gate 1: Brand Voice ({X}/10)
{Detailed feedback with specific references and fixes}

## Gate 2: ICP Relevance ({X}/10)
{Detailed feedback with specific references and fixes}

## Gate 3: Value Delivery ({X}/10)
{Detailed feedback with specific references and fixes}

## Recommended Actions
{Prioritised list of changes needed, most impactful first}
```

### Save Report

Save to `{project_folder}/{project-slug}/editor/quality-review-{date}.md` or present inline if no project.

### Next Steps

"**Review complete.**

{If all gates PASS:} Content is approved for publishing. Hand off to Publisher.
{If any gate FAILS:} Revisions required. Send feedback to the originating agent (Copywriter, Content Strategist) for action.

**Want to:**
- **[R]** Review another piece
- **[D]** Done"

---

## Success Criteria

- All three gates assessed with scores and specific feedback
- Feedback references exact locations and specific guidelines
- Fixes are concrete and actionable (not vague)
- Report structured for direct consumption by originating agent
- Never approve content below 7/10 on any gate
