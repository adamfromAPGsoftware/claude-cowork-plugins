---
name: step-07-quality
description: Brand voice + anti-AI quality gate with up to 2 auto-revision cycles
nextStep: ./step-08-queue.md
---

# Step 7: Quality Gate

## Goal

Check both drafts against the brand voice rules and the Anti-AI Red Flags filter. Auto-revise if needed (up to 2 cycles). Only pass drafts that score 7/10+ on all criteria.

## Quality Checklist

Score each criterion 1-10. Threshold: 7/10 minimum.

### Criterion 1: Voice Authenticity (threshold: 7/10)
- Reads like a human wrote it, not a language model
- No forbidden words: leverage, synergy, delve, game-changing, seamless, thought leader, ecosystem, in today's fast-paced world, it's worth noting
- Contractions present where natural
- Sentence variety — not robotically uniform length
- Numbers as numerals throughout
- No em dashes

### Criterion 2: Hook Strength (threshold: 7/10)
- First 1-2 lines stop the scroll
- Creates friction, surprise, curiosity, or a strong claim
- Does NOT open with "I" as the first word
- Does NOT start with a question
- Does NOT start with "Are you..." or "Have you ever..."
- Specific > vague ("60+ projects" > "many projects")

### Criterion 3: ICP Fit (threshold: 7/10)
- Primary audience: AI agency builders + freelancers OR SME decision makers (depending on pillar)
- Content maps to a real problem or aspiration from `{contentICP}`
- Dual-funnel check: builders see a skill, SMEs see ROI (where applicable)

### Criterion 4: CTA Compliance (threshold: 7/10 only if CTA present)
- **Keyword CTA**: ALL-CAPS keyword, 3-step structure, P.S. line
- **Resource giveaway**: link goes in `firstComment` not body, body teases the resource without a direct link
- **No CTA**: post ends with a strong statement, not an open question or vague trail-off
- **NEVER**: "What do you think?", "Have you experienced this?", "Drop your thoughts", "Let me know in the comments"

### Criterion 5: Platform Compliance (threshold: must pass)
- LinkedIn: zero hashtags (anywhere), 800-1300 chars for text, single-line paragraphs
- X: under 280 chars per tweet, or proper thread format
- No body links in LinkedIn draft (links go in firstComment only)

### Criterion 6: Style Fidelity (threshold: 7/10 — only scored if `style_profile` is not `none`)

If a style profile was selected in step-04, check that the draft follows it:
- **Hook**: does the opening line follow the style's prescribed hook type? (e.g., S1 = Gap/Contrarian or Provocative Claim; S3 = Industry Alarm + Ironic Detail; S4 = Income Claim + Deflation)
- **Structure**: does the body follow the step-by-step skeleton from `{styleProfiles}`?
- **CTA**: does the CTA type match (3-step vs single-line vs none)?
- **Format compliance**: does the draft align with the style's visual guidance (text-only for S3/S4, real photo for S5)?
- **Tone markers**: are the style's specific tone rules applied (e.g., S1's fragment sentences, S4's stacked negatives, S3's verdict pattern)?

Score: 1-10. A draft that follows generic templates but ignores the selected style profile scores 5/10 or below.

## Auto-Revision Logic

If any criterion scores below 7/10:

1. Identify the specific failing lines or phrases
2. Rewrite ONLY the failing sections — don't rewrite the whole post
3. Re-score
4. If still below 7/10 after 2 revision cycles, flag in draft frontmatter: `quality_note: "Manual review recommended — {criterion} scored {score}/10"`

Do not block the workflow if quality note is flagged — still proceed to step-08. The creator reviews everything.

## Output Summary

```
Quality gate
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
LinkedIn:
  Voice Authenticity: {score}/10 {✓|✗}
  Hook Strength:      {score}/10 {✓|✗}
  ICP Fit:            {score}/10 {✓|✗}
  CTA Compliance:     {score}/10 {✓|✗} (or N/A)
  Platform:           {pass|fail}
  Style Fidelity:     {score}/10 {✓|✗} (or N/A — no style profile)
  Overall:            {pass|needs-review}

X:
  Voice Authenticity: {score}/10 {✓|✗}
  Hook Strength:      {score}/10 {✓|✗}
  Overall:            {pass|needs-review}

{If revisions made: "Revised {N} section(s) across {M} cycle(s)"}
{If flagged: "⚠ Manual review recommended: {note}"}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

Then immediately load and execute step-08.
