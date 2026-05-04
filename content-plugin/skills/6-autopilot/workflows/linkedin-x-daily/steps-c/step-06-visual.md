---
name: step-06-visual
description: Generate or identify visual asset based on today's format and topic source
nextStep: ./step-07-quality.md
---

# Step 6: Visual Asset

## Goal

For image and video-clip formats, produce or locate the visual asset. For text format, skip and proceed.

Image generation is fully automatic — run immediately without asking for permission or confirming first.

## Sequence

### Step 0: Style Profile Visual Guidance

Before branching by format, check if a style profile was selected in step-04. If so, apply its "Asset Guidance" section from `{adamStyleProfiles}` within the format-specific logic below:

| Style | Visual guidance |
|-------|----------------|
| S1 Video Lead Magnet | 15-30s screen recording showing a system building/running or a result appearing; 20x speed |
| S2 Carousel Lead Magnet | Generate carousel via carousel generator; dark background, green accent, 6-8 slides |
| S3 Authority Contrarian | Text only — do not generate an image |
| S4 Personal Origin Story | Text only — do not generate an image |
| S5 Personal Event/Authority | Real photo of the creator at an event or in context; source from asset catalog stage/outdoor entries |

These are inputs to the Path A/B/C logic — they don't replace the format branching, they constrain the asset selection within it.

---

### If format = text

No visual needed. Set `media_path: null`, `media_type: none`.

Proceed directly to step-07.

---

### If format = image

Use this decision tree based on `topic_source` and post content:

---

#### Path A: YouTube repurpose (`topic_source = youtube-repurpose`)

Download the YouTube thumbnail directly. No generation needed.

```bash
curl -s "{thumbnail_url from channel-library.json}" -o "{draftQueue}/YYYY-MM-DD-linkedin-image.jpg"
```

The `thumbnail_url` is in `{youtubeLibrary}` under the video's entry (field: `thumbnail_url`).

Set `media_path: {draftQueue}/YYYY-MM-DD-linkedin-image.jpg`, `media_type: image`.

This is always the right choice for YouTube repurpose — the thumbnail already has the face, the number, and the hook visual baked in.

**Dimensions note:** YouTube thumbnails are 16:9 (1280×720). LinkedIn displays these as landscape. This is fine — thumbnails are designed for that ratio and key content is centered.

---

#### Path B: Tool-focused post (technical or nurture pillar, NOT youtube-repurpose)

The image should feature the tool(s) mentioned in the post. For style reference, check `{project-root}/context/context/brand-assets/` for any prior tool-logo image examples.

**Step B1:** Identify the tool(s) featured in the post (e.g., Claude Code, n8n, Supabase, Lovable, Cursor).

**Step B2:** Source logos using the hierarchy:
1. `{project-root}/context/context/brand-assets/` — check for existing logos
2. Simple Icons (simpleicons.org) — SVG
3. SVG Repo (svgrepo.com) — SVG
4. CompanyEnrich

**Step B3:** Generate via fal-ai MCP:

```
mcp__fal-ai__generate_image(
  prompt="{2-paragraph prompt — see guidelines below}",
  image_size="square_hd"
)
```

Save the output to `{draftQueue}/YYYY-MM-DD-linkedin-image.png`.

**Dimensions:** Always use `image_size: "square_hd"` (renders at 1024×1024px, displayed as 1:1). Square takes up more vertical feed space than landscape on mobile, where most LinkedIn browsing happens. Do NOT use 16:9 for generated images.

**Tool image prompt guidelines:**
- Dark background (#0D0D0D or #111111)
- Tool logo(s) prominently displayed — large, centered or left-aligned
- Brand accent colour (`{brand.colors.primary}` from config.yaml) used sparingly (glow, underline, or border — one usage only)
- A short anchor text stat or phrase (e.g., "100x faster", "$5K/month saved") rendered as bold white text
- No stock photo aesthetics, no clutter, no gradients
- Clean, technical, credible — like a developer's dashboard card

For style reference, check `{project-root}/context/context/brand-assets/` for any prior tool-logo image examples.

---

#### Path C: Personal post

The image should use a real reference photo of the creator that metaphorically matches the post's theme or emotional tone.

**Step C1:** Read `{project-root}/context/context/brand-assets/asset-catalog.yaml`.

**Step C2:** Search the catalog for entries with `use_cases` or `mood`/`emotion` tags that match the post's theme. Examples:
- Post about failure/learning → find a photo tagged with `reflective`, `candid`, `thinking`
- Post about results/wins → find a photo tagged with `confident`, `working`, `at desk`
- Post about the grind/process → find a photo tagged with `focused`, `building`, `laptop`

**Step C3:** If a matching photo is found, use it directly as the image — no generation needed. Crop or note ideal crop to 1:1 (square) if the original is landscape.
Set `media_path: {photo path from catalog}`, `media_type: image`.

**Step C4:** If no suitable photo exists yet (catalog may be sparse), note this in the draft frontmatter:
`quality_note: "Personal post image — no matching reference photo in asset catalog. Add photos with relevant mood tags."`
Fall back to generating a minimal text-on-dark card as a placeholder.

---

### If format = video-clip

**Step 6C: Select YouTube source video**

Read `{youtubeLibrary}`. If `youtube_video_id` is already set from step-02 (YouTube-repurpose), use that video. Otherwise, find the most relevant video from the library based on today's topic.

**Step 6D: Select the best segment**

Load the video transcript from `{project-root}/context/youtube/transcripts/{video_id}.json`.

Identify a 15-30 second segment where:
- Something is visually happening (the creator typing, a tool running, a result appearing)
- The moment connects directly to the post's key point
- It's self-contained enough to make sense without audio

Extract: `start_time` (seconds), `end_time` (seconds), `segment_description`.

**Step 6E: Output ffmpeg command**

```
ffmpeg -i {video_filename} -ss {start_time} -t {clip_duration} -vf "setpts=0.05*PTS" -an -c:v libx264 -preset fast output-{video_id}-{start_time}s-20x.mp4
```

Notes:
- `setpts=0.05*PTS` = 20x speed. Adjust: 0.10 = 10x, 0.025 = 40x
- `-an` strips audio (sped-up voice sounds terrible)
- Output filename includes video_id and start time for traceability

Set `media_path: null` (user must run ffmpeg), `media_type: video-clip`, `ffmpeg_command: {command}`, `video_segment: {description}`.

## Output Summary

```
Visual asset
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Path:   {Path A | B | C}
Format: {image | video-clip | none}
{If image: "Asset: {media_path} (youtube-thumbnail | tool-generated | reference-photo | placeholder)"}
{If video-clip: "Source video: {title} ({video_id})"}
{If video-clip: "Segment: {start}-{end}s — {description}"}
{If video-clip: "ffmpeg command: {command}"}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

Then immediately load and execute step-07.
