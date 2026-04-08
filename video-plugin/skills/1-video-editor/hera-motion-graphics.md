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

Extract Visual Asset Source Map entries where `type: motion-graphic`. For each: mg-id, prompt/description, duration, aspect_ratio, reference_image, image_source.

### 1.3 Manual Input (if M)

Collect per brief: prompt (required), duration (1-60s, default 5s), aspect ratio (16:9/9:16/1:1/4:5), reference image source.

### 1.4 Validate

Check HERA_API_KEY exists in `.env`. Resolve output paths. Present plan for confirmation.

---

## Phase 2: Generate

### 2.1 Prepare Reference Images

**fetch-logo:** Logo acquisition via waterfall (Simple Icons -> SVG Logos -> Logotypes.dev -> Logo.dev). Visual verification required.

**branded-assets:** Copy from `_bmad/_memory/video-editor-sidecar/branded-assets/`. Upload to public URL.

**frame-extract:** Extract frame from source video at specified timestamp. Auto-extract is default for Type B and Type C MGs where tool is visible in body footage.

**web-screenshot:** Use unified resolver for full waterfall + upload.

**canvas-build:** Composite multiple images at appropriate resolution.

### 2.2 MG Brief Templates by Type (Long-Form)

**Type A — Text/Number Overlay:** Bold text with pop-in animation on dark background. 3-4s, no reference image.

**Type B — Logo Graphic:** Tool logo sliding in with brand-color glow effect. 4-5s, reference: tool logo. Use tool's primary color (Claude: #D97757, ChatGPT: #10A37F, n8n: #FF6D5A, Cursor: #7B61FF).

**Type C — UI Mockup:** Recreated platform interface with authentic colors and layout. 5-8s, reference image strongly recommended. Inject tool's exact hex colors, UI layout, and key visual elements.

**Type D — Concept Graphic:** Minimalist diagram with tool-styled design language. 5-15s, style with tool's visual identity.

**Type E — Sequential Reveals:** Bullet points appearing one by one. 3-5s per item, no reference image.

**Type F — Stylized B-Roll:** Cinematic B-roll with film grain overlay. 3-6s, optional mood reference.

**Type G — Digital Pan/Zoom:** Uses SubtleZoom Remotion component, NOT Hera. Continuous duration.

### 2.3 Batch Submit API Calls

Submit ALL briefs first, then poll all (batch-submit-then-poll pattern):

```
POST https://api.hera.video/v1/videos
x-api-key: {HERA_API_KEY}
{
  "prompt": "{detailed_prompt}",
  "duration_seconds": {duration},
  "reference_image_url": "{url_or_omit}",
  "outputs": [{"format": "mp4", "aspect_ratio": "{ratio}", "fps": 30, "resolution": "1080p"}]
}
```

### 2.4 Unified Polling Loop

Poll all submitted jobs every 10s until all reach "success" or "failed". Download completed `.mp4` files to output paths.

---

## Phase 3: Completion

Verify all generated `.mp4` files exist and are non-zero. Present summary with status per MG. Recommend next: Storyboard or Remotion Edit.
