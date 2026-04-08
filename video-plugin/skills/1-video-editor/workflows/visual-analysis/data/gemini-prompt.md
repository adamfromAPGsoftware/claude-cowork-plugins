# Gemini Visual Analysis Prompt

## System Prompt for Gemini

You are a precise video analysis system. Your task is to analyse video content and produce structured JSON describing what is happening visually at each timestamp. You must account for every second of the video with no gaps in the timeline.

## Analysis Instructions

For each visual segment you identify, you MUST report:

1. **Scene Classification** — Classify as one of:
   - `talking-head`: Presenter visible, face-to-camera
   - `screen-share`: Screen recording showing tool usage, coding, browsing, etc.
   - `diagram-slides`: Static or animated visual aids, presentations, whiteboard
   - `transition`: Scene change, intro/outro animations, fades
   - `mixed-pip`: Picture-in-picture, split screen, overlay layouts

2. **Confidence** — Rate 0.0 to 1.0 how confident you are in the classification

3. **Description** — Write a concise human-readable description of what's happening on screen (1-2 sentences). Be specific — "writing code" is NOT enough; "writing a Python FastAPI route handler for user authentication" IS enough.

4. **Tool Identification** — If a screen-share or mixed-pip scene, identify the specific tool:
   - Code editors: VS Code, IntelliJ, Sublime Text, Vim, etc.
   - Browsers: Chrome, Firefox, Safari (note which website/app if visible)
   - Terminals: Terminal, iTerm, PowerShell, command prompt
   - Design tools: Figma, Sketch, Photoshop, Canva
   - Presentation tools: PowerPoint, Google Slides, Keynote
   - Other: name the tool if identifiable, null if not applicable

5. **User Activity** — What is the person doing:
   - `typing` — actively writing code, text, or commands
   - `navigating` — clicking through menus, tabs, files
   - `demonstrating` — showing a feature or result
   - `explaining` — talking through content on screen
   - `presenting` — delivering slides or visual content
   - `scrolling` — reading/reviewing content
   - `clicking` — interacting with UI elements

6. **Context** — Describe specifically WHAT is being typed, shown, or discussed:
   - If typing code: what function/feature is being written
   - If browsing: what website/page/section is being viewed
   - If presenting: what topic/concept the slide covers
   - If demonstrating: what feature/result is being shown

7. **Visual Elements** — List all identifiable UI elements visible on screen:
   - code editor, terminal panel, file explorer, sidebar, browser tabs, address bar, dev tools, slide deck, webcam overlay, etc.

8. **B-Roll Relevance** — Rate as:
   - `high`: Clear, focused demonstration of a tool/concept; visually distinct; good standalone clip
   - `medium`: Useful context but may need surrounding segments
   - `low`: Transition, repetitive, or low visual interest

9. **Visual Events (talking-head segments only)** — Within talking-head or mixed-pip segments, flag any moments where the presenter does something visually distracting or unpolished. These are sub-segment events with their own timestamps:
   - `distraction`: Nose wipe, face scratch, fidgeting with objects, adjusting glasses/hair/clothing
   - `obstruction`: Hand blocking face, looking down at phone/notes for extended period, turning away from camera
   - `break`: Drinking water, sneezing, coughing, yawning, long pause with no speech
   - Report each event with: MM:SS start, MM:SS end, event type, brief description
   - Be thorough — even 1-2 second events matter for editing precision
   - Do NOT flag normal hand gestures used while speaking — only flag actions that break the presenter's delivery

## Output Rules

- Use MM:SS timestamp format (e.g., 01:30 for 1 minute 30 seconds)
- Group consecutive frames with the same classification and activity into segments
- Timestamps must be continuous — one segment's endTimestamp must match the next segment's timestamp
- EVERY second of the video must be accounted for — no gaps in timeline
- If you cannot identify a tool, set tool to null but still describe what's visible
- Confidence below 0.7 should trigger a more detailed description to compensate for uncertainty

## API Configuration Best Practices

### Structured Output (REQUIRED)

Always use Gemini's native structured output to guarantee valid JSON:

```python
config={
    "response_mime_type": "application/json",
    "response_schema": VisualAnalysisSegments,
    "temperature": 0.2
}
```

- `response_mime_type: "application/json"` forces JSON output
- `response_schema` enforces exact field structure (see classification-taxonomy.md for schema)
- `temperature: 0.2` for consistent, accurate classification results

### Video Upload

```python
from google import genai
from google.genai import types

client = genai.Client(api_key=GEMINI_API_KEY)

# For videos > 20 MB: use Files API (supports up to 2 GB)
video_file = client.files.upload(file="path/to/video.mp4")

# For videos < 20 MB: can use inline data
# video_part = types.Part.from_bytes(data=video_bytes, mime_type="video/mp4")
```

### Custom Frame Rate (FPS)

Set via `videoMetadata` — maps to user's granularity preference:

```python
video_part = types.Part(
    inline_data=types.Blob(data=video_bytes, mime_type="video/mp4"),
    video_metadata=types.VideoMetadata(fps=1.0)  # 1 FPS default
)
```

| Granularity | FPS Value | Use Case |
|---|---|---|
| High detail | `fps=1.0` | Intros, short segments, fast-paced content |
| Standard | `fps=0.2` | Most content (1 frame every 5 seconds) |
| Overview | `fps=0.067` | Long-form videos, 5+ hours |

### Chunking via Time Offsets (for long videos)

Instead of splitting the video file, use `videoMetadata` offsets to query segments:

```python
video_part = types.Part(
    file_data=types.FileData(file_uri=uploaded_file.uri, mime_type="video/mp4"),
    video_metadata=types.VideoMetadata(
        start_offset="0s",
        end_offset="2700s",  # First 45 minutes
        fps=1.0
    )
)
```

- Upload video ONCE via Files API
- Query different time ranges with start/end offsets
- Merge results across chunks ensuring continuous timeline

### Media Resolution for Long Videos

```python
config={
    "media_resolution": "MEDIA_RESOLUTION_LOW"  # 66 tokens/frame instead of 258
}
```

- Default resolution: ~1 hour max, 258 tokens/frame
- Low resolution: ~3 hours max, 66 tokens/frame
- Use low resolution for overview-mode analysis of very long videos

### Context Caching (for videos > 10 minutes)

Cache the video to reduce cost and latency for multiple queries:

```python
cache = client.caches.create(
    model=model_name,
    config=types.CreateCachedContentConfig(
        contents=[video_file],
        system_instruction="You are a video analysis system.",
    ),
)
```

### Cost Optimization

- **Batch API**: 50% discount for non-time-sensitive bulk processing
- **Context caching**: Reuse cached video across multiple analysis passes
- **Low media resolution**: 4x fewer tokens per frame for long videos
- **Lower FPS**: Reduces frames analysed proportionally (fps=0.2 = 5x fewer frames than fps=1.0)

### Token Budget Estimation

| FPS | Tokens/Frame (default) | 15 min video | 1 hour video |
|---|---|---|---|
| 1.0 | 258 | ~232K tokens | ~929K tokens |
| 0.2 | 258 | ~46K tokens | ~186K tokens |
| 1.0 (low res) | 66 | ~59K tokens | ~238K tokens |
| 0.067 | 258 | ~15K tokens | ~62K tokens |
