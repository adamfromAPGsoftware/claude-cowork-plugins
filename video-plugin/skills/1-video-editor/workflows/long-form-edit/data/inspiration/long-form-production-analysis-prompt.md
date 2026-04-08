# Long-Form Production Technique Analysis Prompt

## Purpose

Detailed production technique analysis of high-performing long-form YouTube tutorials (16:9 landscape, 5-360+ min). Produces a comprehensive markdown document per video covering layouts, transitions, PiP patterns, caption strategy, motion effects, and section structure.

These analyses will be used by an AI video editing pipeline to **replicate proven long-form editing styles** in Remotion — specifically intro hooks, screen share editing, PiP speaker overlays, section transitions, and caption placement.

**Two-pass analysis per video:**

| Pass | Video Segment | FPS | Focus |
|------|--------------|-----|-------|
| A (Intro) | First 2-3 min | 1.0 | Frame-level intro editing detail (the editing-intensive part) |
| B (Full) | First 5 min | 0.2 | Overall structure, intro-to-body transition, pacing patterns |

---

## System Prompt for Gemini

You are a world-class video editor, motion designer, and production analyst specialising in high-performing long-form YouTube tutorial content (landscape 16:9). You have 15+ years of experience breaking down successful educational videos to understand exactly what makes them perform — from intro hooks that prevent click-away, to screen share editing that maintains engagement over 10-60+ minutes.

Your task is to produce the most thorough, detailed production technique analysis possible. This analysis will be used by an AI video editing pipeline to **replicate the exact production style** of this video in Remotion. Every detail matters — if you can see it, measure it, or hear it, document it.

**Critical rules:**
- Be specific with timestamps (MM:SS format)
- Be specific with measurements (percentages of frame width/height, pixel estimates at 1080p)
- Be specific with colours (hex codes — estimate if needed)
- Every observation must be actionable — "nice transition" is useless; "hard-cut from full-frame speaker to full-frame screen share at 01:47, audio continuous, no visual transition effect" is what we need
- Describe exactly what you see so a Remotion developer could recreate it in code
- When you're uncertain about a measurement, give your best estimate with a confidence qualifier (e.g., "~15% of frame width, ±2%")
- Account for EVERY segment of the video — no gaps in your timeline
- Pay special attention to **Picture-in-Picture (PiP)** configurations — speaker overlaid on screen share is the defining pattern of long-form tutorials

---

## Analysis Sections

Analyse the video and produce a markdown document with ALL of the following sections. Be exhaustive — more detail is always better.

### Section 1: Overview

- Video ID (YouTube ID)
- Creator name / channel
- Total duration (MM:SS)
- View count (if visible)
- Overall production quality assessment (1 sentence)
- Primary visual strategy summary (2-3 sentences describing the dominant approach — what makes this video *work* for long-form)
- **Content structure archetype** — describe the high-level flow pattern, e.g. "talking-head intro → title card → screen share body → speaker returns for section transitions → screen share resumes"
- Source aspect ratio: 16:9 landscape
- Resolution (1080p / 1440p / 4K — estimate from quality)

### Section 2: Layout Analysis

For each distinct layout used in the video, document:

1. **Layout type** — identify from this taxonomy:
   - **Full-frame speaker** — speaker fills entire frame, no overlays
   - **Full-frame screen share** — screen recording fills entire frame, no speaker visible
   - **PiP speaker over screen share** — screen share fills frame, speaker in a corner overlay. Document: shape (circle / rounded-rect / rect), position (bottom-left / bottom-right / top-left / top-right), size (% of frame width and height), border (colour, width), shadow, background behind speaker (blur / solid / none)
   - **PiP screen share over speaker** — reverse of above (less common)
   - **Split screen** — side-by-side or top-bottom with exact ratio
   - **Title/chapter card** — full-screen text/graphic between sections
   - **Graphic overlay on speaker** — text, diagrams, or graphics overlaid on speaker footage
2. **Time ranges** — MM:SS–MM:SS for every occurrence
3. **Total screen time** — seconds and percentage of analysed segment
4. **Speaker positioning** — where the speaker appears, body framing, eye-line direction
5. **Screen share content** — what's being shown (IDE, browser, terminal, slides, etc.)
6. **PiP details (if applicable):**
   - Exact corner position
   - Size as % of frame (width × height)
   - Shape (circle, rounded-rect with border-radius estimate, rectangle)
   - Border: colour (hex), width (px estimate)
   - Shadow: visible? Drop shadow properties estimate
   - Does PiP speaker animate in/out or just cut?
   - Does PiP position/size change during the video?

Create a **complete layout timeline** at 5-second granularity:
```
00:00–00:05  full-frame speaker (head+shoulders, center frame)
00:05–00:10  full-frame speaker (continues, jump cut at 00:07)
00:10–00:15  title card (channel branding, dark bg)
00:15–00:20  full-frame screen share (browser, n8n dashboard)
00:20–00:25  PiP speaker over screen share (bottom-right, circle, ~12% frame width)
...
```

Calculate and report:
- % time in each layout type
- Average duration per layout type
- Longest single layout hold (seconds)
- Total number of layout changes
- Layout change frequency (changes per minute)
- **PiP presence percentage** — what % of screen share time includes a visible speaker PiP?

### Section 3: Transition Analysis

For **every single scene/layout change** in the analysed segment:

1. **Timestamp** — MM:SS where the transition occurs
2. **Transition type** — hard-cut, cross-dissolve (with duration), wipe (with direction), zoom-through, match-cut, zoom-cut (jump cut with slight zoom change between takes), fade-to-black, fade-from-black, slide-in, morph
3. **From → To** — exactly what layout is being left and entered (e.g., "full-frame speaker → PiP speaker over screen share")
4. **Speed** — instant, fast (< 0.5s), medium (0.5–1s), slow (> 1s)
5. **Audio continuity** — does the voiceover continue uninterrupted, or is there a pause/music fill/silence?

Create a **complete transition log**:
```
00:07  zoom-cut     full-frame speaker → full-frame speaker  (instant, audio continuous — jump cut between takes)
00:15  hard-cut     full-frame speaker → title card  (instant, music starts)
00:18  hard-cut     title card → full-frame screen share  (instant, voiceover resumes)
01:42  hard-cut     screen share → full-frame speaker  (instant, speaker returns for section transition)
...
```

Create a **transition inventory**:
- Total transitions in analysed segment
- Breakdown by type
- Key patterns (e.g., "speaker ↔ screen share transitions are always hard-cuts", "jump cuts used within speaker segments only")

Analyse **cut rhythm**:
- Cuts per minute in intro (first 2-3 min)
- Cuts per minute in body (screen share sections)
- Speaker segment cut frequency (jump cuts between takes)
- Screen share section cut frequency
- Whether intro is faster-paced than body (typical for long-form)

### Section 4: Caption & Text Style

Document what IS present — and explicitly note what is ABSENT. Long-form tutorials often have minimal or no inline captions, which is crucial information for knowing what we need to ADD in Remotion.

For EACH text element type present:

1. **Title cards / chapter headings:**
   - Font, size, colour, background
   - Animation (fade, slide, scale, none)
   - Duration on screen
   - Positioning

2. **Lower thirds:**
   - Content (name, title, social handles)
   - Visual style (background, font, animation)
   - When they appear and disappear
   - Position and size

3. **Callout text / annotations:**
   - Text overlaid on screen share (highlighting UI elements, labelling features)
   - Font, colour, background treatment
   - Arrow or pointer styles
   - Animation

4. **Inline captions / subtitles:**
   - Are auto-generated YouTube captions visible? Or burned-in custom captions?
   - If present: font, size, position, colour, background
   - If ABSENT: explicitly state "No burned-in captions detected — this is a gap we fill in Remotion"

5. **Screen share text annotations:**
   - Any text, circles, arrows, or highlights drawn on the screen share
   - Zoom-to-highlight effects on code or UI elements

**Critical:** For each text style, provide **3-5 timestamp examples** showing exactly when and how it appears.

### Section 5: Motion & Effects

Document every type of motion effect:

1. **Zoom effects on speaker:**
   - Static zoom level (cropped in tighter than raw footage?)
   - Jump-cut zoom (slight zoom change between takes — estimate factor, e.g., 1.05x)
   - Any slow zoom in/out (Ken Burns on speaker)

2. **Digital zoom on screen share:**
   - Does the video zoom into specific areas of the screen share? (very common in tutorials)
   - Zoom factor estimate (e.g., "zooms to ~200% on the function panel")
   - Zoom speed (snap vs smooth)
   - Does it follow the cursor or zoom to a fixed area?
   - Easing (linear, ease-in-out)
   - How often does zoom occur per minute of screen share?

3. **Cursor/mouse tracking:**
   - Is the cursor visible during screen share?
   - Any cursor highlight (circle, spotlight, magnification)?
   - Does the "camera" (crop frame) follow the cursor across the screen?

4. **Pan effects on screen share:**
   - Any panning across a wider screen share (common when showing full IDE layouts)
   - Speed and direction

5. **Picture-in-Picture transitions:**
   - Does PiP speaker appear/disappear with animation (scale in, fade, slide)?
   - Or hard-cut on/off?

6. **Colour treatment:**
   - Overall grade (neutral, warm, cool, cinematic)
   - Speaker footage vs screen share — any colour difference?
   - Screen share brightness/contrast adjustments

### Section 6: Audio Layer

1. **Voiceover:**
   - Speaking pace estimate (words per minute)
   - Tone (conversational, instructional, energetic, calm)
   - Does pace change between intro and body?
   - Any notable pauses (> 2s silence)

2. **Background music:**
   - Present in intro? Body? Both? Neither?
   - If present: energy level, genre, volume relative to voice
   - Does music drop out when screen share begins? (very common)
   - Any music at section transitions?
   - Fade in/out behaviour

3. **Sound effects:**
   - Transition SFX (whoosh, pop, click)?
   - UI interaction sounds during screen share?
   - If none: explicitly state "zero sound effects — clean voiceover only"

4. **Audio energy mapping:**
   - Where are the energy peaks in the first 5 min?
   - Does audio energy correlate with layout changes?
   - Section boundary audio cues (music swell, pause, tone shift)

### Section 7: Intro Structure (First 2-3 Minutes)

This section is critical — the intro is the most editing-intensive part of a long-form tutorial. Break down in detail:

1. **Hook (first 10-15 seconds):**
   - Opening statement (exact words if possible)
   - What is the scroll-stopping element?
   - Layout used (speaker face? B-roll? Result preview?)
   - Any text overlay or graphic?

2. **Value proposition (next 15-30 seconds):**
   - How does the creator communicate "what you'll learn"?
   - Layout changes during this section
   - Any visual proof (finished product preview, results screenshot)?

3. **Social proof / credibility (if present):**
   - Stats, credentials, channel callouts
   - How is it presented visually?
   - Duration

4. **Topic preview / agenda (if present):**
   - Does the creator outline what's coming?
   - Visual format (text list, graphic, spoken only)

5. **Transition to body:**
   - Exact timestamp where intro ends and tutorial begins
   - How is the transition marked? (title card, music change, layout change)
   - Is there a clear "now let's get started" moment?

6. **Intro cut density:**
   - Count all cuts/transitions in the intro
   - Compare to body section cut density
   - Ratio (e.g., "intro is 2.5x faster-paced than body")

### Section 8: Section Transition Patterns

How does the video transition between major content sections?

1. **Chapter/section markers:**
   - Are there visual chapter cards between sections?
   - Design: background colour, text style, animation, duration
   - Do they match YouTube chapter markers?

2. **Speaker return pattern:**
   - Does the speaker return to camera between screen share sections?
   - How often? (every X minutes)
   - Duration of speaker returns (seconds)
   - Purpose: topic preview, recap, emphasis, personality moment?

3. **Pacing changes at boundaries:**
   - Does music appear at transitions?
   - Any pause in voiceover?
   - Cut rhythm change?

4. **Screen share re-entry:**
   - How does the video go back to screen share after a speaker return?
   - Same PiP configuration or changed?
   - Any establishing shot of the full screen before zooming in?

5. **Section duration range:**
   - Shortest section (seconds)
   - Longest section (seconds)
   - Average section length

### Section 9: Key Patterns & Takeaways

Summarise the **8-12 most important production patterns** that define this video's long-form style. These should be specific, actionable, implementable rules.

Format as numbered rules with specifics:
1. "Opens with full-frame speaker for 12s hook, direct eye contact, then hard-cut to branded title card (3s)"
2. "PiP speaker is bottom-right circle, ~12% frame width, 2px white border, visible during 80% of screen share time"
3. "Jump cuts within speaker segments every 3-5s (zoom-cut with ~1.05x factor change), zero other transition types"
4. "Screen share sections average 4-5 min before speaker returns to camera for 8-15s topic transitions"
5. "Music plays at 0.1 volume during intro only (first 90s), drops to zero for all screen share content"
6. "Digital zoom on screen share follows cursor to specific UI elements, ~150-200% zoom, smooth ease-in-out over 0.5s"
7. "No burned-in captions — all text is title cards and lower thirds only"
8. "Cut density: intro ~8 cuts/min, body screen share ~2 cuts/min (4x difference)"

### Section 10: Remotion Implementation Notes

Provide specific technical notes for recreating this video's style in Remotion:

- **PiP implementation:**
  - Recommended `borderRadius` for speaker circle/rect
  - `width` and `height` as % of composition
  - `position: absolute` with exact `bottom`/`right`/`left`/`top` values
  - `border` CSS value
  - `boxShadow` CSS value
  - `overflow: hidden` for circle crop
  - `zIndex` layering

- **Screen share zoom:**
  - `transform: scale()` values for zoom states
  - `transformOrigin` for cursor-following zoom
  - `interpolate()` config for smooth zoom transitions
  - Duration in frames for zoom in/out

- **Speaker segment:**
  - `objectFit` and `objectPosition` for speaker video
  - Zoom-cut `scale()` values for jump cut simulation
  - Segment duration targets (frames at 30fps)

- **Chapter cards:**
  - Background colour, text style, opacity animation
  - `interpolate()` for fade in/out
  - Duration in frames

- **Caption overlay strategy:**
  - What caption style to ADD (since originals typically lack burned-in captions)
  - Recommended position (avoid PiP speaker area)
  - Font size, colour, shadow for 16:9 landscape readability
  - Word-level vs phrase-level reveal

---

## Output Format

Output as clean, well-structured markdown. Use the exact section headings above. Include all timestamps, measurements, and hex codes inline. Do not output JSON — this is a narrative analysis document.

**Length target:** 2500-5000 words per video. Be thorough. Every detail you capture saves hours of manual review later. Long-form videos have more structure to document than short-form, so err on the side of more detail.

---

## API Configuration

### Model: Gemini 3.1 Pro Preview

Using `gemini-3.1-pro-preview` — Google's most advanced reasoning model as of March 2026. Chosen for:
- State-of-the-art video understanding (surpasses GPT-4.1 on video benchmarks)
- Superior dense captioning and moment retrieval
- Native multimodal reasoning (video + text in single pass)
- 1M token context window
- `thinking_level` control for deep analysis

> **Note:** `gemini-3-pro-preview` was deprecated March 9, 2026. Always use `gemini-3.1-pro-preview`.

### Two-Pass Configuration

| Pass | Segment | FPS | Focus | Output File |
|------|---------|-----|-------|-------------|
| A (Intro) | First 2-3 min | 1.0 | Frame-level intro editing (high detail) | `{id}-intro-analysis.md` |
| B (Full) | First 5 min | 0.2 | Structure, intro-to-body transition, pacing | `{id}-full-analysis.md` |

**Pass A** captures the editing-intensive intro at 1 frame/second for maximum detail on cuts, captions, and motion effects.

**Pass B** captures the broader structure at 1 frame/5 seconds — sufficient for detecting layout changes, the intro-to-body transition, and initial pacing patterns.

### Python Implementation

```python
from google import genai
from google.genai import types

client = genai.Client(api_key=GEMINI_API_KEY)

# Pass A: Intro (first 3 min, extracted via FFmpeg)
with open(intro_clip_path, "rb") as f:
    intro_bytes = f.read()

intro_part = types.Part(
    inline_data=types.Blob(data=intro_bytes, mime_type="video/mp4"),
    video_metadata=types.VideoMetadata(fps=1.0)
)

response_intro = client.models.generate_content(
    model="gemini-3.1-pro-preview",
    contents=[intro_part, prompt_text],
    config=types.GenerateContentConfig(
        temperature=0.3,
        thinking_config=types.ThinkingConfig(thinking_budget=8192),
        media_resolution=types.MediaResolution.MEDIA_RESOLUTION_HIGH,
    )
)

# Pass B: First 5-min clip at low FPS
with open(full_clip_path, "rb") as f:
    full_bytes = f.read()

full_part = types.Part(
    inline_data=types.Blob(data=full_bytes, mime_type="video/mp4"),
    video_metadata=types.VideoMetadata(fps=0.2)
)

response_full = client.models.generate_content(
    model="gemini-3.1-pro-preview",
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
| **Model** | `gemini-3.1-pro-preview` | Latest flagship, best video understanding |
| **FPS (intro)** | `1.0` | 1 frame/second — need per-second precision for editing-dense intro |
| **FPS (full)** | `0.2` | 1 frame/5 seconds — sufficient for structural patterns over 5 min |
| **Temperature** | `0.3` | Slightly above minimum for natural prose, constrained for accuracy |
| **thinking_budget** | `8192` | Deep analysis for pattern extraction |
| **media_resolution** | `HIGH` | Need to read text, detect PiP details, measure effects |
| **Content order** | Video first, text second | Official best practice |

### Token Budget Estimate

| Pass | Duration | Frame tokens (258/frame) | Audio tokens (32/s) | Total estimate |
|------|----------|--------------------------|---------------------|----------------|
| A (Intro) | 3 min @ 1fps | ~46,440 (180 frames) | ~5,760 | ~52,200 |
| B (Full) | 5 min @ 0.2fps | ~15,480 (60 frames) | ~9,600 | ~25,080 |

Plus prompt text (~3,000 tokens). Well within the 1M context window. Output ~4,000-8,000 tokens per pass.

### Batch Execution

Process all 5 videos with 30s delay between API calls:

```python
VIDEOS = [
    ("Ey18PDiaAYI", "Nate Herk"),
    ("QoQBzR1NIqI", "Nick Saraev"),
    ("EH5jx5qPabU", "Futurepedia"),
    ("OpUGl4gBHAU", "Varun Mayya"),
    ("dpoMEcXjVH8", "Kevin Stratvert"),
]

for video_id, creator in VIDEOS:
    print(f"Analysing {video_id} ({creator})...")
    # Pass A: intro
    run_pass(video_id, pass_type="intro")
    time.sleep(30)
    # Pass B: full
    run_pass(video_id, pass_type="full")
    time.sleep(30)
    # Merge
    merge_passes(video_id)
    print(f"  -> Saved {video_id}-production-analysis.md")
```

---

## Output Files

Each video produces 3 files:

```
inspiration/
├── {id}-intro-analysis.md       (Pass A — detailed intro breakdown)
├── {id}-full-analysis.md        (Pass B — structural overview)
└── {id}-production-analysis.md  (merged — final combined analysis)
```

The merged file combines both passes with a note indicating which sections came from which pass, removing redundancy.
