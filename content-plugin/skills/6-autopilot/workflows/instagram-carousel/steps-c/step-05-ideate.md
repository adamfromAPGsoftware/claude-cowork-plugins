---
name: step-05-ideate
description: Select topic from trend candidates, map to carousel structure, choose CTA keyword
nextStep: ./step-06-draft.md
---

# Step 5: Ideate

## Goal

Pick the sharpest trending topic and map it to a carousel structure that replicates the psychology of high-performing posts. Decide on the CTA keyword and any YouTube tie-in.

## Sequence

### 1. Select Topic

From the trend_candidates ranked in step-03, select the single best candidate for a carousel based on:
- Carousel fit: can it be broken into discrete, swipe-worthy insights?
- Relevance to today's topic_angle
- ICP resonance (AI builders, agency owners, non-technical professionals learning AI)
- Freshness: most recent first if scores are tied

In automated mode: select candidate #1 unless it has a score below 3/5.
In manual mode: present top 3 and wait for selection.

### 2. Map to Carousel Structure

Using the style_brief from step-04 (slide count target, hook technique, content slide pattern), map the selected topic to a concrete slide plan:

```
Slide 1 — Hook
  Type: {bold claim | shocking stat | visual contrast}
  Core idea: {the single most surprising or counterintuitive thing about this topic}
  Format: Creator photo + short text overlay

Slide 2 — {first sub-point or setup}
  Core idea: {1 key insight, concrete detail, or "why this matters"}

Slide 3 — {second sub-point}
  ...

Slide {N-1} — {final insight or payoff}
  The "aha moment" — the most shareable insight in the carousel

Slide {N} — CTA
  Type: text-only
  CTA: "Comment [KEYWORD] for {specific value}"
  Skool link context: {where this leads — free hub or academy}
```

Target 5-7 content slides based on today's style_brief. Never fewer than 4 content slides (plus hook + CTA).

### 3. Choose CTA Keyword and Offer

Check `{leadMagnetKeywords}` for any existing keywords that match today's topic.

If none match, select from today's topic angle preferred keywords (from `{topicRotation}`).

The keyword must:
- Be 1 word (all caps)
- Directly relate to what the person gets (e.g., CLAUDE → "Comment CLAUDE for the full Claude Code setup guide")
- Sound natural when said aloud ("Comment AGENT for...")

**CTA offer rules:**
- The offer must be **content-specific value** derived from the carousel topic — NOT a generic community pitch
- Good: "Comment AGENT and I'll send you the exact prompt" / "Comment CLAUDE for the full setup guide" / "Comment BUILD and I'll send you all 5 prompts"
- Bad: "Comment AGENT for access to the free {YOUR_FREE_COMMUNITY}" / "Join the community"
- Model the CTA after the top-performing inspiration posts: they offer the specific resource shown in the carousel (prompts, skills, setup guide), not a community or course
- **Never mention** the {YOUR_FREE_COMMUNITY}, {YOUR_PAID_COMMUNITY}, or "free community" on carousel slides or in the CTA slide. These are funnel destinations handled by ManyChat automation — the audience sees only the specific value offer
- The CTA slide sub-text should describe what the person gets in concrete terms, not where they're going

### 4. YouTube Tie-In (Optional)

Check `{project-root}/content-plugin/data/youtube/channel-library.json` for any video that covers the selected topic.

If a relevant video exists:
- Note the video ID for metadata tracking in the draft file
- **Do NOT use firstComment on Instagram** — no first comments on carousel posts

If no relevant video: skip.

### 5. Output Summary

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Carousel Brief
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Topic:        {1-line description}
Angle:        {topic_angle}
Source:       {source URL}
Slide count:  {N} slides
CTA keyword:  {KEYWORD}
CTA offer:    {what they get}
YouTube:      {video title + ID or null}

Slide plan:
  1 [Hook]    {core idea}
  2           {core idea}
  ...
  {N} [CTA]   Comment {KEYWORD} for {offer}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

Then immediately load and execute step-06.
