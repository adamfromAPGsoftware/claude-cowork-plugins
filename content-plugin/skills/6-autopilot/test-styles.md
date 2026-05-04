---
name: test-styles
description: Generate one test LinkedIn post per creator style profile to verify style fidelity and calibrate the workflow
menu-code: TS
---

# [TS] Test Styles

## Goal

Generate one LinkedIn draft per identified creator style profile. Each draft uses a topically relevant but hypothetical topic — these are calibration posts, not real campaign drafts.

This capability does NOT:
- Touch the pillar/format rotation state
- Add to the content calendar
- Send push notifications
- Auto-queue for publishing

Outputs save to `{project-root}/context/draft-queue/test-styles/` for manual review only.

---

## Pre-Load

Load the following before generating any posts:
1. `{styleProfiles}` — all 5 style profiles with template skeletons
2. `{linkedinWritingRules}` — universal LinkedIn rules
3. `{linkedinHookPatterns}` — hook formulas
4. `{linkedinCTAPatterns}` — CTA patterns
5. `{brandVoice}` — anti-AI red flags filter
6. `{contentICP}` — ICP relevance check
7. `{leadMagnetKeywords}` — for keyword selection in lead magnet styles

---

## Generation Sequence

For each of the 5 style profiles, run this mini-pipeline:

### For each style:

**Step A: Topic Selection**

Pick a topic that is:
- Relevant to this niche (AI automation, Claude Code, agency, content creation)
- Has NOT been done in the last run (check `autopilot-state.yaml` history)
- Naturally fits the style's hook type
- Connected to something the creator has demonstrably built or experienced

| Style | Example topic directions |
|-------|------------------------|
| S1 Video Lead Magnet | Claude Code agents, Remotion video pipeline, MCP servers, content automation system |
| S2 Carousel Lead Magnet | skill library, content pipeline stack, agency workflow automation |
| S3 Authority Contrarian | N8N vs agentic systems, SaaS vs custom AI, context engineering |
| S4 Personal Origin Story | Early agency days, first client, first $1K, first 100 subscribers |
| S5 Personal Event/Authority | Speaking at events, client discovery moments, conference observations |

**Step B: Draft LinkedIn Post**

Using the style's template skeleton from `{styleProfiles}`:
1. Write the hook following the style's prescribed hook type
2. Follow the step-by-step skeleton for body structure
3. Apply the style's tone rules
4. Apply the correct CTA type (3-step / single-line / none)
5. Apply universal rules: no hashtags, no em dashes, contractions, → arrows, numerals
6. Apply Anti-AI Red Flags filter

**Step C: Quality Check**

Score against all 6 criteria (including Style Fidelity):
- Voice Authenticity ≥7/10
- Hook Strength ≥7/10
- ICP Fit ≥7/10
- CTA Compliance ≥7/10 (or N/A)
- Platform Compliance: pass
- Style Fidelity ≥7/10

If any criterion fails, revise once and re-score.

**Step D: Save Test Draft**

Save to `{draftQueue}test-styles/test-{style-slug}-{YYYY-MM-DD}.md`:

```yaml
---
style_profile: {style name}
style_code: {S1|S2|S3|S4|S5}
topic: {topic description}
format: {text|image|video-clip}
pillar: {lead-magnet|personal|technical|nurture}
cta_type: {none|keyword|resource-giveaway}
keyword: {KEYWORD or null}
char_count: {N}
quality_scores:
  voice_authenticity: {N}/10
  hook_strength: {N}/10
  icp_fit: {N}/10
  cta_compliance: {N}/10 or N/A
  platform: pass
  style_fidelity: {N}/10
status: test-draft
generated: {YYYY-MM-DD}
---

{full LinkedIn post text}
```

---

## Presentation

After generating all 5 posts, present them side by side with:

```
TEST STYLES — {date}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

[S1] VIDEO LEAD MAGNET
Topic: {topic}
Quality: Voice {N}/10 | Hook {N}/10 | ICP {N}/10 | CTA {N}/10 | Style {N}/10
Reference post: {activity_id}

{full post text}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

[S2] CAROUSEL LEAD MAGNET
... (same format)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

[S3] AUTHORITY CONTRARIAN
...

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

[S4] PERSONAL ORIGIN STORY
...

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

[S5] PERSONAL EVENT / AUTHORITY SIGNAL
...

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

TEST SUMMARY
Styles generated: 5/5
All passing: {yes/no — list any that need review}
Test drafts saved to: context/draft-queue/test-styles/
```

---

## After Review

If any test draft reveals a calibration issue with a style profile:
1. Note the specific structural misalignment
2. Update `{styleProfiles}` to clarify the template skeleton
3. Re-run [TS] for just that style to verify the fix
