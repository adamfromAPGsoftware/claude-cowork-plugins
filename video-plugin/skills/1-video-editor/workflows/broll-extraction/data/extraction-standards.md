# B-Roll Extraction Standards

## FFmpeg Command Template

```bash
ffmpeg -y -ss {start_time} -to {end_time} -i "{source_video}" -c:v libx264 -crf 18 -preset fast -an "{output_path}"
```

## Mandatory Flags

| Flag | Purpose | Exception |
|------|---------|-----------|
| `-an` | Strip all audio streams | NEVER — no exceptions |
| `-y` | Overwrite output without prompting | NEVER — no exceptions |
| `-c:v libx264` | H.264 video codec | Only if source requires different codec |
| `-crf 18` | Near-lossless quality | May adjust 16-20 range if needed |
| `-preset fast` | Encoding speed/quality balance | May use `medium` for final renders |

## Source File Rules

- **ALWAYS** use full-resolution source files
- **NEVER** use 480p proxy files for extraction
- Proxy files are for API calls only (DeepGram, Gemini)
- Extraction must preserve original resolution and quality

## Timestamp Format

Accepted formats:
- `HH:MM:SS.mmm` — e.g., `00:01:23.500`
- `HH:MM:SS` — e.g., `00:01:23`
- Seconds as float — e.g., `83.5`

**Note:** `-ss` before `-i` enables fast seeking (input seeking). This is the preferred method for accuracy with `-to` (absolute end time).

## Quality Settings

| Setting | Value | Notes |
|---------|-------|-------|
| CRF | 18 | Near-lossless. Lower = better quality, larger files |
| Preset | fast | Good balance. Use `medium` for final production |
| Pixel format | Default (yuv420p) | Widely compatible |

## Naming Convention

B-roll clip IDs follow the pattern: `broll-{sequence}-{descriptor}`

Examples:
- `broll-01-vscode-demo.mp4`
- `broll-02-terminal-commands.mp4`
- `broll-03-browser-walkthrough.mp4`
- `broll-04-slide-overview.mp4`

## Verification Commands

### Check for audio streams (should return empty)
```bash
ffprobe -v error -select_streams a -show_entries stream=codec_type -of csv=p=0 "{file}"
```

### Get video resolution
```bash
ffprobe -v error -select_streams v:0 -show_entries stream=width,height -of csv=s=x:p=0 "{file}"
```

### Get file duration
```bash
ffprobe -v error -show_entries format=duration -of csv=p=0 "{file}"
```

## Common Issues

| Issue | Cause | Fix |
|-------|-------|-----|
| Audio in output | Missing `-an` flag | Re-extract with `-an` |
| Low resolution | Used proxy file | Re-extract from full-res source |
| Seek inaccuracy | Keyframe alignment | Use `-ss` before `-i` for input seeking |
| Black frames at start | Seek before keyframe | Add small offset or use `-noaccurate_seek` |
| Large file size | CRF too low | CRF 18 is standard; don't go below 16 |
