# Short-Form Script Rules

## Speaking Rate Guidelines

**The single most important constraint for script accuracy.** Every word count and timing calculation must use these rates.

| Pace | Words per Second | Words per Minute | When to Use |
|------|-----------------|-----------------|-------------|
| Normal | 3.5 wps | 210 wpm | Body sections — energetic, confident delivery |
| Fast | 4.0 wps | 240 wpm | Hook — high-energy, urgent |
| Slow | 3.0 wps | 180 wpm | CTA — brisk but clear |

### Duration Calculation Formula

```
section_duration_seconds = word_count / words_per_second
```

**Examples:**
- Hook (fast pace): 12 words ÷ 4.0 wps = **3.0 seconds**
- Body beat (normal pace): 25 words ÷ 3.5 wps = **7.1 seconds**
- CTA (slow pace): 9 words ÷ 3.0 wps = **3.0 seconds**

### Validation Rule

After writing each script section, count the words and calculate the speaking duration. The calculated duration MUST match the time allocated in the storyboard within ±1 second. If it doesn't, rewrite the section to fit.

**B-roll/MG segments do NOT consume speaking time** — the speaker continues talking while visuals change. Only count words that the speaker actually says in the time window.

---

## Duration Variations

Generate scripts across a mix of optimal short-form lengths to maximise platform performance:

| Category | Duration | Word Count (approx) | Best For | Platform Sweet Spot |
|----------|----------|---------------------|----------|-------------------|
| Punchy | 15–20s | 50–70 words | Single insight, hot take, one-liner + proof | TikTok, Reels (algorithm favours high completion rate) |
| Standard | 22–30s | 75–105 words | Tool demo, pain point + solution, mini-story | All platforms (22–30s = highest completion rates) |
| Deep | 35–45s | 120–155 words | Step-by-step, framework, detailed case study | YouTube Shorts (longer watch time rewarded) |

### Mix Rule

When generating 5 scripts, use this distribution:
- **1× Punchy** (15–20s) — highest completion rate, algorithm boost
- **3× Standard** (22–30s) — sweet spot for engagement + depth (data shows 22–30s dominates top performers)
- **1× Deep** (35–45s) — highest value, builds authority

Each concept from step 02 should be assigned to the duration category that best fits its complexity. Simple insights → Punchy. Multi-step concepts → Deep.

---

## Angle Diversity

Every batch of 5 scripts must include a mix of **angle types** — not just different topics, but different storytelling approaches.

### Angle Types

| Angle Type | Description | What It Feels Like |
|-----------|-------------|-------------------|
| **Story** | Mini-journey extracted from the body video — walks through what actually happened on screen | "Watch me build this..." / "Here's what happened when I..." |
| **Tool-Focus** | Spotlights one specific tool or skill demonstrated in the video | "This one feature changed everything..." |
| **Concept** | Framework, insight, data point, or mental model from the video | "Most people get this wrong..." |
| **Value-Drop** | Free resource, accessibility angle, or immediate takeaway | "You don't need to pay for this anymore..." |

### Distribution Rule

- **Minimum 1 Story** + **Minimum 1 Tool-Focus** — these are mandatory in every batch
- Remaining 3 scripts: any mix of Concept / Value-Drop
- **If the body video has 3+ tool interaction segments** (check `visual-analysis.json` for segments classified as `screen-share` or `mixed-pip`): target **2 Story** scripts instead of 1

### Story Script Writing Rules

Story scripts are built from real body video moments — they are NOT conceptual reimaginings:

1. Each beat maps to a **real body video moment** with a specific timestamp range
2. MGs should show what was actually on screen — predominantly **Tier B/C with reference frames** extracted from those moments
3. Narrator tells the journey in first person: "I opened...", "The agents started...", "Here's what came back..."
4. The hook teases the outcome or the problem that triggered the journey
5. Body walks through 2–4 stages from the body video in chronological order

---

## Script Structure

Every short-form video follows a strict 3-part structure. Timing varies by duration category.

### Hook (2–5 seconds)
- **Purpose:** Stop the scroll. Pattern interrupt.
- The first 2 seconds determine if the viewer stays or scrolls.
- Must contain either a bold claim, surprising question, or result tease.
- Voice should be confident, slightly faster than normal pace (4.0 wps).
- **Hook MUST open with V5 split-screen (50/50)** — recognizable visual (brand logo, tool UI, authority figure) in top half + speaker face in bottom half. V6 (hook text) as the opening segment is FORBIDDEN (P4 rule). 4/5 top performers open with split-screen, not text cards.
- **Punchy videos:** Hook is 2–3 seconds (6–9 words)
- **Standard videos:** Hook is 3–5 seconds (9–15 words)
- **Deep videos:** Hook is 3–5 seconds (9–15 words)

### Body (varies by duration category)
- **Purpose:** Deliver the insight, tool demo, or story.
- Break into distinct beats — each beat is one visual segment (2–3 seconds).
- **Punchy:** 1–2 beats (10–15s body). At least 3 B-roll/MG markers.
- **Standard:** 2–4 beats (15–23s body). At least 6 B-roll/MG markers.
- **Deep:** 3–5 beats (28–38s body). At least 10 B-roll/MG markers.
- Use conversational language — write for speaking, not reading.
- Include one "re-hook" moment around the 50% mark (except Punchy — too short).
- **Err on the side of MORE B-roll/MG markers, not fewer.** Every beat transition is a visual change opportunity. B-roll keeps viewers engaged.

### CTA (2–5 seconds)
- **Purpose:** Tell the viewer what to do next.
- Keep it to ONE action (follow, comment, save, or visit link).
- Don't stack CTAs ("follow AND like AND share" = no action).
- **Default CTA pattern: comment-gated** — "Comment [keyword] and I'll send you [resource]." (appears in all top 5 performers). Use follow/save CTAs only as variation.
- **NEVER mention "community" in the CTA** — do not say "the free community link" or "the community". Tell them specifically what they're getting: "the free Claude skill", "the free AI workflow", "the free pipeline walkthrough", etc. Match the descriptor to what the video is actually about. "The free resource" is a fallback, not the default.
- **Punchy videos:** CTA is 2–3 seconds (4–6 words) — fast, decisive
- **Standard/Deep videos:** CTA is 3–5 seconds (6–10 words)

---

## Hook Patterns

| Pattern | Template | Frequency in Top 15 | Best For |
|---------|----------|---------------------|----------|
| Product Drop | "[Company] just [dropped/launched] [Product]" | 7/15 (dominant) | New tool launches, feature reveals |
| Elimination | "You don't need to [pay for X] anymore" | 3/15 | Free alternatives, cost-saving tools |
| Pain Interrupt | "Stop [doing wrong thing]" | 2/15 | Bad habit correction, better workflows |
| Step-by-Step Tease | "Here's how to [outcome], step by step" | 1/15 (highest single engagement) | Tutorials, frameworks, how-tos |
| Result Reveal | "This [tool] saved me [metric]" | retained | Tool demos, case studies |
| Journey Tease | "Watch what happens when I [action]..." | — | Story-driven scripts |
| Before/After | "I used to [old way]. Now [new way]." | — | Story + tool scripts |
| Direct Address | "If you're a [role] who [struggles with X]..." | use sparingly | Pain point content (lowest performer) |

---

## Writing Rules

1. **Write for speaking** — Read every line aloud. If it doesn't sound natural, rewrite it.
2. **One idea per video** — Short-form is not a summary. Pick one angle and go deep.
3. **No throat-clearing** — Don't start with "So," "Hey guys," or "Today I want to talk about." Start with the hook.
4. **Specificity beats generality** — "This saved me 4 hours per week" > "This saves time."
5. **Active voice only** — "I built this in 2 hours" not "This was built in 2 hours."
6. **Contrast creates interest** — Set up the wrong way, then reveal the right way.
7. **End before you're done** — Leave them wanting more. Don't wrap up neatly.
8. **Count your words** — After writing each section, count the words and verify against speaking rate. A 7-second body beat at 3.5 wps = exactly 24–25 words. If you wrote 35, you wrote too many.
9. **No headline-style colons as sentence openers** — "Before this:" and "Now:" are ad copy, not speech. Write as you'd say it out loud: "Before this, it was..." / "Now one AI pipeline..." / "The only difference is...". If reading it aloud feels like announcing a slide title, rewrite it.
10. **Complete connective sentences** — Avoid back-to-back fragment pairs as mid-beat connectors. Use "and", "but", "so", "because", "with" to link ideas into sentences a real person would say. Short punchy fragments are only allowed as deliberate beat-closers for emphasis (e.g. "Every week." "Your skills transfer.").
11. **Use first person to anchor experience** — "I used to...", "I spent...", "I built...", "I noticed..." grounds the script in lived experience and sounds credible. Avoid third-person narration about yourself ("one AI pipeline loads...") in the hook — first person is stronger.

---

## Proven Engagement Signals

Data from 15 top-performing short-form videos and 36 high-engagement reels reveals these patterns:

1. **"Free" keyword** — Appears in 13/15 top performers. Mention "free" when describing tools, templates, or resources.
2. **Immediate text overlay** — Text on screen within the first SECOND (14/15 top performers). Not the second or third second — the first.
3. **Comment-gated CTA** — "Comment [keyword] and I'll send you [resource]" appears in all top 5 performers. Default to this CTA pattern.
4. **MG coverage** — 65–84% of total video duration should be non-speaker MG visuals. Raw B-roll is NEVER used directly — only as reference frames for Hera MG prompts. 65% is the FLOOR; top performers hit 80–84%.
5. **No hashtags** — Top performers use zero hashtags. Platforms now auto-classify content.
6. **Split-screen layout** — 50/50 content-to-speaker ratio (content/MG TOP, speaker BOTTOM). Transparent divider. 4/5 top performers use 50/50 (NOT 65/35).

---

## B-Roll and MG Markers

Use inline markers in the script to indicate where visual changes occur. **Be generous with markers — more is better.** Every 2–3 seconds of speaker footage should be broken up with a visual change.

### Reference Frame Markers (for Hera MG Generation)

Reference frames are single keyframe extracts from long-form B-roll — they are NOT used directly in the final video. Each reference frame feeds a Hera MG prompt that generates the animated visual.

```
[REF-FRAME: source="intro" timestamp="2:15" description="VS Code showing the API integration configured" mg_prompt_ref="MG-01"]
```

Include:
- `source` — which long-form segment (intro, body, etc.)
- `timestamp` — single keyframe timestamp from long-form video (not a range)
- `description` — what's visible on screen (specific enough to extract the right frame)
- `mg_prompt_ref` — which MG prompt number this frame feeds (e.g., MG-01)

### Body Video Moment Markers (Story Scripts Only)

For Story-type scripts, use inline markers to link each beat to a specific body video moment. These markers feed downstream storyboard and asset generation with pre-curated timestamps:

```
[BODY-MOMENT: timestamp="3:45-4:12" description="Claude Desktop with research prompt" feeds_mg="MG-01" tier_intent="B"]
```

Include:
- `timestamp` — range from the body video (not the short-form timeline)
- `description` — what's visible on screen at that moment
- `feeds_mg` — which MG prompt number this moment feeds
- `tier_intent` — expected MG tier: `B` (frame-extract + Hera enhancement) or `C` (frame-extract as Hera reference)

### MG Markers (Hera Motion Graphic Prompts)

MG prompts must be **detailed and production-ready** — they are passed directly to the Hera Video API. Vague prompts produce unusable results.

```
[MG: prompt="A sleek 9:16 vertical motion graphic showing a WhatsApp chat interface (green #25D366 header) with automated reply messages appearing one by one in speech bubbles, each with a subtle slide-in animation from the right. Dark background (#0a0a0a). Modern, clean UI aesthetic. Messages appear at 0.5-second intervals." reference="branded-assets/whatsapp-screenshot.png" duration="4s"]
```

#### MG Prompt Structure (MANDATORY — follow this order):

1. **Format + orientation** — "A sleek 9:16 vertical motion graphic showing..."
2. **Subject** — What is being shown (specific tool/concept with brand colors)
3. **Motion** — How it moves (slides in, fades up, counts up, particles flow)
4. **Visual style** — Treatment (clean, minimal, corporate, energetic, dark theme)
5. **Color palette** — Specific hex codes for brand colors, background color
6. **Timing** — Pacing guidance (elements appear at X-second intervals, quick reveal, slow build)

#### MG Prompt Quality Rules:

- **Name specific tools/platforms with brand colors** — "Slack purple #4A154B workspace" not "messaging app"
- **Describe the motion, not just the end state** — "counter rapidly counts from 0 to 500, then bounces to rest" not "shows 500"
- **Include background color** — Always specify background (default: `#0a0a0a` dark)
- **Include aspect ratio** — Always mention "9:16 vertical" in the prompt
- **Reference images dramatically improve output** — Always include a `reference` field pointing to a branded asset, frame extract, or canvas build when the MG features recognisable tools/brands
- **Duration affects motion pacing** — A 2s MG needs fast reveals; a 4s MG can build up. State the duration in the prompt context.

#### Bad MG Prompts (NEVER write these):

- "Show some AI stuff" — no subject, no motion, no style
- "Animate the workflow" — what workflow? What motion?
- "Cool transition" — not actionable
- "Data visualization" — of what data? What format? What colors?

### V4b MG Cutaway Markers

V4b cutaways are brief 1–2 second (30–60 frame) motion graphic interstitials with NO caption overlay. The speaker's voiceover continues from the adjacent segment. Plan at least 1 V4b per 10–12 seconds.

```
[V4b: content_rule="{tool|build|stat|default}" mg_prompt_ref="MG-{NN}" duration="1-2s"]
```

**Content selection rules:**
- Tool/platform mentioned → tool logo MG (e.g., Claude logo, VS Code icon)
- Build/creation action described → typing/coding animation
- Statistic or number cited → animated counter or data visualisation
- Default (no specific context) → abstract tech/data flow

**Frequency:** At least 1 per 10–12 seconds. For a 30s video, minimum 2–3 V4b cutaways.
**Duration:** 30–60 frames (1–2s at 30fps). Never longer than 60 frames.
**Caption:** NONE — voiceover plays through from adjacent speaker segment.

---

## Pacing Guidelines

- **Hook:** V5 split-screen (50/50) as the opening segment (P4 rule). V6 hook text as opener is FORBIDDEN.
- **Punchy (15–20s):** 5–7 visual changes minimum. Fast cuts. Every moment earned. 65%+ non-speaker.
- **Standard (22–30s):** 8–12 visual changes. Rapid rhythm. 65%+ non-speaker.
- **Deep (35–45s):** 12–18 visual changes. Sustained engagement through near-constant variety. 70%+ non-speaker.
- **V4b cutaway frequency:** At least 1 V4b MG cutaway per 10–12 seconds (P3 sub-rule).
- **Min cut density:** At least 6 visual changes per 15 seconds (P10 rule).
- **Max same-shot:** 4 seconds (120 frames) absolute max. Typical: 2 seconds (60 frames).
- **Visual changes:** Minimum every 2–3 seconds
- **MG coverage:** 65% is the FLOOR, not the goal. Top performers hit 80–84%. Target 80%+.
- **Design principle:** "MG with occasional speaker moments" — the speaker's voice plays continuously under all visual types.
- **Re-hook moment:** Around the 50% mark of the body (Standard/Deep only)

---

## MG Density Guidelines

**Near-constant MG is the standard for high-performing short-form.** Research shows viewers scroll within 3 seconds if the visual doesn't change. Speaker-only footage should be the exception, not the rule — think of it as "MG with occasional speaker moments."

| Duration Category | Min MG/Visual Clips | Min MG Coverage (FLOOR) | Target Coverage |
|-------------------|---------------------|------------------------|-----------------|
| Punchy (15–20s) | 4 | 65% | 80%+ |
| Standard (22–30s) | 7 | 65% | 80%+ |
| Deep (35–45s) | 10 | 70% | 80–84% |

**The speaker's voice continues under ALL MG clips** — visual changes don't interrupt the script. This means you can (and should) layer MG over most of the body section while the speaker keeps talking.

When in doubt, add another MG clip. The Video Editor SF pipeline can always remove extras during storyboard refinement, but it can't add clips that weren't planned. Plan for 80%+ coverage and let the pipeline trim if needed.

### MG Selection Priority

1. **Hera MG from reference frame** — Extract keyframe from long-form B-roll, feed to Hera with reference image for animated version
2. **Hera MG from prompt only** — When no suitable B-roll reference exists, generate MG from detailed prompt alone
3. **V4b MG cutaway** — Brief 1–2s interstitial MG (tool logo, typing animation, counter, abstract tech) between speaker segments

**Raw B-roll is NEVER used directly in the final video.** All non-speaker visuals are Hera AI-generated motion graphics. B-roll extracts serve only as reference frames for Hera prompts.

---

## Caption Rules

- **Sentence case** (default) — ALL CAPS only for emphasis words (P8 rule)
- 1 highlight word per caption burst (rendered in teal `#4ADE80` — NOT orange)
- Max 3–4 words per burst
- Word-by-word reveal animation (5 frames/word, scale pop-in 0.8→1.0)
- Layout-dependent positioning: full-speaker 60%, split-screen 75%, full-screen 78%, fallback 70%
- Safe zone: 10% margin top/bottom

---

## Speaker Zoom Values

| Segment Type | Zoom Factor | Notes |
|-------------|-------------|-------|
| V1 (speaker) | 1.03 | Barely perceptible — default for speaker returns |
| V2 (speaker-zoom/emphasis) | 1.08 | Moderate emphasis — hook moments, emotional peaks |
| V7 (CTA) | 1.05 | Distinct from V2, subtle closing emphasis |

**1.25 zoom is FORBIDDEN** — old value that looked amateur. Real top creators use subtle zoom only (max 1.08).

### Ken Burns MG Zoom (MANDATORY)

All non-speaker visuals (V4, V4b, V5 overlay zone) MUST have Ken Burns zoom. Static MG display is FORBIDDEN.

| Motion Type | Zoom Range | When |
|------------|-----------|------|
| Default zoom | 1.0 → 1.15 | All MG/screen content |
| Aggressive zoom (UI highlight) | 1.0 → 1.3 | Close-up on specific UI element |

---

## Teleprompter Section

Every script output file MUST include a `## Teleprompter` section at the bottom. This section contains ONLY the speaker's words — no markers, no stage directions, no section labels — formatted for easy copy-paste into a teleprompter app.

### Teleprompter Formatting Rules:

- **Plain text only** — no markdown formatting, no bold, no headers
- **One sentence per line** — each line is a natural breath point
- **Short lines** — max 8–10 words per line for easy reading while filming
- **ALL CAPS for emphasis words** — matches the caption highlight words
- **Double line break between sections** — Hook / Body / CTA separated by blank lines
- **No [B-ROLL] or [MG] markers** — those are visual cues, not spoken words
- **Include pause indicators** — use `...` for natural pauses (e.g., between hook and body)

### Example:

```
Most people get CLIENT COMMUNICATION
completely wrong.

...

They send long emails that
nobody reads.
They schedule MEETINGS that could
have been a message.

Here's what I do instead.
I set up an AI that handles
the FIRST RESPONSE automatically.

...

Follow for part two where I
show you the exact SETUP.
```

---

## Platform Copy Rules

Every script output file MUST include a `## Platform Copy` section after the Teleprompter section. Each platform copy adapts the video's hook angle to that platform's native style — never copy-paste the same text across platforms.

### Instagram Reel Copy

Two-part format:

1. **Hook line** — Under 125 chars (visible before "more" truncation). Keyword-rich. Must match the video's hook angle but written for reading, not speaking.
2. **Body + CTA** — 1-2 sentence value line + comment-gated CTA matching the video's CTA keyword.
3. **Hashtags** — 4–5 niche hashtags at the end of the caption (after the body, on a new line). Choose topic-specific tags that match the video's angle and ICP (e.g. `#aiagent #claudeai #contentautomation`). No generic mega-tags (#viral, #fyp).

**Tone:** Confident, direct, slightly polished. Instagram rewards keyword-rich captions over hashtags (Meta reduced hashtag impact). For lead generation, target 300-900 chars total.

### TikTok Copy

Single caption field, more casual/raw tone than Instagram.

- **Hook** — Self-diagnosis ("If you're someone who...") or chaotic/personal style preferred. Can be longer than Instagram (up to 300 chars).
- **CTA** — Comment-first with DM delivery: "Comment '{KEYWORD}' below and then DM me '{KEYWORD}' — I'll send you [resource]!" The comment is the PRIMARY ask because TikTok's algorithm heavily rewards comment engagement. The DM is the delivery mechanism (ManyChat triggers on DMs). Always make the comment action crystal clear — tell them exactly what word to comment and that they need to DM the same word to receive the resource.
- **Hashtags** — 3-5 topic hashtags for categorization (TikTok algorithm reads caption text for SEO).
- **Voice** — Personal ("I", "my"), raw/unfiltered beats polished.

### YouTube Shorts Copy

Two separate fields:

1. **Title** — Under 40 chars. Front-load the primary keyword. Create curiosity gap. This appears in YouTube AND Google search results.
2. **Description** — Front-load with lead magnet CTA on the first line (e.g. "🎁 Grab this free resource in my free community → {YOUR_COMMUNITY_URL}"), then 2-3 keyword-rich sentences summarizing the value, then subscribe CTA, then 3-5 hashtags including #Shorts.

**Tone:** More professional/SEO-focused than TikTok. Descriptions can be detailed since longer watch time is rewarded.

### Platform Copy Quality Rules

- Each platform's copy MUST adapt the video's hook angle to that platform's native style
- Never copy-paste identical text across platforms — each has different algorithm priorities
- Instagram: keyword-dense, no/minimal hashtags, polished
- TikTok: casual, personal voice, self-diagnosis hooks, 3-5 hashtags
- YouTube: SEO-first, front-loaded keywords, #Shorts hashtag required
- **CTA language:** Tell the viewer specifically what they're getting — "the free Claude skill", "the free AI workflow", "the free pipeline walkthrough", etc. Match the descriptor to the video's content. NEVER say "the free community link" or "the community". "The free resource" is a generic fallback — always try to be more specific.

### Lead Magnet Keyword Integration

Every script's Platform Copy section MUST include a lead magnet CTA using a keyword from the centralised library.

1. Load `{project-root}/_bmad/ccs/data/lead-magnet-keywords.yaml`
2. Select ONE keyword from the `keywords` list that best matches the video's topic
3. Use the platform-appropriate CTA template:
   - **Instagram:** "Comment '{KEYWORD}'" pattern (comment-gated)
   - **TikTok:** Comment-first pattern — "Comment '{KEYWORD}' below and then DM me '{KEYWORD}' — I'll send you [resource]!" (Comment is primary for algorithmic engagement boost; DM is the ManyChat delivery trigger)
   - **YouTube Shorts:** No keyword CTA. Front-load description with direct hub link: "🎁 Grab this free resource in my free community → {YOUR_COMMUNITY_URL}". The YouTube first comment should also drive to the free community — e.g. "I put together free resources on this inside my free community → {YOUR_COMMUNITY_URL}". Never use "Comment X" keyword CTAs on YouTube — those only work on Instagram/TikTok via ManyChat.
4. The same keyword MUST be used across all platform copies for the same video
5. Do NOT reuse the same keyword across multiple scripts in the same batch — use 5 different keywords for 5 scripts

---

## ICP Targeting Rules

### 5-Angle / ICP Matrix

| Angle Type | ICP Target | Hook Patterns | Emotional Register | MG Visual Default |
|---|---|---|---|---|
| Story | Primary (TOFU) | Journey Tease, Step-by-Step Tease | Curious / Energised | Coding interface, workflow diagram |
| Tool-Focus | Primary (TOFU) | Product Drop, Result Reveal | Excited / Empowered | UI walkthrough, tool logo |
| Concept | Primary (TOFU) | Pain Interrupt, Elimination | Challenged / Validated | Abstract tech, counter graphic |
| Value-Drop | Primary (TOFU) | Value-Drop, Step-by-Step Tease | Relieved / Grateful | Clean logo badge, high-level workflow |
| Before/After | Secondary (BOFU) | Result Reveal, Pain Interrupt | Pragmatic / Proof-hungry | Cost counter, side-by-side comparison |

### Batch Diversity Requirement

Every batch of 5 scripts MUST meet all three:

1. **Minimum 1 Secondary ICP (Before/After)** script per batch
2. **Maximum 2 scripts of any single angle type** in a batch
3. **Minimum 2 distinct emotional registers** across the 5 scripts

### Before/After Angle Writing Rules

Before/After scripts target the **Secondary ICP (BOFU)** only. Every rule below is mandatory.

- **Hook:** Must name a specific business pain with a metric. Example: "We were losing 12 hours a week to manual reporting." NOT "We had a problem with reports."
- **Body structure:** Old state (how things were, with specific cost/time) → Trigger (what changed — the AI system introduced) → New state (the measurable result)
- **Metrics mandatory:** At least one of the following must appear in the body: time saved (hrs/week), money saved ($/month or $/year), or headcount redirected (X people freed up)
- **CTA:** MUST use a BOFU keyword — AUDIT, AI, RESULTS, ROI, or SYSTEM. NEVER use TOFU keywords (BUILD, AGENT, TEMPLATE, etc.) in a Secondary ICP script
- **Platform copy tone:** LinkedIn-forward and ROI-forward. Treat all three platforms as if the primary reader is a business owner evaluating proof, not a developer wanting to learn
- **ROI-framing test:** Before finalising each body sentence, ask "Would a 45-year-old SME owner care about this?" If the sentence is about syntax, tooling choices, or developer internals, reframe it as a business outcome

### Language Register Enforcement

Apply the correct voice for each ICP. Same insight, different frame:

| Insight | Primary (TOFU) — Builder Voice | Secondary (BOFU) — Decision Maker Voice |
|---|---|---|
| Automation | "Deploy an n8n workflow that handles this automatically." | "Eliminate 8 hours per week per team member. No new hires needed." |
| Cost | "This is completely free — open source, self-hosted." | "Replaces $2,400/month in SaaS subscriptions — same outcome, one system." |
| Speed | "I shipped this in 2 hours with Claude Code and Cursor." | "Implementation done in under a week. ROI inside the first month." |
| CTA | "Comment BUILD for the template." | "Comment AUDIT for the ROI checklist." |

**TOFU keywords** (Primary ICP only): AGENT, BUILD, CLAUDE, CURSOR, TEMPLATE, WORKFLOW, AUTOMATE, STACK, n8n, DEPLOY, SHIP
**BOFU keywords** (Secondary ICP only): AUDIT, AI, RESULTS, ROI, SYSTEM
