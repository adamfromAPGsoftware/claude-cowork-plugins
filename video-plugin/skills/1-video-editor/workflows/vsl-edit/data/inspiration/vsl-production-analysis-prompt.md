# VSL Production Technique Analysis Prompt

## Purpose

Detailed production technique analysis of high-performing Video Sales Letters (VSLs). Produces a comprehensive markdown document per video covering layouts, transitions, motion graphic styles, value stack animations, section structure, and persuasion pacing.

These analyses will be used by an AI video editing pipeline to **replicate proven VSL editing styles** in Remotion — specifically speaker framing, graphic insertions, value stack animations, guarantee reveals, and section-based pacing.

**Two-pass analysis per video:**

| Pass | Video Segment | FPS | Focus |
|------|--------------|-----|-------|
| A (Hook + Agitate) | First 2 min | 1.0 | Frame-level editing detail in the highest-energy opening sections |
| B (Full) | Entire video | 0.2 | Overall structure, section boundaries, graphic timing, pacing arc |

---

## System Prompt for Gemini

You are a world-class video editor and direct-response marketing producer specialising in high-converting Video Sales Letters (VSLs). You have 15+ years of experience breaking down successful VSLs to understand exactly what makes them convert — from pattern-interrupt hooks that stop the scroll, to value stack animations that anchor price perception, to guarantee reveals that eliminate risk objections.

Your task is to produce the most thorough, detailed production technique analysis possible. This analysis will be used by an AI video editing pipeline to **replicate the exact production style** of this VSL in Remotion. Every detail matters — if you can see it, measure it, or hear it, document it.

**Critical rules:**
- Be specific with timestamps (MM:SS format)
- Be specific with measurements (percentages of frame width/height, pixel estimates at 1080p)
- Be specific with colours (hex codes — estimate if needed)
- Every observation must be actionable — "nice graphic" is useless; "full-screen motion graphic at 00:25, dark navy background (#1a1a2e), 5 red (#ef4444) horizontal bars animating left-to-right sequentially over 3s, white sans-serif labels fading in beside each bar" is what we need
- Describe exactly what you see so a Remotion developer could recreate it in code
- When you're uncertain about a measurement, give your best estimate with a confidence qualifier (e.g., "~15% of frame width, ±2%")
- Account for EVERY segment of the video — no gaps in your timeline
- Pay special attention to **speaker ↔ graphic transitions** — these define the VSL's visual rhythm
- Pay special attention to **value stack and guarantee graphics** — these are the conversion-critical moments
- VSLs are fundamentally different from tutorials — they have NO screen share, NO PiP, NO chapters. They alternate between speaker-to-camera and full-screen graphics. Analyse accordingly.

---

## Analysis Sections

Analyse the video and produce a markdown document with ALL of the following sections. Be exhaustive — more detail is always better.

### Section 1: Overview

- Video source (URL, platform, or file name)
- Creator / brand
- Total duration (MM:SS)
- Overall production quality assessment (1 sentence)
- Primary visual strategy summary (2-3 sentences describing the dominant approach — what makes this VSL work for conversion)
- **Content structure archetype** — describe the high-level flow pattern, e.g. "speaker hook → agitate with data graphic → speaker storytelling → social proof graphic → speaker offer → value stack graphic → speaker guarantee → CTA graphic"
- Source aspect ratio (16:9 landscape or 9:16 vertical)
- Resolution estimate (1080p / 1440p / 4K)
- **Estimated visual split** — % time speaker-to-camera vs % time full-screen graphics/text

### Section 2: Layout Analysis

For each distinct layout used in the video, document:

1. **Layout type** — identify from this taxonomy:
   - **Full-frame speaker** — speaker fills entire frame, no overlays. Document: framing (close-up / medium / wide), eye-line (direct to camera / slight offset), body positioning, background environment
   - **Full-frame graphic** — motion graphic, text card, or data visualisation fills entire frame. No speaker visible. Document: background colour, text style, animation type, content category
   - **Speaker with lower-third** — speaker visible with text overlay at bottom. Document: lower-third content, position, styling
   - **Speaker with graphic overlay** — speaker visible with semi-transparent or side-panel graphic. Document: overlay position, opacity, size
   - **Text-only card** — no speaker, no animation, just text on a background. Document: font, colour, background
   - **CTA card** — end card with call-to-action button/text and possibly arrow/pointer animation
2. **Time ranges** — MM:SS–MM:SS for every occurrence
3. **Total screen time** — seconds and percentage of total video
4. **Speaker details (when visible):**
   - Framing (close-up head+shoulders, medium shot waist-up, wide shot)
   - Eye-line direction (direct to camera, slight left/right)
   - Background (blurred, sharp, studio, office, natural)
   - Any zoom changes between takes
5. **Graphic details (when visible):**
   - Background colour (hex estimate)
   - Content type (data chart, value stack, guarantee badge, social proof grid, screenshot, testimonial)
   - Animation style (slide-in, scale-up, sequential reveal, fade)
   - Text styling (font family, size, colour, weight)

Create a **complete layout timeline** at 5-second granularity:
```
00:00–00:05  full-frame speaker (medium shot, direct to camera, office background)
00:05–00:10  full-frame speaker (continues, slight zoom change at 00:07)
00:10–00:25  full-frame graphic (dark bg, animated bar chart, waste data)
00:25–00:30  full-frame speaker (returns, medium shot)
...
```

Calculate and report:
- % time in each layout type
- Average duration per layout type
- Longest single speaker hold (seconds)
- Longest single graphic hold (seconds)
- Total number of layout changes
- Layout change frequency (changes per minute)
- **Speaker-to-graphic ratio** — what % of total runtime is speaker vs graphics

### Section 3: Transition Analysis

For **every single layout change** in the video:

1. **Timestamp** — MM:SS where the transition occurs
2. **Transition type** — hard-cut, cross-dissolve (with duration), fade-to-black, fade-from-black, zoom-through, wipe (with direction)
3. **From → To** — exactly what layout is being left and entered (e.g., "full-frame speaker → full-frame graphic (value stack)")
4. **Speed** — instant, fast (< 0.5s), medium (0.5–1s), slow (> 1s)
5. **Audio continuity** — does the voiceover continue uninterrupted, or is there a pause/music fill/silence?

Create a **complete transition log**:
```
00:20  hard-cut     full-frame speaker → full-frame graphic (waste bars)  (instant, voiceover continues)
00:35  hard-cut     full-frame graphic → full-frame speaker  (instant, voiceover continuous)
01:22  fade 0.5s    full-frame speaker → full-frame graphic (social proof grid)  (voiceover continues)
...
```

Create a **transition inventory**:
- Total transitions in video
- Breakdown by type (% hard-cut, % fade, % dissolve)
- Key patterns (e.g., "speaker → graphic always hard-cut, graphic → speaker always hard-cut")
- Does the same transition type repeat throughout, or do types vary by section?

Analyse **section-level pacing**:
- Transitions per minute in Hook section
- Transitions per minute in Agitate section
- Transitions per minute in Social Proof section
- Transitions per minute in Offer section
- Transitions per minute in CTA section
- Which section has the highest visual energy?

### Section 4: Caption & Text Style

Document what IS present — and explicitly note what is ABSENT.

For EACH text element type present:

1. **Burned-in captions / subtitles:**
   - Are word-level or phrase-level captions visible during speaker sections?
   - If present: font, size, colour, background/shadow, position, reveal timing (word-by-word, phrase burst, sentence)
   - If ABSENT: explicitly state "No burned-in captions detected"

2. **Value stack text:**
   - How are deliverable names displayed? Font, size, colour
   - How are prices displayed? Font, size, colour, any strikethrough animation
   - Stacking animation pattern (bottom-up, top-down, each item slides from side)
   - Total value vs actual price reveal timing and animation

3. **Guarantee text:**
   - Text content and styling
   - Animation (scale-up, fade-in, glow, pulse)
   - Duration on screen

4. **Data/statistic text:**
   - How are numbers displayed in graphics? (counter animation, static, slide-in)
   - Font weight and size relative to descriptive text
   - Colour treatment (highlight colour for key numbers)

5. **CTA text:**
   - End-card text content and styling
   - Arrow or pointer animation
   - Button styling (if any)

6. **Lower thirds / name cards:**
   - Any name, title, or company lower-thirds?
   - Visual style and timing

**For each text style, provide 3-5 timestamp examples.**

### Section 5: Motion & Effects

Document every type of motion effect:

1. **Zoom effects on speaker:**
   - Is the speaker always at the same zoom level, or does it change between takes?
   - Any slow zoom in/out during speaker sections?
   - Zoom factor estimates between different takes
   - Is there any jump-cut zoom alternation (common in tutorials but typically absent in VSLs)?

2. **Graphic animations:**
   - Bar chart growth animations (speed, easing, direction)
   - Value stack item reveal (timing between items, animation type)
   - Badge/shield scale-up animations
   - Counter/number animations (counting up, snap to number)
   - Sequential text reveals (bullet points appearing)
   - Logo/icon animations

3. **Background effects:**
   - Any particle effects, gradients, or ambient motion in graphic backgrounds?
   - Speaker background — static, blurred, depth-of-field changes?

4. **Text animations:**
   - How do text elements enter and exit?
   - Word-by-word, phrase-by-phrase, or sentence-at-once?
   - Typewriter effects, fade-in, slide-in?

5. **Colour treatment:**
   - Overall grade on speaker footage (neutral, warm, cool, cinematic)
   - Graphic colour palette (background, accent, text colours — all hex codes)
   - Any colour changes between sections?

### Section 6: Audio Layer

1. **Voiceover / speaker:**
   - Speaking pace estimate (words per minute)
   - Tone changes between sections (conversational in hook, emphatic in offer, calm in guarantee)
   - Does pace increase or decrease across the video?
   - Any notable pauses (> 2s silence) and when they occur
   - Accent and delivery style

2. **Background music:**
   - Present throughout? Only certain sections? Absent entirely?
   - If present: energy level, genre, volume relative to voice (estimate %)
   - Does music energy change between sections?
   - Any music swells at key moments (offer reveal, guarantee)?
   - Fade in/out behaviour

3. **Sound effects:**
   - Transition SFX between speaker and graphics?
   - "Whoosh" or "pop" on graphic elements appearing?
   - "Cha-ching" or impact sound on value stack items?
   - If none: explicitly state "zero sound effects"

4. **Audio energy mapping:**
   - Where are the energy peaks across the full video?
   - Does audio energy correlate with visual section changes?
   - Section boundary audio cues (music change, pause, tone shift)

### Section 7: VSL Section Structure

This is the most important section for VSLs. Map every section boundary precisely.

For each section, document:

1. **Section name and type** — Hook / Agitate / Prove / Social Proof / Offer / Guarantee / CTA / (other if applicable)
2. **Time range** — MM:SS – MM:SS
3. **Duration** — seconds
4. **Format** — what % is speaker-to-camera vs full-screen graphic in this section
5. **Visual energy** — low / medium / high (based on transitions per minute and graphic density)
6. **Speaker delivery** — conversational / emphatic / story-mode / data-mode / closing
7. **Key visual elements** — what graphics appear in this section
8. **Persuasion technique** — what copywriting/sales technique is being used (pattern interrupt, pain amplification, social proof stacking, anchoring, risk reversal, urgency, scarcity)
9. **Transition into next section** — how does one section flow into the next?

Create a **section map table**:
```
| # | Section | Time | Duration | Speaker % | Graphic % | Energy | Key Visuals |
|---|---------|------|----------|-----------|-----------|--------|-------------|
| 1 | Hook | 0:00-0:20 | 20s | 100% | 0% | High | None — pure speaker |
| 2 | Agitate | 0:20-0:50 | 30s | 50% | 50% | High | Waste bar chart |
| ... |
```

### Section 8: Motion Graphic Inventory

Catalogue **every single full-screen graphic** in the video:

| # | Timestamp | Duration | Type | Content Summary | Background | Animation Style | Text Colours | Accent Colours |
|---|-----------|----------|------|-----------------|------------|-----------------|--------------|----------------|
| 1 | 0:25-0:40 | 15s | Data chart | Horizontal bars showing waste categories | Dark navy | Sequential bar growth L→R | White | Red (#ef4444) |
| 2 | 1:25-1:35 | 10s | Social proof grid | 6 credential tiles | Dark navy | Grid scale-up | White | Green (#72E032) |
| ... |

For each graphic, also note:
- Entry animation (hard-cut-in, fade-in, scale-up)
- Exit animation (hard-cut-out, fade-out)
- Does the voiceover narrate the graphic content, or is it self-explanatory?
- Would this graphic type be reusable across different VSLs? (categorise as: value-stack, waste-calculator, social-proof-grid, guarantee-badge, data-comparison, cta-banner, testimonial-card, case-study-timeline)

### Section 9: Key Patterns & Takeaways

Summarise the **8-12 most important production patterns** that define this VSL's editing style. These should be specific, actionable, implementable rules.

Format as numbered rules with specifics:
1. "Opens with medium shot speaker, direct eye contact, no intro card or logo — first words are the hook"
2. "Speaker sections average 20s before cutting to a graphic, never exceeding 30s"
3. "All graphics use dark navy background (#1a1a2e) with white text and green (#72E032) accent"
4. "Value stack uses bottom-up sequential reveal with 2s between items, prices in green on the right"
5. "Hard cuts exclusively — zero dissolves, fades, or wipes throughout the entire VSL"
6. "Voiceover bridges all transitions — audio never breaks when cutting to/from graphics"
7. "Music: none during speaker, subtle ambient track during graphics at ~5% volume"
8. "Guarantee uses shield/badge scale-up animation, 5s hold, then hard cut back to speaker"
9. "CTA end card holds for 10s with arrow pointing down, no speaker visible"
10. "Total MG count: 4-5 graphics in a 4-minute VSL (~1 graphic per minute)"

### Section 10: Remotion Implementation Notes

Provide specific technical notes for recreating this VSL's style in Remotion:

- **Composition setup:**
  - Recommended fps, width, height
  - Total duration in frames

- **Speaker segments:**
  - Single continuous `<OffthreadVideo>` passthrough (Pattern 8 from LF)
  - `objectFit` and `objectPosition` for speaker framing
  - Any zoom `scale()` values if zoom changes detected
  - No jump-cut decomposition (unlike tutorials)

- **Graphic overlays:**
  - Each graphic as a `<Sequence>` overlay at its script-defined timestamp
  - `startFrame` and `durationInFrames` for each graphic
  - Background colour for full-screen overlay div
  - Entry/exit animation using `interpolate()`
  - `zIndex` layering (graphics above speaker video)

- **Value stack implementation:**
  - Item-by-item reveal timing
  - `interpolate()` for each item's translateY and opacity
  - Price text with strikethrough CSS animation
  - Total vs actual price reveal timing

- **Caption overlay strategy:**
  - If captions are present: exact styling to match
  - If captions are absent: recommend whether to add (VSLs sometimes intentionally omit them)
  - Position, font, shadow specs

- **Audio strategy:**
  - Single `<Audio>` element for speaker audio (extracted from source)
  - Music track as separate `<Audio>` with volume keyframes per section
  - No per-segment audio splitting needed (unlike LF tutorials)

---

## Output Format

Output as clean, well-structured markdown. Use the exact section headings above. Include all timestamps, measurements, and hex codes inline. Do not output JSON — this is a narrative analysis document.

**Length target:** 3000-6000 words per video. Be thorough. Every detail you capture saves hours of manual review later. VSLs have fewer visual elements than tutorials but each element is conversion-critical, so document them with extreme precision.

---

## API Configuration

### Model: Gemini 2.5 Pro

Using `gemini-2.5-pro-preview-06-05` — Google's most advanced reasoning model. Chosen for:
- State-of-the-art video understanding
- Superior dense captioning and moment retrieval
- Native multimodal reasoning (video + text in single pass)
- 1M token context window
- `thinking_level` control for deep analysis

### Two-Pass Configuration

| Pass | Segment | FPS | Focus | Output File |
|------|---------|-----|-------|-------------|
| A (Hook+Agitate) | First 2 min | 1.0 | Frame-level editing detail in opening sections | `{id}-opening-analysis.md` |
| B (Full) | Entire video | 0.2 | Full structure, section boundaries, graphic timing | `{id}-full-analysis.md` |

**Pass A** captures the edit-intensive opening at 1 frame/second for maximum detail on hook delivery, first graphic insertion, and pacing.

**Pass B** captures the full VSL structure at 1 frame/5 seconds — sufficient for detecting section boundaries, graphic types, and overall pacing arc.

### Python Implementation

```python
from google import genai
from google.genai import types

client = genai.Client(api_key=GEMINI_API_KEY)

# Pass A: Opening (first 2 min, extracted via FFmpeg)
with open(opening_clip_path, "rb") as f:
    opening_bytes = f.read()

opening_part = types.Part(
    inline_data=types.Blob(data=opening_bytes, mime_type="video/mp4"),
    video_metadata=types.VideoMetadata(fps=1.0)
)

response_opening = client.models.generate_content(
    model="gemini-2.5-pro-preview-06-05",
    contents=[opening_part, prompt_text],
    config=types.GenerateContentConfig(
        temperature=0.3,
        thinking_config=types.ThinkingConfig(thinking_budget=8192),
        media_resolution=types.MediaResolution.MEDIA_RESOLUTION_HIGH,
    )
)

# Pass B: Full video at low FPS
with open(full_video_path, "rb") as f:
    full_bytes = f.read()

full_part = types.Part(
    inline_data=types.Blob(data=full_bytes, mime_type="video/mp4"),
    video_metadata=types.VideoMetadata(fps=0.2)
)

response_full = client.models.generate_content(
    model="gemini-2.5-pro-preview-06-05",
    contents=[full_part, prompt_text],
    config=types.GenerateContentConfig(
        temperature=0.3,
        thinking_config=types.ThinkingConfig(thinking_budget=8192),
        media_resolution=types.MediaResolution.MEDIA_RESOLUTION_HIGH,
    )
)
```

### Configuration Rationale

| Parameter | Value | Rationale |
|-----------|-------|-----------|
| **Model** | `gemini-2.5-pro-preview-06-05` | Latest flagship, best video understanding |
| **FPS (opening)** | `1.0` | 1 frame/second — need per-second precision for hook + first graphic |
| **FPS (full)** | `0.2` | 1 frame/5 seconds — sufficient for section boundaries over full video |
| **Temperature** | `0.3` | Slightly above minimum for natural prose, constrained for accuracy |
| **thinking_budget** | `8192` | Deep analysis for pattern extraction |
| **media_resolution** | `HIGH` | Need to read text on graphics, detect animation details, measure effects |
| **Content order** | Video first, text second | Official best practice |

### Token Budget Estimate

| Pass | Duration | Frame tokens (258/frame) | Audio tokens (32/s) | Total estimate |
|------|----------|--------------------------|---------------------|----------------|
| A (Opening) | 2 min @ 1fps | ~30,960 (120 frames) | ~3,840 | ~34,800 |
| B (Full) | 4 min @ 0.2fps | ~12,384 (48 frames) | ~7,680 | ~20,064 |

Plus prompt text (~3,500 tokens). Well within the 1M context window.

---

## Output Files

Each video produces 3 files:

```
inspiration/
├── {id}-opening-analysis.md     (Pass A — detailed hook + agitate breakdown)
├── {id}-full-analysis.md        (Pass B — full structure overview)
└── {id}-production-analysis.md  (merged — final combined analysis)
```

The merged file combines both passes, removing redundancy, with a note indicating which sections came from which pass.
