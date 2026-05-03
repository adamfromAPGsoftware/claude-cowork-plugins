---
name: step-06-draft
description: Write per-slide copy, Instagram caption, and TikTok caption
nextStep: ./step-07-generate.md
---

# Step 6: Draft

## Goal

Write all copy: per-slide text, Instagram caption, and TikTok caption. Apply brand voice rules. No AI-sounding language.

## Sequence

### 1. Write Per-Slide Copy

For each slide in the carousel_brief from step-05:

**Slide 1 — Hook slide:**
- Headline: max 8 words. Bold, specific, scroll-stopping.
- No question marks. A claim or stat, not a question.
- This is placed over the creator's photo — keep it tight and punchy.
- Examples: "Claude can now do this in 3 clicks" / "This AI mistake costs businesses $12K/year"

**Content slides (2 through N-1):**
- Headline: max 8 words
- Supporting text: max 25 words (optional — some slides are headline-only if the style brief calls for minimal text)
- Each slide must be a self-contained insight — make sense even if someone screenshots just that slide
- Progressive reveal: each slide should make the reader want the next one
- Use numbers, percentages, and specifics wherever possible ("saves 6 hours" not "saves time")

**CTA slide:**
- Large text: "Comment [KEYWORD]"
- Subtext: "and I'll send you {content-specific value}" or "for {specific resource}"
- The offer must be derived from the carousel content — e.g., "the exact prompt", "the full setup guide", "all 5 skills"
- **Never mention** the {YOUR_FREE_COMMUNITY}, {YOUR_PAID_COMMUNITY}, "free community", or "AI-first agency" on carousel slides or the CTA
- Optional: "Follow for more [topic-relevant phrase]"
- No photo background — text-only in brand style

### 2. Write Instagram Caption

Structure:
1. **Hook line** (line 1, no more than 10 words) — mirrors the hook slide concept. This is what shows before "more"
2. Line break
3. **Context** (2-3 sentences) — why this matters, what they'll learn from the carousel
4. Line break
5. **CTA** — "Comment [KEYWORD] and I'll send you {offer}"
6. Line break
7. **Hashtags** (3-5) — mix of niche and broad. Never generic (#AI alone is too broad). Examples: #claudeai #aitools #aiagency #artificialintelligence #claudecode

Rules:
- Never put links in the caption body (no firstComment on carousels either)
- No open questions as CTAs ("What do you think?" is banned)
- Contractions required — sounds like the creator, not a press release
- No em-dashes at the start of lines (LinkedIn rule applies here too)
- Max 2,200 characters but aim for 150-300 words (Instagram is not LinkedIn)
- **Never mention** the {YOUR_FREE_COMMUNITY}, {YOUR_PAID_COMMUNITY}, "free community", or "AI-first agency" in the caption. The CTA line should offer content-specific value only ("Comment X and I'll send you the prompt / guide / setup"). ManyChat handles the funnel destination.

### 3. Write TikTok Caption

Same topic, different voice — shorter, more casual, TikTok-native:
- Max 150 words
- Hook line even more punchy — TikTok auto-plays, hook = first 3 words
- "Link in bio" instead of comment keyword (TikTok doesn't support comment DMs the same way)
- TikTok hashtags: 3-5, more trend-based than niche (#viral #learnontiktok #aitools #claudeai)
- End with a simple follow CTA: "Follow for more AI tools that actually work"

### 4. Apply Anti-AI Filter

Before finalizing any copy, scan against brand-voice.md Anti-AI Red Flags:

**Banned phrases:** leverage, seamless, game-changing, elevate, unlock the power, dive in, delve into, cutting-edge, innovative solution, revolutionize, transform your, in today's fast-paced world, needless to say, at the end of the day, as an AI language model

**Banned patterns:**
- Three-word openers that start with "In the world of..."
- Lists of adjectives before a noun ("innovative, powerful, game-changing tool")
- Passive voice overuse ("it can be seen that...")
- Hedging language ("might potentially help you")

Replace any flagged phrases with direct, specific language.

### 5. Output

Present all copy for review in manual mode:

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Carousel Copy
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

SLIDES:
[1 - Hook]  {headline}
[2]         {headline} / {supporting text}
...
[{N} - CTA] Comment {KEYWORD} / {subtext}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
INSTAGRAM CAPTION:
{caption}

Hashtags: {#tag1 #tag2 ...}
{if youtube_tie_in: "First comment: {YouTube URL}"}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
TIKTOK CAPTION:
{caption}

Hashtags: {#tag1 #tag2 ...}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

Then immediately load and execute step-07.
