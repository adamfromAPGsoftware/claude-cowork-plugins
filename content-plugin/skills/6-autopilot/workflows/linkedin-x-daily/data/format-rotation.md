# Content Format Rotation

## Rotation Sequence

```
[text, image, text, video-clip, text, image, text]
```

Cycle length: 7. Hits ~57% text, ~29% image, ~14% video-clip.

The `current_index` in `autopilot-state.yaml` advances by 1 each run, wrapping to 0 after index 6.

---

## Format Definitions

### Text
**Asset required:** None — pure copywriting.
**LinkedIn specs:** 800-1300 characters. Single-line paragraphs, liberal line breaks, → arrows for lists.
**X specs:** Single tweet (280 chars) or short thread (2-4 tweets) depending on content density.
**When text dominates:** 5 proven post formats are all text-only. Text works when hook quality is elite.
**Generation:** Write the post body. No image generation needed.

### Image
**Asset required:** 1 image (1:1 for LinkedIn, 16:9 for X).
**LinkedIn specs:** 1200x1200 recommended, JPEG/PNG, max 8MB.
**X specs:** 1200x675 recommended.
**Best for:** Lead magnet posts (image + keyword CTA = high engagement). Personal posts with a visual metaphor.
**Generation steps:**
1. Check `context/brand-assets/` for any indexed reference images (screenshots, tool logos) relevant to the post topic — use these first
2. If no suitable existing image, generate via fal-ai MCP:
   - Call `mcp__fal-ai__generate_image` with `model_id: "fal-ai/nano-banana-2"` (REQUIRED), `image_size: "square_hd"` for LinkedIn, `image_size: "landscape_16_9"` for X
   - For tool logos: use the logo sourcing hierarchy (Simple Icons → SVG Repo → CompanyEnrich)
   - For the creator in the image: upload reference photo first with `mcp__fal-ai__upload_file`, then use `mcp__fal-ai__edit_image` with `model: "fal-ai/nano-banana-2/edit"` + `strength: 0.92` (NOT `generate_image_from_image`)
3. Image prompt rules: 2+ paragraph description, real content only, GREEN gear not blue, no static text overlays

### Video Clip
**Asset required:** 15-30s sped-up clip from an existing YouTube video.
**Best for:** Technical/educational posts where seeing a demo is more convincing than reading about it.
**Generation steps:**
1. Identify the most relevant YouTube video from `context/youtube/channel-library.json`
2. Select a 15-30 second segment from the video transcript that best illustrates the post's key point
3. Output an ffmpeg command to extract + speed up the segment:
   ```
   ffmpeg -i input.mp4 -ss {start} -t {duration} -vf "setpts=0.05*PTS" -an -c:v libx264 output-20x.mp4
   ```
   (0.05 = 20x speed, adjust multiplier as needed)
4. Note: User runs the ffmpeg command manually, or the skill can use Bash if available
**Format note:** Video post text should promise/reference what the viewer will see — not generic copy that ignores the visual.
