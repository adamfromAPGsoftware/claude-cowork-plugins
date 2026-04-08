---
name: 'step-02-generate'
description: 'Call Hera Video API for each MG clip and download results'

nextStepFile: './step-03-completion.md'
dataFile: '../data/hera-api-reference.md'
---

# Step 2: Generate Motion Graphics via Hera Video API

## STEP GOAL:

Execute Hera Video API calls for each motion graphic brief, monitor generation progress, and download completed `.mp4` files to the resolved output paths.

## MANDATORY EXECUTION RULES (READ FIRST):

### Universal Rules:

- CRITICAL: Read the complete step file before taking any action
- CRITICAL: When loading next step with 'C', ensure entire file is read
- YOU MUST ALWAYS SPEAK OUTPUT in your Agent communication style with the config `{communication_language}`

### Step-Specific Rules:

- MUST confirm with user before executing API calls (each call costs money)
- ⚡ **Batch-submit-then-poll:** Submit ALL API calls first (capturing `video_id` from each response), then poll ALL jobs in a single loop every 10s until all reach `"success"` or `"failed"`. This replaces sequential one-at-a-time processing.
- Report status after each completed generation
- Handle API errors gracefully — offer retry or skip

## MANDATORY SEQUENCE

### 1. Pre-Generation Confirmation

"**Ready to Generate {count} Motion Graphic(s)**

Each API call will generate a video clip via Hera Video. Confirm to proceed?

**[G] Generate All** — Process all {count} briefs sequentially
**[O] One-by-One** — Confirm each brief individually before calling API

Select: [G] Generate All / [O] One-by-One"

Wait for user selection.

### 2. Prepare Reference Images

Before API calls, prepare any required reference images:

**For `image_source: fetch-logo` — Logo Acquisition via Waterfall:**
- When any MG brief references a named tool/brand logo, fetch via `scripts/fetch-logo.ts` (4-tier waterfall: Simple Icons → SVG Logos → Logotypes.dev → Logo.dev)
- Command:
  ```bash
  rm -f "{output_path}"
  npx tsx scripts/fetch-logo.ts --name "{tool}" --output "{output_path}" --color ffffff
  ```
- **Visual verification:** Read the output PNG and confirm it is the correct logo. If wrong (generic icon, wrong brand, placeholder), ask user for a direct URL override or skip.
- Store verified logos in the project logos directory (e.g., `short-form/logos/{slug}.png`)
- Upload/host at a publicly accessible URL for `reference_image_url`

**For `image_source: branded-assets`:**
- Copy from `{project-root}/_bmad/_memory/video-editor-sidecar/branded-assets/`
- Upload/host at a publicly accessible URL

**For `image_source: frame-extract` (including auto-extract from body footage):**
- If the MG brief includes `reference_frame_timestamp` (set during storyboard production brief):
  - Extract frame from body/main video: `ffmpeg -ss {reference_frame_timestamp} -i "{main_source_video}" -frames:v 1 "{output_dir}/{mg_id}-reference.png"`
- Otherwise extract from specified source: `ffmpeg -ss {timestamp} -i "{source}" -frames:v 1 "{output}.png"`
- **Auto-extract is the default for all Type B and Type C MGs** where the tool is visible in body footage. The storyboard step identifies these timestamps automatically.
- Upload/host at a publicly accessible URL

**For `image_source: web-screenshot` — Tool Interface Screenshot:**
- Use the unified resolver which handles the full waterfall + upload:
  ```bash
  npx tsx scripts/resolve-reference-image.ts \
    --tool "{tool_name}" \
    --project-slug "{project-slug}" \
    --visual-analysis "{project_folder}/{project-slug}/video-editor/analysis/body/visual-analysis.json" \
    --source-video "{main_source_video}" \
    --output "{output_dir}/{mg_id}-reference.png"
  ```
- The script automatically:
  1. Checks body footage for frame extraction opportunities
  2. Falls back to web screenshot capture
  3. Falls back to logo
  4. Uploads to Supabase Storage → returns persistent public URL
- **Visual verification:** Read the output PNG and confirm it shows the correct tool interface
- Use the returned public URL as `reference_image_url`
- The `.meta.json` sidecar records which tier was used

**For `image_source: canvas-build`:**
- Extract individual images — use logos fetched via `fetch-logo.ts` (not assumed to exist; fetch first if not already in logos dir)
- Build composite canvas at appropriate resolution (1920x1080 for 16:9)
- Use FFmpeg or ImageMagick to composite elements
- Upload/host at a publicly accessible URL

**For `image_source: none`:**
- No image preparation needed

Report prep status:
"**Reference Image Preparation:**
| # | ID | Image Source | Tier Used | Reference URL | Status |
|---|-----|-------------|-----------|---------------|--------|
| 1 | {mg-id} | {source} | {frame-extract/web-screenshot/logo/n/a} | {url or —} | {ready/built/extracted/fetched/verified/not-needed} |
..."

### 2b. Motion Graphic Brief Templates by Type (Long-Form)

When generating motion graphics for long-form content, use these brief templates based on the MG type from the storyboard.

**Tool Visual Reference:** For any MG that references a named tool/platform, load `{project-root}/video-plugin/skills/1-video-editor/workflows/hera-motion-graphics/data/tool-visual-reference.md` and inject the tool's specific colors, UI layout, and key visual elements into the prompt. This transforms generic MGs into recognizable tool-specific graphics.

**Type A — Text/Number Overlay:**
- Prompt pattern: "Bold white text '[NUMBER/METRIC]' appearing with pop-in animation, centered on dark background (#0B1320), subtle drop shadow, hold 2-4 seconds"
- Duration: 3–4s | Reference image: none
- Example: "Bold white text '$1M+ REVENUE' popping in with scale animation on dark background"

**Type B — Logo Graphic:**
- Prompt pattern: "Logo of [TOOL] sliding in from right side, clean presentation on dark background (#0B1320), [TOOL_PRIMARY_COLOR] glow effect radiating from logo, professional motion design"
- Duration: 4–5s | Reference image: tool logo (fetched via `fetch-logo.ts`)
- When the MG brief includes `tool_name` and `tool_visual_details`, replace the generic glow with the tool's primary color:
  - Claude/Anthropic: `#D97757` terracotta glow
  - ChatGPT/OpenAI: `#10A37F` green glow
  - n8n: `#FF6D5A` coral-orange glow
  - Cursor: `#7B61FF` purple glow
  - (Look up other tools in `tool-visual-reference.md`)
- Example: "Claude Code logo sliding in from right on dark background (#0B1320), warm terracotta (#D97757) glow radiating from logo, professional motion design"
- Fallback (tool not in registry): use generic subtle white glow

**Type C — UI Mockup:**
- Prompt pattern: "Recreated [PLATFORM] interface showing [CONTENT]. [TOOL_VISUAL_DETAILS]. Realistic UI with typing/scroll animations, authentic color scheme and layout"
- Duration: 5–8s | Reference image: **STRONGLY RECOMMENDED** — use `frame-extract` from body footage or `canvas-build` composite. Providing a reference image dramatically improves accuracy of UI recreation.
- When the MG brief includes `tool_visual_details`, inject the full visual identity into the prompt:
  - Include the tool's exact hex colors (e.g., sidebar: `#202123`, chat area: `#343541`)
  - Describe the UI layout spatially (e.g., "dark sidebar on left with conversation list, main chat panel center")
  - Name key visual elements (e.g., "green OpenAI dot logo top-left, model selector dropdown, centered input bar at bottom")
- Tool-specific examples:
  - Claude: "Recreated Claude chat interface — left sidebar (#1A1A2E) with conversation list, main chat area (#F5F0E8 warm cream), terracotta (#D97757) Claude sparkle icon, user message in dark bubble asking about scheduling, Claude response appearing with typing animation"
  - n8n: "Recreated n8n workflow canvas — dark background (#1A1A1A), white node cards connected by lines, orange-red (#FF6D5A) n8n logo top-left, HTTP Request node connected to AI Agent node, execution status showing green checkmarks"
  - ChatGPT: "Recreated ChatGPT interface — dark sidebar (#202123) with conversation history, main chat area (#343541), green OpenAI dot, GPT-4 model selector, user asking about code review"
- Fallback (tool not in registry): use generic "modern dark-themed interface" prompt

**Type D — Concept Graphic:**
- Prompt pattern: "Minimalist diagram showing [CONCEPT], [TOOL_VISUAL_STYLE] design language, animated line-drawing effect, dark background with [ACCENT_COLOR] accents"
- Duration: 5–15s | Reference image: none or sketch reference
- When the MG brief references a named tool, style the diagram using that tool's visual language:
  - n8n concepts: use node-card shapes with connection lines (n8n's canvas style), coral-orange (#FF6D5A) accents
  - Claude/AI chat concepts: use chat bubble shapes, conversation flow arrows, terracotta (#D97757) accents
  - Zapier concepts: use vertical step cards with trigger→action arrows, orange (#FF4F00) accents
  - GitHub concepts: use repository/PR card shapes, green (#2EA44F) accents
  - (Look up other tools in `tool-visual-reference.md`)
- Example: "n8n-style workflow diagram — white node cards on dark background (#1A1A1A), coral-orange (#FF6D5A) connection lines, nodes labeled 'Webhook', 'AI Agent', 'Slack', animated line-drawing effect revealing connections sequentially"
- Fallback (no specific tool): use generic blue (#4A90E2) accents with clean box-and-line style

**Type E — Sequential Reveals:**
- Prompt pattern: "Dark slide background (#0B1320) with bullet points appearing one by one: [ITEMS], clean sans-serif typography, each bullet fades in sequentially"
- Duration: 3–5s per item | Reference image: none
- Example: "Agenda slide with 4 bullets appearing sequentially: 'Setup', 'Configuration', 'Testing', 'Deployment'"

**Type F — Stylized B-Roll:**
- Prompt pattern: "Cinematic B-roll of [SCENE], film grain overlay, warm colour grading, shallow depth of field, 4:3 aspect within 16:9 frame"
- Duration: 3–6s | Reference image: optional mood reference
- Example: "Developer working at laptop in dimly lit room, 8mm film grain effect, warm tones"

**Type G — Digital Pan/Zoom:**
- This type does NOT use Hera — it uses the SubtleZoom Remotion component with extended transform interpolation on a static image or screen capture
- Duration: continuous | Reference image: the document/UI to pan across

### 3. Submit ALL API Calls (⚡ batch submit)

**Submit all briefs first, then poll all.** Do not wait for one to complete before submitting the next.

For each brief, following the Hera API reference from {dataFile}:

**Build and submit the request:**
```
POST https://api.hera.video/v1/videos
x-api-key: {HERA_API_KEY}
Content-Type: application/json

{
  "prompt": "{detailed_prompt}",
  "duration_seconds": {duration},
  "reference_image_url": "{public_url_or_omit}",
  "outputs": [
    {
      "format": "mp4",
      "aspect_ratio": "{aspect_ratio}",
      "fps": 30,
      "resolution": "1080p"
    }
  ]
}
```

**If One-by-One mode:** Before each call:
"**Generating Brief #{n}: {mg-id}**
Prompt: {prompt}
Duration: {duration}s | Aspect: {aspect_ratio} | Ref Image: {yes/no}
Confirm? [Y]es / [S]kip"

Capture the `video_id` from each successful submission response. Store all `video_id`s for polling.

"**Submitted {count} jobs to Hera. Polling for completion...**"

### 3b. Poll ALL Jobs (⚡ unified polling loop)

Poll all submitted jobs in a single loop:

```
while any job is still pending:
  for each pending video_id:
    GET /v1/videos/{video_id}
    if status == "success": mark complete, queue for download
    if status == "failed": mark failed
  report progress: "{completed}/{total} complete, {failed} failed"
  sleep 10s
```

**After each successful generation:**
"Generated: {mg-id} — downloading..."

**After each failed generation:**
"Generation failed for {mg-id}: {error_message}
[R]etry / [S]kip / [A]bort remaining"

### 4. Download and Save

For each successful generation:
1. Download the `.mp4` file from the completed job's output URL
2. Save to the resolved output path
3. Verify the file exists and has non-zero size

### 5. Generation Summary

"**Generation Complete**

| # | ID | Status | File Size | Output Path |
|---|-----|--------|-----------|------------|
| 1 | {mg-id} | {generated/skipped/failed} | {size} | {path} |
...

**Success:** {success_count}/{total_count}
**Skipped:** {skip_count}
**Failed:** {fail_count}"

If all successful or user accepts partial results, load, read entire file, then execute {nextStepFile}.

---

## SYSTEM SUCCESS/FAILURE METRICS

### SUCCESS:

- All (or user-accepted subset of) API calls completed
- Files downloaded and saved to correct output paths
- User informed of results for each brief
- Proceeding to completion step

### FAILURE:

- Calling API without user confirmation
- Not handling API errors
- Not verifying downloaded files exist
- Silently skipping failed generations without user notification
