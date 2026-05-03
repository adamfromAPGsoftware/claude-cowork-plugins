# CTA Patterns

## The 3 Content Categories

Every post serves one of three purposes. Match CTA style to category:

### 1. Lead Magnet Posts
- **Goal:** List building + reach explosion
- **CTA:** Comment keyword → DM funnel
- **Pattern:** "Comment X and I'll DM you"
- **Recommended CTA:** Style B (highest performing)

### 2. Personal / Authentic Posts
- **Goal:** Trust + connection + brand building
- **CTA:** Conversation starters, no hard CTA
- **Pattern:** Open-ended question, invite discussion

### 3. Value / Educational Nurture Posts
- **Goal:** Authority + audience nurture
- **CTA:** Soft CTAs (link in comments, resource attached)
- **Pattern:** "Full breakdown in comments" or "Link to resource in first comment"

---

## CTA Style A — Single-Line Keyword

```
Comment '[KEYWORD]' and I'll send you [specific resource description]
```

**Rules:**
- Keyword must be specific and memorable (e.g., "AGENT", "CLAUDE", "STACK")
- Resource description must be concrete — not "a resource" but "the complete 47-page playbook"
- One line, direct, no fluff

**Best for:** Quick posts, nurture category, when brevity matters

---

## CTA Style B — Numbered Steps + Connect (RECOMMENDED for Lead Magnet)

```
Want [specific resource]?

1. Like this post
2. Comment "[KEYWORD]"
3. Connect with me so I can DM you
```

**Rules:**
- Must preserve the 3-action structure: engagement signal → keyword trigger → connect for delivery
- Agent has flexibility to rephrase wording but structure is fixed
- The keyword must match the carousel CTA slide's button text (for carousel format)
- Drives engagement, keyword comment, AND connection request simultaneously

**Best for:** Lead magnet posts — proven highest-performing pattern

---

## CTA-to-Format Mapping

| Format | Recommended CTA | Notes |
|--------|----------------|-------|
| Text | Style B for lead magnet, conversation for personal | Text CTAs drive highest comment:like ratio |
| Image | Style B for lead magnet | Image + keyword CTA = high engagement |
| Carousel | Style B (match CTA slide keyword) | CTA slide keyword MUST match post text keyword |
| Video | Style B for lead magnet | Video + CTA = strong combo |

## CTA Performance Data

> Engagement metrics per CTA type from 48-post analysed dataset. Use to select the right CTA approach for the content category.

| CTA Type | Comment Volume | Engagement Pattern | Best Category |
|----------|-----------------|-------------------|---------------|
| Comment keyword (ALL CAPS) | Up to 1,072 comments | 2.1:1 comment:like ratio | Lead Magnet |
| 2-step (Like + Comment keyword) | Up to 782 comments | 4.9:1 ratio (highest) | Lead Magnet |
| Soft CTA (link in comments) | ~88 comments avg | 8.5:1 like:comment (organic) | Nurture |
| Open question | ~113 comments avg | Quality discussion, balanced ratio | Personal |
| No CTA (pure resonance) | Variable | Highest shares (avg 16.5/post) | Personal / Nurture |

**Key takeaways:**
- 2-step CTA (like + comment + connect) is the highest-performing mechanic for list building — reserve for lead magnet only
- ALL-CAPS keywords ("ROADMAP", "PRICING") outperform lowercase ("framework", "apply") in raw comment volume
- Soft CTAs preserve authenticity in nurture/educational posts — keyword gating breaks the format
- No-CTA posts earn the most shares because people redistribute value, not transactions
- PS connection request ("Connect with me so I can DM you") solves LinkedIn's DM limitation and builds the connection graph

## Keyword Source

Keywords MUST be selected from the centralised library at `{project-root}/content-plugin/data/lead-magnet-keywords.yaml`. Do not invent new keywords. Pick the keyword that best matches the post's topic from the 50 pre-registered options.

## Keyword Rules

- ALWAYS uppercase the keyword in the CTA
- Keyword should be 1 word, relevant to the content topic
- Check derivative tracking — don't reuse keywords across posts in same project
- Carousel: post text keyword must exactly match CTA slide button text
