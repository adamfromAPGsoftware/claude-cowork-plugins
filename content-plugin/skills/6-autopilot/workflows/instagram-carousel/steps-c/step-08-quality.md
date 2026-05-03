---
name: step-08-quality
description: Quality gate — brand voice, hook strength, CTA compliance, visual consistency
nextStep: ./step-09-queue.md
---

# Step 8: Quality Gate

## Goal

Score the carousel on copy quality and visual brand consistency. Auto-revise captions that fail. Flag visual issues for manual review.

## Sequence

### 1. Copy Quality Checks

Score each dimension 1-10 (threshold: 7):

**Voice Authenticity (weight: high)**
- Does it sound like the creator — direct, specific, no hedging?
- No banned phrases from the Anti-AI filter?
- Contractions where natural?
- Numbers instead of words for quantities?

**Hook Strength (weight: high)**
- Does slide 1 headline stop a scroll?
- Is it a claim/stat, not a question?
- Under 8 words?
- Specific enough to be credible?

**CTA Compliance (weight: medium)**
- Is the keyword CTA present in both caption and CTA slide?
- No open-ended questions as the primary CTA?
- Does the offer clearly match what "Comment X" delivers?

**Instagram Caption**
- Hook line shows before "more" (short enough)?
- 3-5 relevant hashtags (not generic solo #AI)?
- No link in the caption body?
- 150-300 words?

**TikTok Caption**
- Under 150 words?
- "Link in bio" instead of comment keyword?
- Punchier/more casual tone than Instagram?

### 2. Visual Quality Check

Read the generated slide PNGs (Claude is multimodal — use the Read tool on each PNG).

Check:
- Dark background present (#0D0D0D or similar)?
- DM Sans or bold sans-serif typography?
- Text readable at thumbnail size?
- Neon lime / green accent visible (#90F23C)?
- No unintended white backgrounds or clipped text?
- Slide count matches plan?

Visual issues are flagged for human review in the draft — they don't block queueing.

### 3. Auto-Revise if Needed

If copy score is below 7 on Voice or Hook:
- Rewrite the failing element (up to 2 revision cycles)
- Apply specific brand voice rules from `{brandVoice}`
- Re-score after each revision

If copy still fails after 2 revisions:
- Queue with `quality_note` flagging the issue
- Creator reviews before scheduling

### 4. Calculate Final Score

```
quality_score = "Instagram {score}/10 | TikTok {score}/10 | Visual {OK|REVIEW}"
passed = both captions >= 7 (visual issues don't block)
```

### 5. Output Summary

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Quality Gate
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Instagram caption: {score}/10 {PASS|FAIL}
TikTok caption:    {score}/10 {PASS|FAIL}
Visual slides:     {OK | REVIEW NEEDED}
Revisions made:    {N}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
{if quality_note: "⚠ Note: {quality_note}"}
```

Then immediately load and execute step-09.
