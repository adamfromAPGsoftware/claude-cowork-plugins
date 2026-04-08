---
name: 'step-07-render'
description: 'npm install, Remotion studio preview, render to MP4'

nextStepFile: './step-08-audio-enhance.md'
---

# Step 7: Preview & Render

## STEP GOAL:

Install dependencies, launch Remotion Studio for preview, and render the final video to MP4 when the user approves. This is the final step — deliver the rendered video.

## MANDATORY EXECUTION RULES (READ FIRST):

### Universal Rules:

- CRITICAL: Read the complete step file before taking any action
- YOU MUST ALWAYS SPEAK OUTPUT in your Agent communication style with the config `{communication_language}`

### Step-Specific Rules:

- This step requires user interaction at every major decision point
- Preview before render — user must confirm visual correctness
- Render command must use the correct composition ID from theme.ts

## MANDATORY SEQUENCE

### 1. Install Dependencies

"**Installing Remotion dependencies...**"

```bash
cd {project_path} && npm install
```

Report result:
- If success: "Dependencies installed."
- If failure: Report error, suggest fixes (node version, npm cache clear).

### 1b. Run Studio Preflight

Before offering Preview or Render, execute the full Studio Preflight diagnostic:

Load, read entire file, then execute `./step-07b-studio-preflight.md`.

The preflight auto-fixes common causes of `media-playback-error` (symlinks, codec issues, missing entrypoint, port conflicts). Only continue to step 2 after all preflight checks pass.

### 2. Offer Preview

"**Remotion project ready for preview.**

**[P]review** — Launch Remotion Studio to preview in browser
**[R]ender** — Skip preview and render directly to MP4
**[F]ix** — Go back and fix issues before rendering

#### Menu Handling Logic:
- IF P: Execute preview (see section 3)
- IF R: Execute render (see section 4)
- IF F: Describe what to fix, apply changes, re-run QA, return to this menu
- IF Any other: Help user, redisplay menu

#### EXECUTION RULES:
- ALWAYS halt and wait for user input after presenting menu"

### 3. Launch Preview (IF P)

```bash
cd {project_path} && npx remotion studio src/index.ts
```

"**Remotion Studio launched. Preview at http://localhost:3000**

Review the composition in your browser. When ready:

**[R]ender** — Render to final MP4
**[F]ix** — Fix issues found during preview
**[X] Exit** — Stop without rendering"

Wait for user selection.

### 4. Render to MP4 (IF R)

Resolve output path:
- `{project_folder}/{project-slug}/video-editor/renders/{video-id}-{format}.mp4`

"**Rendering: {composition-name}**

Output: {output_path}
Resolution: {width}x{height}
FPS: {fps}
Duration: {total_seconds}s ({total_frames} frames)

Starting render..."

Before rendering, confirm the `audioOffsetMs` value. If the user adjusted it in Remotion Studio during preview, ask: "**What audioOffsetMs value did you settle on in Studio?** (default: 0)"

> **Hardware Acceleration Notes (Mac Studio 2025 — M4 Max, 64GB RAM):**
> - `--gl=angle` — enables GPU for CSS effects (shadows, blurs, gradients, transforms) in headless Chromium
> - `--hardware-acceleration if-possible` — uses Apple VideoToolbox for H.264 encoding instead of software libx264 (3-5x faster)
> - `--concurrency=8` — optimised for M4 Max (14-16 CPU cores). Run `npx remotion benchmark` to fine-tune.
> - If rendering on a different machine, adjust `--concurrency` and remove `--hardware-acceleration` if not on macOS.

```bash
cd {project_path} && npx remotion render src/index.ts {CompositionId} out/{composition-name}.mp4 --codec h264 --crf 15 --concurrency=8 --gl=angle --hardware-acceleration if-possible --props='{"audioOffsetMs": {audioOffsetMs}}'
```

> Note: Always use `src/index.ts` as the entrypoint (NOT `src/Root.tsx`). The `out/` path is local and avoids shell-quoting issues with spaces in absolute paths. Copy to `{output_path}` after render completes if needed.

#### Maximum Quality Render Rules

**CRITICAL: The render output MUST match the source video resolution and frame rate exactly. Never downscale or reduce quality.**

1. **Resolution & FPS come from theme.ts** — which is probed from the source video via ffprobe. If the source is 4K 60fps, the composition is 4K 60fps. If it's 1080p 30fps, the composition is 1080p 30fps. The render inherits these from the Composition config.
2. **CRF 15** — Constant Rate Factor for near-lossless quality. Range is 0-51, lower = better. CRF 15 produces visually lossless output. Never use CRF > 18.
3. **Never add `--scale`** — Remotion's `--scale` flag would downscale the output. Never include it.
4. **Never add `--height` or `--width`** — These override the composition dimensions. Never include them.
5. **Codec is always h264** — Compatible with all platforms. The `--hardware-acceleration if-possible` flag uses Apple VideoToolbox for fast encoding without quality loss.
6. **Verify output resolution** — After render, run `ffprobe` to confirm the output matches `PROJECT.width` x `PROJECT.height` @ `PROJECT.fps`. If it doesn't match, the render is invalid.

**Expected output sizes (approximate):**

| Resolution | FPS | Duration | Expected Size |
|-----------|-----|----------|--------------|
| 3840×2160 | 60 | 12 min | 4-6 GB |
| 3840×2160 | 60 | 1 min | 400-500 MB |
| 1920×1080 | 30 | 12 min | 1-2 GB |
| 1920×1080 | 30 | 1 min | 100-150 MB |

If the output file is significantly smaller than expected, the quality may be insufficient — check CRF and resolution settings.

### 5. Verify Render

After render completes:
1. Check output file exists
2. Check file size is non-zero
3. Get duration with ffprobe to verify it matches expected

### 6. Final Summary

"**Remotion Edit — Complete**

**Rendered Video:**
- File: {output_path}
- Size: {file_size}
- Duration: {duration}
- Resolution: {width}x{height}

**Project Files:**
- Remotion project: {project_path}/
- QA Report: {project_path}/qa-report.md
- Theme config: {project_path}/src/theme.ts

**Proceeding to audio enhancement...**"

Load, read entire file, then execute {nextStepFile}.

---

## SYSTEM SUCCESS/FAILURE METRICS

### SUCCESS:

- Dependencies installed successfully
- Preview offered to user
- Render completed to correct output path
- Output file verified (exists, non-zero, correct duration)
- Clear summary with all file paths

### FAILURE:

- Rendering without user confirmation
- Not verifying output file after render
- Not reporting render errors
- Not offering preview option
