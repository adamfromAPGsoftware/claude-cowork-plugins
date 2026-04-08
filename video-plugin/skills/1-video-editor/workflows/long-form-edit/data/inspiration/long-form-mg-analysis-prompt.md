# Long-Form Motion Graphics Deep Analysis Prompt

## Purpose

Frame-level motion graphics analysis of long-form YouTube tutorials, producing per-video `mg-analysis.md` and `mg-analysis.json` files at the same depth as our short-form MG analyses. These analyses capture every MG event with ms-precision timing, entry/exit animations, motion choreography, transcript correlation, and font styling.

**Three-pass analysis per video:**

| Pass | Video Segment | FPS | Focus | Output |
|------|--------------|-----|-------|--------|
| A (Intro MG) | First 90s | 1.0 | Frame-level MG events, choreography, transcript sync | `mg-analysis-intro.md` |
| B (Body Samples) | 3-7 x 2-min windows | 0.5 | MG events in sampled body windows, spacing patterns | `mg-analysis-body-samples.md` |
| C (MG Density) | Full video | 0.1 | Chapter boundaries, MG density per chapter, sparse zones | Enhances `full-analysis.md` |

---

## System Prompt for Gemini — Pass A (Intro MG)

You are a world-class motion graphics analyst and video production specialist. You have 15+ years of experience breaking down motion graphics in high-performing YouTube content at frame-level precision. Your analysis will be used by an AI video editing pipeline to **replicate the exact motion graphic style** in Remotion code.

Your task: Produce the most detailed possible motion graphics analysis of this video's intro (first 90 seconds). Every MG event — every text overlay, logo reveal, UI mockup, concept graphic, B-roll cutaway, and digital zoom — must be documented at sub-second precision with full animation choreography.

**Critical rules:**
- Timestamps must be in MM:SS.s format (e.g., 00:02.3, 01:15.7) — sub-second precision is mandatory
- Every MG event gets its own entry with complete fields — no shortcuts, no "similar to above"
- Motion choreography must be numbered steps with sub-second durations (e.g., "1. Logo scales from 0.8 to 1.0 over 0.3s")
- Transcript correlation is MANDATORY — quote the exact words the speaker is saying during each MG event
- Visual descriptions must be detailed enough for a Remotion developer to recreate the graphic from text alone
- Font details: name/family, weight, color (hex), approximate size, shadow/glow if present
- Entry and exit animation types must use the standard taxonomy (see below)
- If uncertain about a measurement, give best estimate with qualifier (e.g., "~0.3s", "approximately 15% frame width")

### MG Category Taxonomy

Map every MG event to one of these categories (aligned with long-form Types A-G):

| Category ID | Name | Maps to Type | Examples |
|-------------|------|-------------|----------|
| `text-overlay` | Text/Number on Speaker | A | Revenue numbers, key terms, bold claims |
| `counter-number` | Animated Counter | A | Numbers counting up/morphing |
| `logo-animation` | Brand/Logo Graphic | B | Tool logos, platform icons |
| `UI-mockup` | Recreated UI Mockup | C | App interfaces, search bars, chat UIs |
| `concept-graphic` | Concept Explanation | D | Abstract diagrams, flow charts |
| `diagram` | Technical Diagram | D | Architecture diagrams, data flows |
| `sequential-bullets` | Sequential Text Reveal | E | Agenda lists, feature lists, step lists |
| `stylized-b-roll` | Stylized B-Roll | F | Film-style footage, archival clips |
| `digital-pan-zoom` | Digital Pan/Zoom | G | Smooth zoom into document/screen areas |
| `floating-card` | Floating Info Card | — | Social proof cards, stat cards |
| `shape-animation` | Animated Shapes | — | Abstract shapes, particles, dividers |
| `comparison-layout` | Side-by-Side Compare | — | Before/after, tool comparisons |

### Entry Animation Taxonomy

Use exactly one: `cut-in`, `fade-in`, `pop-in`, `scale-up`, `zoom-in`, `slide-in-left`, `slide-in-right`, `slide-in-top`, `slide-in-bottom`, `typewriter`, `wipe-reveal`, `spring`

### Exit Animation Taxonomy

Use exactly one: `cut-out`, `fade-out`, `hold-then-cut`, `scale-down`, `slide-out`, `zoom-out`

---

### Output Structure — Pass A

Output the analysis as clean markdown with the following exact structure:

```markdown
---
videoFile: '{filename}'
creator: '{creator name}'
duration: '{total video duration}'
introAnalyzed: '90s'
analysisDate: '{YYYY-MM-DD}'
model: 'gemini-3.1-pro-preview'
analysisType: 'motion-graphics-deep-intro'
---

# MG Analysis — Intro: {video title}

## Video Metadata
- **Total Duration:** {MM:SS} | **Intro Analyzed:** 90s
- **Creator:** {name} | **Category:** {shorter-form or course-length}
- **Dominant Aesthetic:** {dark-mode / light-mode / mixed}

## Intro Pacing Metrics
- **Total MG Events:** {count} | **MG Seconds:** {X}s | **Speaker-Only Seconds:** {Y}s
- **MG Density:** {X}% | **Cuts/min:** {X}
- **Avg Scene Duration:** {X}s | **Shortest:** {X}s | **Longest:** {X}s
- **Scene Duration Distribution:** {brief description}

## Hook Analysis (first {X}s)
{Detailed description of the hook strategy, psychological approach, and why it works}
**Elements:**
1. {specific element}
2. {specific element}
3. {specific element}

## CTA Analysis
{If present in intro — timestamp, strategy, verbatim text. If not present: "No CTA in intro — CTA appears later in video."}

## Motion Graphic Events ({N} total)

### MG 1: {category} ({start}–{end})

**Duration:** {X}s | **Position:** {position} | **Size:** {size}
**Entry:** {animation} | **Exit:** {animation} | **Easing:** {easing or ?}
**Text:** "{verbatim text content or null}"

**Visual Description:** {3-5 sentence detailed description of exactly what appears on screen. Include colors (hex), layout, composition, any gradients, shadows, or effects. Must be detailed enough for a Remotion developer to recreate.}

**Motion Choreography:**
1. {step with timing, e.g., "Logo scales from 0.8 to 1.0 over 0.3s"}
2. {step with timing}
3. {step with timing}

**Transcript at this moment:** "{exact words spoken}"

**Font Style:** {fontName}, {weight}, {color hex}, {size description}, {shadow if present}

{Repeat for each MG event}

## Transitions ({N} total)

| # | Timestamp | Type | Duration | From → To | SFX |
|---|-----------|------|----------|-----------|-----|
| 1 | {MM:SS.s} | {type} | {Xs} | {description} | {yes/no} |
{...}

## Layout Timeline (1-second granularity)

| Time Range | Layout | Zone Descriptions |
|------------|--------|-------------------|
| 00:00–00:03 | {layout type} | {what's in each zone} |
{...}

## Color Palette
**Color Palette is MANDATORY — do NOT leave empty.** Extract at least 3 background hex codes, 2 text hex codes, and 2 accent hex codes from observed MG elements and slides. If the video uses dark mode UIs, include those background colors.
**Background:** {hex1}, {hex2}, {hex3}, ...
**Text:** {hex1}, {hex2}, ...
**Accent:** {hex1}, {hex2}, ...
**Brand Observations:** {notes on color strategy}

## Recurring Patterns
1. **{Pattern Name}** ({X} occurrences) — {description}. Timestamps: {list}
2. {repeat}
```

**Also output a JSON version** following the `mg-analysis-schema.json` `introAnalysis` section structure. Output the JSON in a fenced code block tagged `json` at the end of the markdown.

---

## System Prompt for Gemini — Pass B (Body Sample Windows)

You are a world-class motion graphics analyst. You are analyzing a 2-minute sample window from the body of a long-form YouTube tutorial. Your task is to document every motion graphic event, transition, and visual change at the same depth as a short-form reel analysis.

**Context for this window:**
- Video: {title} by {creator}
- Window: {start} – {end}
- Section context: {what chapter/topic is being covered}
- This is a body section (post-intro) — expect primarily screen share with occasional MG overlays, speaker returns, chapter cards, and digital zoom events

**Critical rules:**
- Same precision standards as Pass A: sub-second timestamps, numbered choreography, transcript correlation, font details
- **MANDATORY FIELDS — every body MG event must have:**
  - `category`: Use the exact same taxonomy as Pass A (text-overlay, logo-animation, UI-mockup, concept-graphic, sequential-bullets, stylized-b-roll, digital-pan-zoom, floating-card, shape-animation, comparison-layout, diagram, counter-number, screen-share-annotation)
  - `entryAnimation`: One of: cut-in, fade-in, pop-in, scale-up, zoom-in, slide-in-left, slide-in-right, slide-in-top, slide-in-bottom, typewriter, wipe-reveal, spring
  - `exitAnimation`: One of: cut-out, fade-out, hold-then-cut, scale-down, slide-out, zoom-out
  - `visualDescription`: 2-3 sentences minimum
  - Do NOT leave any of these fields as null — if uncertain, give your best classification with a qualifier
- Document ALL visual events including:
  - MG overlays on screen share (text callouts, annotations, zoom effects)
  - PiP state changes (speaker overlay appearing/disappearing)
  - Chapter/section cards
  - Digital zoom events with parameters (factor, direction, easing, duration)
  - Speaker return segments (when speaker comes back to camera)
- Measure spacing between consecutive MG events — this is critical data
- Note what is being shown in the screen share (IDE, browser, terminal, etc.)

### Output Structure — Pass B (per window)

```markdown
## Body Sample Window: {start} – {end}

### Context
- **Section:** {chapter/topic name}
- **Primary Layout:** {screen-share-with-pip / full-frame-screen-share / full-frame-speaker / etc.}
- **PiP State:** {on / off / mixed}

### Pacing Metrics
- **MG Events:** {count} | **Transitions:** {count}
- **MG Spacing:** min {X}s, max {X}s, avg {X}s
- **Cuts/min:** {X}
- **Zoom Events:** {count}

### Motion Graphic Events ({N} total)

{Same format as Pass A — each event with full detail}

### Transitions

| # | Timestamp | Type | Duration | Description | SFX |
|---|-----------|------|----------|-------------|-----|
{...}

### Zoom Events

| # | Timestamp | Factor | Direction | Duration | Easing |
|---|-----------|--------|-----------|----------|--------|
{...}

### Layout Timeline

| Time Range | Layout | Notes |
|------------|--------|-------|
{...}

### MG Spacing Log
{List gap in seconds between each consecutive MG event}
```

When all windows for a video are complete, output a **Body MG Patterns Summary** section:

```markdown
## Body MG Patterns Summary

### MG Type Distribution
| Category | Count | Avg Duration |
|----------|-------|-------------|
{...}

### Spacing Statistics
- **Overall:** min {X}s, max {X}s, avg {X}s between MG events
- **By Layout:** screen-share: avg {X}s, speaker-return: avg {X}s

### Transition Type Frequency
| Type | Count |
|------|-------|
{...}

### PiP Toggle Pattern
{Description of when PiP turns on/off}

### Speaker Return Cadence
- Min: {X}s | Max: {X}s | Avg: {X}s between speaker returns

### Zoom Patterns
- Frequency: {X} zooms per minute of screen share
- Typical factor: {X}
- Common easing: {type}
```

**Also output JSON** for each window following the `mg-analysis-schema.json` `bodyAnalysis.bodySampleWindows[]` structure, plus the aggregated `bodyMGPatterns` object.

---

## System Prompt for Gemini — Pass C (MG Density)

You are analyzing the full structure of a long-form YouTube tutorial at low frame rate (0.1 fps = 1 frame per 10 seconds). Your task is to map the video's chapter structure and estimate motion graphic density per chapter.

**You are NOT analyzing individual MG events** — that was done in Passes A and B. Instead you are:
1. Identifying every chapter/section boundary with exact timestamp
2. Counting approximate MG events visible per chapter
3. Identifying MG-sparse zones (>30 seconds without any visual change beyond screen share content)
4. Documenting the chapter transition style at each boundary
5. Locating any CTA moments (mid-roll and end)

### Output Structure — Pass C

```markdown
# MG Density Analysis: {video title}

## Chapter Map

| # | Chapter Name | Start | End | Duration | Approx MG Count | Avg Inter-MG Spacing | Transition Style |
|---|-------------|-------|-----|----------|-----------------|---------------------|-----------------|
| 1 | {name} | {MM:SS} | {MM:SS} | {Xm Ys} | {count} | {Xs} | {style} |
{...}

## Section Transitions

### Transition at {MM:SS}: {from} → {to}
- **Style:** {black title card / speaker return + verbal bridge / direct cut / etc.}
- **Card Design:** {if applicable: bg color, text color, font, duration}
- **Audio:** {music change, pause, continuous}

{Repeat for each transition}

## MG-Sparse Zones (>30s without visual change)

| Start | End | Duration | Context |
|-------|-----|----------|---------|
| {MM:SS} | {MM:SS} | {Xs} | {what's happening — deep screen share tutorial, etc.} |
{...}

## CTA Moments

### Mid-Roll CTAs
{Timestamp, type, text — or "None detected"}

### End CTA
{Timestamp, type, text, visual description — or "None detected"}

## Summary Statistics
- **Total Chapters:** {N}
- **Avg Chapter Duration:** {X min}
- **Total MG-Sparse Zones:** {N} (total {X min})
- **Estimated Total Body MG Events:** {count}
- **Overall Body MG Density:** ~{X} MGs/minute
```

**Also output JSON** following the `mg-analysis-schema.json` `bodyAnalysis.sectionTransitions[]`, `bodyAnalysis.ctaAnalysis`, and `bodyAnalysis.mgDensityByChapter[]` structures.

---

## API Configuration

### Model: Gemini 3.1 Pro Preview

Using `gemini-3.1-pro-preview` — same model as production analysis passes.

> **Note:** `gemini-3-pro-preview` was deprecated March 9, 2026. Always use `gemini-3.1-pro-preview`.

### Three-Pass Configuration

| Pass | Segment | FPS | Thinking Budget | Media Resolution | Output File |
|------|---------|-----|-----------------|------------------|-------------|
| A (Intro MG) | First 90s | 1.0 | 8192 | HIGH | `mg-analysis-intro.md` |
| B (Body Samples) | 2-min windows | 0.5 | 8192 | HIGH | `mg-analysis-body-samples.md` |
| C (MG Density) | Full video | 0.1 | 4096 | MEDIUM | Enhances `full-analysis.md` |

### Token Budget Estimate

| Pass | Frames | Frame tokens (258/frame) | Audio tokens (32/s) | Total estimate |
|------|--------|--------------------------|---------------------|----------------|
| A (90s @ 1fps) | 90 | ~23,220 | ~2,880 | ~26,100 |
| B (per 2-min window @ 0.5fps) | 60 | ~15,480 | ~3,840 | ~19,320 |
| C (varies by length @ 0.1fps) | varies | varies | varies | varies |

Plus prompt text (~4,000 tokens). All well within the 1M context window.

Body sample windows are sent as **separate API calls** (one per window) to keep context focused and prevent cross-contamination between windows.

### Python Implementation

```python
from google import genai
from google.genai import types

client = genai.Client(api_key=GEMINI_API_KEY)

# Pass A: Intro MG (first 90s, 1fps)
intro_part = types.Part(
    inline_data=types.Blob(data=intro_bytes, mime_type="video/mp4"),
    video_metadata=types.VideoMetadata(fps=1.0)
)

response_a = client.models.generate_content(
    model="gemini-3.1-pro-preview",
    contents=[intro_part, pass_a_prompt],
    config=types.GenerateContentConfig(
        temperature=0.3,
        thinking_config=types.ThinkingConfig(thinking_budget=8192),
        media_resolution=types.MediaResolution.MEDIA_RESOLUTION_HIGH,
    )
)

# Pass B: Body sample window (2-min clip, 0.5fps)
window_part = types.Part(
    inline_data=types.Blob(data=window_bytes, mime_type="video/mp4"),
    video_metadata=types.VideoMetadata(fps=0.5)
)

response_b = client.models.generate_content(
    model="gemini-3.1-pro-preview",
    contents=[window_part, pass_b_prompt],
    config=types.GenerateContentConfig(
        temperature=0.3,
        thinking_config=types.ThinkingConfig(thinking_budget=8192),
        media_resolution=types.MediaResolution.MEDIA_RESOLUTION_HIGH,
    )
)

# Pass C: MG Density (full video, 0.1fps)
full_part = types.Part(
    inline_data=types.Blob(data=full_bytes, mime_type="video/mp4"),
    video_metadata=types.VideoMetadata(fps=0.1)
)

response_c = client.models.generate_content(
    model="gemini-3.1-pro-preview",
    contents=[full_part, pass_c_prompt],
    config=types.GenerateContentConfig(
        temperature=0.3,
        thinking_config=types.ThinkingConfig(thinking_budget=4096),
        media_resolution=types.MediaResolution.MEDIA_RESOLUTION_MEDIUM,
    )
)
```

### Batch Execution

```python
for video in videos:
    # Pass A: Intro MG
    run_mg_pass(video["id"], pass_type="mg-intro")
    time.sleep(30)

    # Pass B: Body sample windows (one API call per window)
    for window in video["sampleWindows"]:
        run_mg_pass(video["id"], pass_type="mg-body", window=window)
        time.sleep(30)

    # Pass C: MG density
    run_mg_pass(video["id"], pass_type="mg-density")
    time.sleep(30)

    # Merge all passes
    merge_mg_analysis(video["id"])
```

---

## Output Files

Each video produces these MG analysis files (alongside existing production analysis):

```
{folder}/
├── mg-analysis-intro.md          (Pass A — intro MG events at short-form depth)
├── mg-analysis-body-samples.md   (Pass B — body sample window MG events)
├── mg-analysis.md                (Merged — unified per-video MG analysis)
├── mg-analysis.json              (Structured JSON — unified)
├── intro-analysis.md             (existing — production/layout detail)
├── full-analysis.md              (existing — enhanced by Pass C density data)
├── production-analysis.md        (existing — merged production analysis)
└── transcript.json               (existing — word-level transcript)
```
