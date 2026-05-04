# Content Pillar Rotation

## Rotation Sequence

```
[personal, technical, lead-magnet, personal, nurture, technical, lead-magnet]
```

Cycle length: 7. Hits ~29% personal, ~29% technical, ~28% lead-magnet, ~14% nurture.

The `current_index` in `autopilot-state.yaml` advances by 1 each run, wrapping to 0 after index 6.

---

## Pillar Definitions

### Personal
**Goal:** Trust, connection, brand building. Show the human behind the work.
**LinkedIn template:** Vulnerability Story OR Contrarian Anti-List
**CTA type:** No CTA — pure resonance. End with a strong closing statement, reframe line, or honest P.S.
**Tone:** Honest, raw, balanced. Vulnerability that teaches, not vulnerability for sympathy.
**Key rules:**
- Never ask open questions ("What do you think?", "Have you experienced this?" = instant AI tell)
- End with a mic-drop line, a P.S. honest caveat, or simply let the post speak for itself
- Shares come from emotional relief — write for that, not for comments
- Contrarian Anti-List: "Here's what I DIDN'T do:" ❌ format with a simple truth underneath

**Matching creator styles:**
- Text format → **S4 Personal Origin Story** (income/journey narratives, "The long way is actually the shortcut" closes)
- Image format → **S5 Personal Event/Authority Signal** (event posts, speaking engagements, in-person moments)
- See `{styleProfiles}` for template skeletons

### Technical
**Goal:** Authority, education, audience nurture. Demonstrate depth.
**LinkedIn template:** Nurture / Educational
**CTA type:** Resource giveaway — put YouTube video link or Skool community link in `firstComment`. Post body: "Full breakdown in the first comment" or "Link below."
**Tone:** Teacher explaining to a capable student. Dense on value, light on fluff.
**Key rules:**
- Named frameworks and analogies drive highest shares (16.5/post avg)
- Soft CTA only — no keyword mechanics for these posts
- References to specific tools/methods with specificity build credibility
- Body links ALWAYS go in firstComment, never in post body

**Matching creator styles:**
- **S3 Authority Contrarian** — use when the topic has a math proof or data-backed argument against conventional wisdom
- **S1 Video Lead Magnet** — use when there's a YouTube video with a demo moment that proves the technical point
- See `{styleProfiles}` for template skeletons

### Lead Magnet
**Goal:** List building, reach explosion. Drive comment keyword engagement.
**LinkedIn template:** Core Template
**CTA type:** Comment keyword — Style B 3-step (like + comment "[KEYWORD]" + connect)
**Tone:** Expert-confident without arrogance. Technical credibility woven in naturally.
**Key rules:**
- Keyword must be ALL-CAPS, selected from `context/lead-magnet-keywords.yaml`
- 2-step CTA mechanic: 1. Like this post 2. Comment "[KEYWORD]" 3. Connect so I can DM
- Post must deliver real value preview (✅ checklist or → arrow list) before the CTA
- P.S. line with honest caveat builds trust and counters the CTA feel
- Image format preferred (7/9 top lead magnet posts use image)

**Matching creator styles:**
- Video format → **S1 Video Lead Magnet** (demo clip + 3-step CTA, avg 432 comments)
- Image/carousel format → **S2 Carousel Lead Magnet** (carousel + result hook + KEYWORD CTA)
- Text format → **S3 Authority Contrarian** (math-backed claim + single-line keyword CTA)
- See `{styleProfiles}` for template skeletons

### Nurture
**Goal:** Relatable value delivery. Strengthen existing audience relationship.
**LinkedIn template:** Nurture/Educational with personality
**CTA type:** Resource giveaway in `firstComment` if content maps to a resource, or no CTA at all
**Tone:** Conversational but substantive. More personality than Technical, more value than Personal.
**Key rules:**
- These posts earn the most shares when they provide emotional relief or perspective shift
- Don't oversell — no urgency framing, no "most people miss this" unless genuinely earned
- Keep the close clean — statement, not a question

**Matching creator styles:**
- **S3 Authority Contrarian** (softer version — same structure but with a resource giveaway instead of keyword CTA)
- **S4 Personal Origin Story** — when the nurture post is a reflective lesson from the creator's journey
- See `{styleProfiles}` for template skeletons
