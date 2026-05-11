---
name: hera-motion-graphics
description: Generate motion graphic clips via Hera Video API
menu-code: HM
---

# [HM] Hera Motion Graphics

**Goal:** Generate motion graphic video clips using the Hera Video API — from storyboard briefs or manual input — and deliver them as `.mp4` files ready for Remotion integration.

**Role:** Motion graphics pipeline operator. API-driven generation with technical precision.

---

## Phase 1: Initialize

### 1.1 Determine Input Source

"**Hera Motion Graphics — Initialization**

[S] Storyboard — Auto-discover briefs from approved storyboard's Visual Asset Source Map
[M] Manual — Enter briefs manually (prompt, aspect ratio, duration, reference image)"

### 1.2 Storyboard Discovery (if S)

Extract Visual Asset Source Map entries where `visual_type: motion-graphic`. For each entry:

**Eligibility gate (REQUIRED — long-form intro):** Check that the entry has `hera: true`. If it does NOT:
- This brief was not approved by the storyboard process for Hera generation.
- **Stop and report:** "MG {mg-id} is assigned `visual_type: motion-graphic` but is missing `hera: true`. This slot should use a showcase template. Please update the storyboard's Visual Asset Source Map to reassign this slot, or confirm Hera eligibility before continuing."
- Do not generate the clip until the storyboard is corrected.

For each `hera: true` brief, collect: mg-id, prompt/description, duration, aspect_ratio, reference_image, image_source, `template_category` (should be `hera-interface`).

### 1.3 Manual Input (if M)

Collect per brief: prompt (required), duration (1-60s, default 5s), aspect ratio (16:9/9:16/1:1/4:5), reference image source.

### 1.4 Validate

Check HERA_API_KEY exists in `.env`. Resolve output paths. Present plan for confirmation.

---

## Phase 2: Generate

### 2.1 Prepare Reference Images

**Reference image is MANDATORY for all long-form intro Hera briefs.** A brief without a reference image produces generic chrome that looks fabricated and inconsistent with the real interface. If no reference image can be obtained, the brief must be demoted to a showcase template — do not generate without one.

Resolve the reference image using this waterfall (stop at the first that succeeds):

1. **frame-extract (preferred):** Extract a frame from the source video at a timestamp where the target tool UI is clearly visible. Crop to show only the interface. Save as PNG. This produces the most authentic reference.
2. **web-screenshot:** Take a full-page screenshot of the tool's live web interface via the unified resolver. Upload to public URL.
3. **branded-assets:** Copy from `_bmad/_memory/video-editor-sidecar/branded-assets/` if a matching asset exists.
4. **canvas-build:** Composite logo + UI screenshot at appropriate resolution.

**If all four fail:** Do not generate the Hera clip. Report: "No reference image obtainable for {mg-id} ({tool name}). Demote this slot to a showcase template ({recommended_showcase_component}) and update the storyboard." Stop the pipeline for this brief only — continue with remaining eligible briefs.

**fetch-logo** is only used when the brief is a `B: Logo Graphic` type (i.e., just the tool logo, no interface frame needed). For all `interface-zoom` and `interface-ui-mockup` types, the frame-extract or web-screenshot waterfall above takes precedence.

### 2.2 Long-Form Hera Brief Types

Hera is only used for three types in long-form (Types A, D, E are now covered by showcase templates):

---

**Type: `interface-zoom`** (was Type C, elevated)

The canonical long-form Hera style. Every `hera: true` brief that shows a tool UI in action should use this format.

**Requirements:**
- Duration: 5–8s
- Reference image: MANDATORY (frame-extract or web-screenshot of the actual interface)
- Prompt must follow the **Interface Zoom Template** below

**Interface Zoom Template:**

> Starting from a wide view of [INTERFACE NAME — match reference image exactly], showing [describe the visible screen: sidebar, canvas, chat panel, etc.]. The camera begins a smooth, continuous push-in zoom toward [ZOOM TARGET — specific UI element: terminal panel, input field, code line, button, conversation thread]. As the camera tightens, [LIVE ACTION — describe what happens in the interface: green execution logs appear line by line filling the terminal / text types character-by-character into the input field / a button pulses and is clicked / agent steps process sequentially]. The zoom tightens until only [FINAL FRAME DESCRIPTION — what fills the screen at the end: the log output, the typed text, the result]. Professional minimal tech aesthetic. No people, no faces, no invented chrome — all colours and UI elements match the reference image exactly.

**Example (canonical — use as style reference):**

> Starting from a wide view of a code editor matching the reference image, then smoothly zooming into the terminal panel on the right side. Green execution logs appear line-by-line as the camera pushes in: "Scanning 10 channels in parallel...", "Extracting transcripts...", "Calculating outlier scores...", "Output report created." The text typing animation fills the terminal as the zoom tightens to just the log output. Do not include any people or faces. Clean modern design, professional minimal tech aesthetic.

---

**Type: `interface-ui-mockup`** (was Type B when interface context is needed)

Use when a tool logo alone doesn't convey the integration — the interface itself (Gmail inbox, Calendar grid, Claude conversation) needs to be shown in motion without a zoom-and-type action.

**Requirements:**
- Duration: 4–6s
- Reference image: MANDATORY
- Prompt: Describe the interface faithfully using the reference image. Show the tool in its natural state with subtle animation (cards loading, rows populating, status indicators updating). Tool's exact hex colours. No invented UI elements.

---

**Type: `interface-pan`** (was Type G when over a live interface)

Use for slow pan across a wide dashboard, Excalidraw canvas, or code file where the width exceeds the frame.

**Requirements:**
- Duration: 4–8s
- Reference image: MANDATORY (the full-width content to pan across)
- Prompt: Describe start position, direction, and end position. Smooth Ken-Burns-style horizontal or vertical movement. No zoom unless combined with pan.

---

**Types NOT handled by Hera (use showcase templates):**
- Number/text overlays → `NumberCountUp`, `MetricCard`, `BoldStatement`
- Sequential reveals / lists → `ChecklistReveal`, `StackedPillsReveal`
- Concept diagrams → `FlowchartAnimation`, `TransformationArrow`
- Logo-only callouts → `ToolLogoGrid`, `GlowingIconPop`
- Stylized B-roll → `BRollOverlay` with CSS filters

### 2.3 Batch Submit API Calls

Submit ALL briefs first, then poll all (batch-submit-then-poll pattern):

```bash
curl -s -X POST https://api.hera.video/v1/videos \
  -H "x-api-key: $HERA_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "{detailed_prompt}",
    "duration_seconds": {duration},
    "reference_image_url": "{url_or_omit}",
    "outputs": [{"format": "mp4", "aspect_ratio": "16:9", "fps": "30", "resolution": "1080p"}]
  }'
```

**Critical API schema notes (validated against docs.hera.video):**
- `outputs` array is **required** — the API rejects requests without it
- All 4 output fields are **required**: `format`, `aspect_ratio`, `fps`, `resolution`
- `fps` must be a **string** (`"24"`, `"25"`, `"30"`, `"60"`) — NOT a number. Integers are rejected.
- `resolution` must be one of: `"360p"`, `"480p"`, `"720p"`, `"1080p"`, `"4k"`
- `aspect_ratio` options: `"16:9"`, `"9:16"`, `"1:1"`, `"4:5"`
- `reference_image_url` — omit the key entirely if not needed (don't pass null)
- Response returns `{ "video_id": "vid_..." }` — store this for polling

**Status polling:**
```bash
curl -s https://api.hera.video/v1/videos/{video_id} \
  -H "x-api-key: $HERA_API_KEY"
```
Response fields: `video_id`, `status` (`in-progress` → `success`/`failed`), `outputs[].file_url` (S3 signed URL when complete — **field is `file_url` not `url`**).

**Download pattern:**
```bash
file_url=$(curl -s "https://api.hera.video/v1/videos/$vid" \
  -H "x-api-key: $HERA_API_KEY" | \
  python3 -c "import sys,json; d=json.load(sys.stdin); print(d['outputs'][0]['file_url'])")
curl -sL "$file_url" -o output.mp4
```

### 2.4 Unified Polling Loop

Poll all submitted jobs every 10s until all reach "success" or "failed". Download completed `.mp4` files to output paths.

---

## Phase 3: Completion

Verify all generated `.mp4` files exist and are non-zero. Present summary with status per MG. Recommend next: Storyboard or Remotion Edit.
