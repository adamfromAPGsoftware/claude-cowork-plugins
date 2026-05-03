---
name: step-05-draft
description: Generate LinkedIn and X post drafts using today's template, pillar, and topic brief
nextStep: ./step-06-visual.md
---

# Step 5: Draft

## Goal

Write the LinkedIn and X post drafts using the creator's exact voice, today's template, and the topic brief from step-04.

## Mandatory Pre-Load

Before writing anything, load:
1. `{linkedinWritingRules}` — universal rules, format-specific rules, template structures, performance data
2. `{linkedinHookPatterns}` — proven hook formulas ranked by pillar
3. `{linkedinCTAPatterns}` — CTA mechanics for the 3 CTA types
4. `{xWritingRules}` — X-specific voice, format rules, thread mechanics
5. `{nickStyleGuide}` — external style reference calibration (for image post tone and brevity)
6. Brand voice Anti-AI Red Flags filter from `{brandVoice}` (already loaded in step-01)
7. `{styleProfiles}` — creator's proven style profiles with template skeletons (primary structural reference when a style was selected in step-04)

## LinkedIn Draft

### Style Profile Application (primary reference when selected in step-04)

If `style_profile` is set (not `none`), use the selected style's **template skeleton** from `{styleProfiles}` as the primary structural guide:

- **Hook**: use the hook type specified in the style profile (not the generic hook patterns)
- **Body structure**: follow the step-by-step skeleton from the style's "Template Skeleton" section
- **Tone markers**: apply the style's "Tone Rules" — these override generic copywriting advice
- **CTA mechanics**: follow the style's "CTA Mechanics" exactly (3-step vs single-line, etc.)
- **Visual alignment**: confirm the draft references what the visual will show (if format = video or image)
- **Reference post**: if a matching activity ID was noted in step-04, you may read the actual post from `{linkedinPostsReference}{activity_id}/post.md` as a structural model — do NOT copy it, use it to calibrate rhythm and specificity

If `style_profile` is `none`, fall back to the generic template structures below.

### Generic Template Structures (fallback — used when no style profile selected)

**Core Template (lead-magnet pillar):**
```
[Contrarian/alarming hook — 1 line]

[3-way problem framing OR highs vs reality contrast — → arrows]

[Content teaser — "I just finished/recorded/built..."]

[Value list — ✅ or → arrows, 4-6 items, specific]

[Reframe line — what this is really about]

Comment "[KEYWORD]" and I'll send you [specific resource].

Want [resource]?
1. Like this post
2. Comment "[KEYWORD]"
3. Connect so I can DM you

P.S. — [Honest caveat or practical benefit]
```

**Vulnerability Story (personal pillar):**
```
[Statement challenging belonging or identity]

[2-3 paragraphs: honest personal narrative, specific details]

[Turning point — what changed / what I learned]

[Closing statement — strong, definitive, no CTA]
```

**Contrarian Anti-List (personal pillar):**
```
[Bold claim about what I achieved]

Here's what I DIDN'T do:
❌ [Common advice 1]
❌ [Common advice 2]
❌ [Common advice 3]

All I did was [simple truth].

[Reframe — core principle]
```

**Nurture / Educational (technical + nurture pillar):**
```
[Outcome hook — what the result was]

[Context — why this matters / what prompted it]

[Method breakdown — → arrows or numbered steps]

[Key takeaway — single quotable sentence]

[If resource-giveaway: "Full breakdown in the first comment" OR "Link below" — one short line]
```

### Universal LinkedIn Rules (enforce all of these)

- Zero hashtags — anywhere. Ever. Not even in the CTA.
- Short sentences. Each line earns the next. Cut anything that doesn't add value.
- Single-line paragraphs. Line breaks between every paragraph.
- No bold keyword spam — bold/CAPS sparingly (1-2 per post max)
- Contractions mandatory — "I've", "you're", "it's"
- Numbers always as numerals — "60" not "sixty"
- No em dashes — use a full stop or line break instead
- 800-1300 characters for text posts; 600-1000 for carousel companion posts
- Links NEVER in the body — always in `firstComment` if resource-giveaway CTA

**Anti-AI Red Flags — check every draft for these:**
- "Leverage" → cut
- "Game-changing" → cut
- "Seamless" → cut
- "Delve into" → cut
- "It's worth noting" → cut
- "In today's fast-paced world" → cut
- "Thought leader" → cut
- Perfectly parallel bullet lists (every item exactly same length) → break the pattern
- Title Case headings → sentence case only
- Opening with "I" on the very first word → restructure

### X Draft

Read `{xWritingRules}` for full X-specific guidance. Key rules:
- LinkedIn draft is always primary; X is an adapted version — same topic, different format and tone
- X tone: more direct, punchier, slightly more opinionated than LinkedIn. Less structured, more raw.
- **X Premium is active (25,000 char limit).** Default to a single long-form post, NOT a thread.
- **Format decision:**
  - Quick contrarian take or punchy observation → short post (71–140 chars)
  - YouTube repurpose, tutorial, or substantial insight → long-form single post (500–2,500 chars)
  - Only use a thread if the content is a genuine numbered list where each item needs its own space
- **First 140 chars must work as a standalone hook** — this is what appears before "Show more"
- No hashtags — ever
- No links in body — X suppresses them algorithmically. State "link in reply" if needed, or omit.
- If `cta_type = resource-giveaway`: do NOT put the URL in the post body. Write "Full walkthrough in the first reply." — the URL goes in a reply after posting (handled at publish time via Buffer first comment option).

### Draft Output Format

Present both drafts clearly:

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
LINKEDIN DRAFT
Pillar: {pillar} | Template: {template} | Format: {format} | {char count} chars
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

{full LinkedIn post copy}

{If resource-giveaway — firstComment preview:}
── First comment ──
{firstComment content}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
X DRAFT
Format: {short-post | long-form | thread} | {char count}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

{full X post copy}

{If resource-giveaway — first reply preview:}
── First reply ──
{URL}

```

Then immediately load and execute step-06.
