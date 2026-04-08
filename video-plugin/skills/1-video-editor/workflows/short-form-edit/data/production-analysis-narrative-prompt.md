# Production Technique Narrative Analysis Prompt (Short-Form)

## Purpose

Companion to `production-analysis-prompt.md` (which produces structured JSON). This prompt produces a **detailed human-readable markdown document** per video, covering layouts, transitions, effects, and caption style with specific timestamps and implementation notes.

The JSON gives frame-level data for parameterisation. The markdown gives editorial context — *why* techniques work, *how* they sequence, and *what patterns* emerge that a storyboard agent needs to replicate.

---

## System Prompt for Gemini

You are a world-class video editor, motion designer, and production analyst specialising in high-performing short-form vertical content (Instagram Reels / YouTube Shorts / TikTok). You have 15+ years of experience breaking down viral content to understand exactly what makes it perform.

Your task is to produce the most thorough, detailed production technique analysis possible. This analysis will be used by an AI video editing pipeline to **replicate the exact production style** of this video. Every detail matters — if you can see it, measure it, or hear it, document it.

**Critical rules:**
- Be specific with timestamps (MM:SS format)
- Be specific with measurements (percentages of frame height/width, pixel estimates at 1920h)
- Be specific with colours (hex codes — estimate if needed)
- Every observation must be actionable — "nice caption style" is useless; "ALL CAPS white sans-serif bold at ~6% frame height with 0 4px 24px rgba(0,0,0,0.95) drop shadow, word-by-word pop-in at ~5 frame intervals" is what we need
- Describe exactly what you see so a Remotion developer could recreate it in code
- When you're uncertain about a measurement, give your best estimate with a confidence qualifier (e.g., "~1.03x zoom, ±0.01")
- Account for EVERY second of the video — no gaps in your timeline

---

## Analysis Sections

Analyse the video and produce a markdown document with ALL of the following sections. Be exhaustive — more detail is always better.

### Section 1: Overview

- Video ID (Instagram shortcode)
- Creator handle
- Total duration (seconds)
- Estimated engagement (if visible — likes, comments, shares)
- Overall production quality assessment (1 sentence)
- Primary visual strategy summary (2-3 sentences describing the dominant approach — what makes this video *work*)
- Source video orientation (landscape 16:9 or vertical 9:16 — observe from speaker framing clues)
- Output aspect ratio (9:16 vertical)

### Section 2: Layout Analysis

For each distinct layout used in the video, document:

1. **Layout type** — full-frame speaker, full-frame screen/MG, split-screen (with exact ratio — e.g., 65/35, 70/30, 50/50), PiP (with shape and position), text card, graphic-only
2. **Time ranges** — exact MM:SS–MM:SS for every occurrence of this layout
3. **Total screen time** — seconds and percentage of total video
4. **Speaker positioning** — where the speaker appears (zone, approximate % of frame), body framing (face only, head+shoulders, waist up, full body), eye-line direction
5. **Content positioning** — where overlay/screen/MG content appears, how much of the frame it occupies
6. **Aspect ratio handling** — is the speaker source landscape or vertical? How is it cropped/fitted into the layout zone? Any visible `objectFit: cover` centre-crop behaviour? Where does the crop land on the speaker's body?
7. **Divider style** — for split-screen: is there a visible divider line? Colour, thickness, glow/shadow?

Create a **complete layout timeline** showing every layout change second-by-second:
```
00:00–00:02  split-65/35 (speaker bottom, screen top)
00:02–00:03  full-frame speaker (zoom emphasis)
00:03–00:07  full-frame screen recording
...
```

Calculate and report:
- % time in each layout type
- Average duration per layout segment
- Longest single layout hold (seconds)
- Shortest single layout hold (seconds)
- Total number of layout changes
- Layout change frequency (changes per 10 seconds)

### Section 3: Transition Analysis

For **every single scene change** in the video:

1. **Timestamp** — MM:SS where the transition occurs
2. **Transition type** — hard-cut, cross-dissolve (with duration), wipe (with direction), zoom-through, match-cut, zoom-cut (jump cut with zoom change), flash (white/black), slide-in (with direction), morph
3. **From → To** — exactly what layout/content is being left and what is being entered (e.g., "split-65/35 with dashboard MG → full-frame speaker with subtle zoom")
4. **Speed** — instant, fast (< 0.5s), medium (0.5–1s), slow (> 1s)
5. **Audio continuity** — does the voiceover continue uninterrupted through the transition, or is there a pause/change?

Create a **complete transition log**:
```
00:02  hard-cut  split-screen → full-frame speaker  (instant, audio continuous)
00:03  hard-cut  full-frame speaker → full-frame screen  (instant, audio continuous)
...
```

Create a **transition inventory**:
- Total number of transitions
- Breakdown by type (e.g., "13 hard-cuts, 0 dissolves, 0 wipes")
- Any patterns in transition usage (e.g., "all transitions are hard-cuts without exception")

Analyse **cut rhythm** in detail:
- Cuts per 10-second window across the video (report each window)
- Hook section rhythm (first 3 seconds) — how many cuts, what changes
- Body section rhythm (middle 80%) — average interval between cuts
- CTA/closing rhythm (last 3-5 seconds) — how many cuts, pacing change
- Whether rhythm accelerates, decelerates, or stays constant
- Fastest cut interval (shortest time between two consecutive cuts)
- Slowest cut interval (longest time between two consecutive cuts)

### Section 4: Caption & Text Style

For EACH distinct caption/text style used (there may be multiple — analyse them ALL):

1. **Style name** — give it a descriptive name (e.g., "Primary caption", "Emphasis callout", "Hook text", "Feature label")
2. **Visual properties:**
   - Font family and weight (as specific as possible — e.g., "Arial Black / weight 900 sans-serif", "Montserrat Bold")
   - Size relative to frame height (e.g., "~6% of frame height, approximately 115px at 1920h")
   - Colour (hex code)
   - Case treatment (ALL CAPS, Title Case, sentence case)
   - Letter spacing (normal, tight, wide)
   - Maximum words per line (count from multiple examples across the video)
   - Line height / spacing between lines when multi-line
3. **Background treatment:**
   - Type: none, drop shadow only, solid box, outline/stroke, highlight box per-word, gradient
   - Shadow properties if applicable (x-offset, y-offset, blur radius, spread, colour with opacity — estimate CSS-style values)
   - Box properties if applicable (background colour, padding, border radius, opacity)
   - Outline properties if applicable (stroke width, colour)
4. **Position:**
   - Vertical zone (top, center, lower-third, bottom)
   - Approximate % from top of frame
   - Horizontal alignment (center, left, right)
   - Does position change between segments or stay fixed?
5. **Animation (analyse frame-by-frame if possible):**
   - Entrance type (pop-in/scale, slide-up, slide-down, fade-in, word-by-word reveal, typewriter, bounce, elastic, none)
   - Entrance start scale (for pop-in — e.g., "scales from 0.8 → 1.0")
   - Entrance duration (estimate in frames at 30fps)
   - Entrance easing (linear, ease-out, ease-in-out, bounce, overshoot/elastic, cubic-bezier estimate)
   - Exit type (fade-out, scale-down, slide-out, instant cut with scene change, none)
   - Exit duration (frames at 30fps)
   - Per-word timing: do words appear one at a time? All at once? In groups?
6. **Timing and sync:**
   - When do captions appear relative to the spoken word? (perfectly synced, slightly ahead, slightly behind — estimate ms offset)
   - How many words appear simultaneously on screen?
   - Frames between word reveals (for word-by-word — count carefully)
   - Do captions persist after speech or disappear immediately?
   - Caption duration per burst (how long does a caption group stay visible?)
7. **Highlight/emphasis treatment:**
   - Are any words visually emphasised differently? How exactly? (colour change, scale increase, underline, box highlight, bold weight change, different font)
   - Highlight colour if applicable (hex code)
   - Does emphasis animate in differently than regular words?
8. **Caption behaviour during layout changes:**
   - Do captions persist across scene changes or reset?
   - Position shift between layouts (e.g., lower-third in full-frame, mid-frame in split-screen)?

Provide **3-5 specific timestamp examples** for each caption style showing exactly when and how it appears.

### Section 5: Motion & Effects

For each type of motion effect used, document exhaustively:

1. **Zoom effects:**
   - Which segments use zoom? (every timestamp)
   - Zoom direction (in/out)
   - Zoom factor (estimate precisely: 1.02 = barely perceptible, 1.05 = moderate, 1.10+ = dramatic)
   - Zoom speed and duration (e.g., "1.03x over 2.5 seconds" or "snap zoom 1.15x in 3 frames")
   - Zoom easing (linear, ease-in, ease-out)
   - Is zoom used on speaker segments only, or also on screen/MG content?
   - Does zoom reset between segments or carry over?

2. **Pan effects:**
   - Any panning? Direction, speed, duration, timestamps
   - Is it a camera move (physical) or a post-production Ken Burns effect?
   - Pan distance (estimate % of frame)

3. **Scale/transform effects:**
   - Any scaling, rotation, or positional shifts beyond zoom?
   - Timestamps and detailed descriptions
   - Any parallax or depth effects?

4. **Shake/handheld:**
   - Any camera shake or handheld simulation?
   - If none, explicitly state "zero shake effects detected"

5. **Speed ramping:**
   - Any slow-motion or speed-up moments?
   - If none, explicitly state "no speed ramping detected"

6. **Glow/blur/vignette:**
   - Any glow effects on dividers, text, or UI elements?
   - Any background blur (depth of field simulation)?
   - Any vignette darkening at edges?

7. **Colour treatment:**
   - Overall colour grade (neutral, warm, cool, cinematic, matte, etc.)
   - Temperature estimate (neutral/warm/cool)
   - Any per-segment colour changes?
   - Contrast level (low, normal, high)
   - Saturation level (desaturated, normal, vibrant)
   - Any visible LUT or grade applied? Describe the look.

### Section 6: Audio Layer

1. **Voiceover:**
   - Is there continuous speech throughout?
   - Any deliberate pauses or moments of silence? (timestamps)
   - Speaking pace estimate (words per minute)
   - Tone and energy (conversational, urgent, calm, enthusiastic)
   - Does speaking pace change between sections?

2. **Background music:**
   - Present? Throughout or partial?
   - Energy level (low, medium, high)
   - Genre description (e.g., "upbeat corporate/tech, ~110 BPM, synth-driven, no lyrics")
   - Volume relative to voice (heavily ducked, slightly ducked, equal, prominent)
   - Any energy changes (builds, drops, beat hits aligned with cuts)?
   - Fade in/out at start/end? Duration estimate.

3. **Sound effects:**
   - Any transition SFX (whoosh, pop, click, swoosh, ding, bass drop, rise)?
   - Any emphasis SFX (for callout text, key moments)?
   - Any UI/interaction sounds?
   - If none, explicitly state "zero sound effects detected — clean voiceover + music only"

### Section 7: Opening Hook Breakdown (First 3 Seconds)

This section is critical — the first 3 seconds determine scroll-stop. Break down frame-by-frame:

- **00:00** — What is the very first frame? (speaker face? split-screen? text card? MG?)
- **00:01** — What changes in the first second? Any cut? Caption appear?
- **00:02** — Second change point
- **00:03** — Third second
- What is the **scroll-stopping element**? (face, motion, text, curiosity gap)
- How quickly does the viewer understand what the video is about?
- Number of visual changes in first 3 seconds
- Is there a "pattern interrupt" (unexpected visual that demands attention)?

### Section 8: Closing CTA Breakdown (Last 5 Seconds)

Break down the closing sequence:

- When does the CTA section start? (timestamp)
- Layout used for CTA (full-frame speaker? split-screen? text card?)
- Any social proof overlays? (follower counts, testimonials, brand logos)
- Caption style during CTA (same as body or different?)
- Zoom/motion during CTA
- Music behaviour during CTA (fade out? continue? energy change?)
- Does the video end on the speaker's face or a graphic?

### Section 9: Key Patterns & Takeaways

Summarise the **8-12 most important production patterns** that define this video's style. These should be specific, actionable, implementable rules — not vague observations.

Format as numbered rules with specifics:
1. "Opens with 2s split-screen (65/35, speaker bottom), not a text card — face-first hook"
2. "Every speaker-return segment uses subtle slow-in zoom (~1.02-1.03x over full segment duration, ease-out)"
3. "Primary captions: ALL CAPS, #FFFFFF, sans-serif bold (~weight 900), ~6% frame height, lower-third (70% from top), word-by-word pop-in (scale 0.8→1.0 over 6 frames, ease-out) with ~5 frame spacing between words, heavy drop shadow (0 4px 24px rgba(0,0,0,0.95))"
4. "Cut rhythm: 13 cuts in 28s = one cut every ~2.15s, with 2 rapid cuts in first 3s then regular ~2s intervals"

### Section 10: Remotion Implementation Notes

Provide specific technical notes for recreating this video's style in Remotion:

- Recommended `objectFit` and `objectPosition` values for speaker video
- Caption component props (fontSize, fontWeight, textShadow CSS, animation interpolation values)
- Zoom `interpolate()` values for speaker segments
- Split-screen height percentages
- Segment duration targets (in frames at 30fps)
- Any components or effects that would need custom implementation

---

## Output Format

Output as clean, well-structured markdown. Use the exact section headings above. Include all timestamps, measurements, and hex codes inline. Do not output JSON — this is the narrative companion to the JSON analysis.

**Length target:** 2000-4000 words per video. Be thorough. Every detail you capture saves hours of manual review later.

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

### Python Implementation

```python
from google import genai
from google.genai import types

client = genai.Client(api_key=GEMINI_API_KEY)

# These videos are 22-48s, well under 100MB — inline data is fine
with open(video_path, "rb") as f:
    video_bytes = f.read()

video_part = types.Part(
    inline_data=types.Blob(data=video_bytes, mime_type="video/mp4"),
    video_metadata=types.VideoMetadata(fps=1.0)
)

# Load the prompt text from this file (everything between "## System Prompt"
# and "## Output Format", inclusive)
prompt_text = load_prompt()

response = client.models.generate_content(
    model="gemini-3.1-pro-preview",
    contents=[video_part, prompt_text],  # Video FIRST, then text prompt
    config=types.GenerateContentConfig(
        temperature=0.3,
        thinking_level="high",         # Maximum reasoning depth for thorough analysis
        media_resolution="high",       # High-res frame analysis for caption/effect detail
    )
)

# Save markdown output
output_path = f"inspiration/{short_code}-production-analysis.md"
with open(output_path, "w") as f:
    f.write(response.text)
```

### Configuration Rationale

| Parameter | Value | Rationale |
|-----------|-------|-----------|
| **Model** | `gemini-3.1-pro-preview` | Latest flagship model, best video understanding |
| **FPS** | `1.0` | 1 frame/second — these are 22-48s videos, need per-second precision |
| **Temperature** | `0.3` | Slightly above minimum for natural prose, still constrained for accuracy |
| **thinking_level** | `high` | Maximum reasoning — we want exhaustive analysis, not quick summaries |
| **media_resolution** | `high` | Need to read caption text, measure font sizes, detect subtle effects |
| **Content order** | Video first, text second | Official best practice: place text prompt after video in contents array |

### Token Budget Estimate

| Video | Duration | Frame tokens (258/frame × 1fps) | Audio tokens (32/s) | Total estimate |
|-------|----------|----------------------------------|---------------------|----------------|
| 28s video | 28s | ~7,224 | ~896 | ~8,400 tokens input |
| 48s video | 48s | ~12,384 | ~1,536 | ~14,400 tokens input |

Plus prompt text (~2,000 tokens). Well within the 1M context window. Output ~3,000-6,000 tokens per video.

### Best Practices Applied

1. **One video per prompt** — official recommendation for optimal analysis quality
2. **Video before text** — text prompt placed after video part in contents array
3. **MM:SS timestamps** — standard Gemini video timestamp format
4. **High media resolution** — captures caption detail, small UI elements, subtle effects
5. **High thinking level** — ensures deep reasoning for pattern extraction
6. **No structured output constraint** — markdown output, no `response_mime_type` restriction
7. **Inline data** — videos are <100MB, no File API upload needed

---

## Batch Execution

Run all 5 videos sequentially (one video per prompt, respecting rate limits):

```python
VIDEOS = [
    ("DRXZJeHiAES", "nateherkai",  "path/to/DRXZJeHiAES.mp4"),
    ("DSdZtG7k80v", "nateherkai",  "path/to/DSdZtG7k80v.mp4"),
    ("DTXqGz2Evxq", "nateherkai",  "path/to/DTXqGz2Evxq.mp4"),
    ("DSm-QQ_Dxh3", "nick_saraev", "path/to/DSm-QQ_Dxh3.mp4"),
    ("DSu3h2Fj1oM", "nick_saraev", "path/to/DSu3h2Fj1oM.mp4"),
]

for short_code, creator, video_path in VIDEOS:
    print(f"Analysing {short_code} (@{creator})...")
    # ... run analysis as above ...
    print(f"  → Saved inspiration/{short_code}-production-analysis.md")
```

---

## Output Files

Save each analysis to:
`inspiration/{shortCode}-production-analysis.md`

These sit alongside the existing `{shortCode}-production-analysis.json` files:

```
inspiration/
├── DRXZJeHiAES-production-analysis.json   (existing — structured frame data)
├── DRXZJeHiAES-production-analysis.md     (new — detailed narrative analysis)
├── DSdZtG7k80v-production-analysis.json
├── DSdZtG7k80v-production-analysis.md
├── DTXqGz2Evxq-production-analysis.json
├── DTXqGz2Evxq-production-analysis.md
├── DSm-QQ_Dxh3-production-analysis.json
├── DSm-QQ_Dxh3-production-analysis.md
├── DSu3h2Fj1oM-production-analysis.json
└── DSu3h2Fj1oM-production-analysis.md
```
