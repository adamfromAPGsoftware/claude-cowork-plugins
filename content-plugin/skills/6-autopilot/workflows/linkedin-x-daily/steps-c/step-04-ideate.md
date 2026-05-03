---
name: step-04-ideate
description: Select the best topic and produce a topic brief for the drafting step
nextStep: ./step-05-draft.md
---

# Step 4: Ideate

## Goal

Combine pillar + template + research + analytics to select the single best topic for today's post and produce a complete topic brief.

## Sequence

### 1. Select Topic

If `topic_source = youtube-repurpose`:
- Topic is already determined from step-02. The video is the source.
- Confirm the pillar still maps well to this video's content. If not (e.g., a "personal" pillar day but the unpromoted video is purely technical), override pillar to "technical" for this run — video-repurpose always takes priority.
- Extract the 3-5 most quotable or surprising moments from the transcript for use as raw material in the draft.

If `topic_source = exa-trending`:
- Evaluate the 3-5 candidate topics from step-02 against today's pillar, analytics insights, and ICP relevance
- Select the topic with the strongest hook potential AND clearest connection to the creator's experience/authority
- Must connect to something the creator has actually built, done, or witnessed — no generic takes

### 2. Define the Angle

The same topic can be framed many ways. Choose the angle that:
- Creates the most friction or surprise in line 1 (the hook)
- Matches today's template structure
- Will resonate with both ICPs (AI agency builders AND SME decision makers)

Examples of angle types:
- **Contrarian angle** — "Everyone's saying X, but I've seen the opposite"
- **Number/stat anchor** — "After 60+ projects, the pattern is always the same"
- **Tool-specific** — "This is what Claude Code actually does differently"
- **Personal story** — "I made this mistake early on and it cost me 6 months"
- **Industry call-out** — "Most [role]s are ignoring this"

### 3. Select CTA + Resource (if applicable)

If `cta_type = keyword`:
- Load `{leadMagnetKeywords}` — pick the keyword that best matches today's topic
- Define what resource will be DM'd (free YouTube video, lead magnet doc, community access, etc.)

If `cta_type = resource-giveaway`:
- Identify the best resource: most relevant YouTube video URL or Skool community link (`https://{YOUR_COMMUNITY_URL}`)
- Prepare the `firstComment` content: "Full breakdown here → {URL}" or similar — short, direct, no hype

If `cta_type = none`:
- Plan the closing statement or P.S. line — it should land as a mic-drop or honest admission, not trail off

### 4. Select Style Profile

Load `{styleProfiles}`. Based on today's pillar, format, and topic, select the best-fit style profile:

| Pillar | Primary style | Secondary style |
|--------|--------------|-----------------|
| lead-magnet | S1 Video Lead Magnet (if format=video) / S2 Carousel (if format=image+carousel) / S3 Authority Contrarian (if format=text) | — |
| personal | S4 Personal Origin Story (if text) / S5 Personal Event/Authority (if image) | — |
| technical | S3 Authority Contrarian | S1 Video Lead Magnet |
| nurture | S3 Authority Contrarian (softer) | S4 Personal Origin Story |

If none of the 5 styles fit the topic naturally, set `style_profile: none` and use the generic templates in step-05.

Also check whether the chosen style has a matching example post in `{linkedinPostsReference}` — if so, note the activity ID so step-05 can reference it directly.


### 5. Output Topic Brief

```
Topic brief
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Topic: {1-line description}
Source: {youtube-repurpose | exa-trending}
Angle: {angle type + 1-sentence description}
Hook direction: {the opening line concept}
Key points (3-5):
  - {point}
  - {point}
  - {point}
CTA type: {none | resource-giveaway | keyword}
{CTA details: keyword / resource URL / closing line direction}
Style profile: {S1 Video Lead Magnet | S2 Carousel Lead Magnet | S3 Authority Contrarian | S4 Personal Origin Story | S5 Personal Event/Authority | none}
{If style matched: "Reference post: {activity_id} — {post title/hook}"}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

Then immediately load and execute step-05.
