---
name: 'step-08-audio-enhance'
description: 'Post-render broadcast voice enhancement using FFmpeg — zero extra dependencies'
---

# Step 8: Post-Render Audio Enhancement

## STEP GOAL:

Apply a professional broadcast voice filter chain to the rendered MP4 using FFmpeg. This step improves audio quality (removes noise, compresses dynamics, normalises loudness to -16 LUFS) without re-encoding the video track. FFmpeg is already installed in this pipeline (used in B-roll extraction and clipping steps).

## MANDATORY EXECUTION RULES (READ FIRST):

### Universal Rules:

- CRITICAL: Read the complete step file before taking any action
- YOU MUST ALWAYS SPEAK OUTPUT in your Agent communication style with the config `{communication_language}`

### Step-Specific Rules:

- This step is **optional** — offer skip option before running
- Use `-c:v copy` — the video track is NEVER re-encoded
- Input = rendered MP4 from step-07; output = `{video-id}-enhanced.mp4` in the same renders folder
- Verify output duration matches input ±1 second after processing

---

## MANDATORY SEQUENCE

### 1. Detect Rendered MP4

Identify the render output from step-07:
- Path: `{project_folder}/{project-slug}/video-editor/renders/{video-id}-{format}.mp4`

Verify it exists and is non-zero with ffprobe:
```bash
ffprobe -v error -show_entries format=duration,size -of json "{input_path}"
```

Report: file size and duration.

### 2. Offer Enhancement

"**Audio Enhancement Available**

The rendered video can be processed with an 8-filter broadcast voice chain:
- `highpass=f=80` — removes low-frequency rumble (AC hum, desk vibration)
- `lowpass=f=15000` — removes high-frequency hiss above 15kHz
- `afftdn=nf=-25` — FFT-based noise reduction at -25dB noise floor
- `equalizer=f=200:g=-3` — mud cut at 200Hz for cleaner vocals
- `equalizer=f=3500:g=4` — presence boost at 3.5kHz for vocal clarity
- `equalizer=f=12000:g=2` — air boost at 12kHz for broadcast shimmer
- `acompressor` — dynamic range compression (quieter parts up, loud peaks tamed)
- `loudnorm=I=-16:TP=-1.5:LRA=11` — EBU R128 normalisation to -16 LUFS (YouTube/podcast broadcast standard)

Video track is NOT re-encoded (`-c:v copy`) — only the audio track is processed.
Estimated processing time: 10–30s for a typical 4K 60fps video.

**[E]nhance** — Run audio enhancement
**[S]kip** — Skip and finish pipeline"

Wait for user selection.

#### Menu Handling Logic:
- IF E: Execute enhancement (see section 3)
- IF S: Execute section 5 (Final Summary — skip)
- IF Any other: Redisplay menu

### 3. Run Enhancement

Resolve output path:
- `{project_folder}/{project-slug}/video-editor/renders/{video-id}-enhanced.mp4`

"**Enhancing audio...**

Input:  {input_path}
Output: {output_path}
"

```bash
ffmpeg -y -i "{input_path}" \
  -af "highpass=f=80, \
       lowpass=f=15000, \
       afftdn=nf=-25, \
       equalizer=f=200:t=q:w=1.5:g=-3, \
       equalizer=f=3500:t=q:w=2:g=4, \
       equalizer=f=12000:t=q:w=1:g=2, \
       acompressor=threshold=0.089:ratio=9:attack=200:release=1000:makeup=2, \
       loudnorm=I=-16:TP=-1.5:LRA=11" \
  -c:v copy \
  -c:a aac -b:a 192k \
  "{output_path}"
```

**Filter chain explained (8 filters):**
1. `highpass=f=80` — removes low-frequency rumble (AC hum, desk vibration)
2. `lowpass=f=15000` — removes high-frequency hiss above 15kHz
3. `afftdn=nf=-25` — FFT-based noise reduction at -25dB noise floor
4. `equalizer=f=200:t=q:w=1.5:g=-3` — **Mud cut**: reduces muddiness at 200Hz (-3dB), cleaner vocal clarity
5. `equalizer=f=3500:t=q:w=2:g=4` — **Presence boost**: adds vocal presence/clarity at 3.5kHz (+4dB), makes voice cut through
6. `equalizer=f=12000:t=q:w=1:g=2` — **Air boost**: adds "shimmer" at 12kHz (+2dB), professional broadcast quality
7. `acompressor` — dynamic range compression (quieter parts up, loud peaks tamed)
8. `loudnorm=I=-16:TP=-1.5:LRA=11` — EBU R128 normalisation to -16 LUFS (YouTube/podcast broadcast standard)

### Optional: AI Audio Enhancement

For studio-quality voice processing beyond FFmpeg filters, consider:
- **Adobe Podcast Enhance** (free tier, web upload) — AI-powered voice enhancement
- **Auphonic** (API available, freemium) — intelligent loudness + noise + EQ
- **ElevenLabs Audio Isolation** — isolates voice from background noise

These can be run on the raw audio BEFORE Remotion render for best results,
or on the rendered MP4 as a replacement for the FFmpeg chain.

### 4. Verify Enhancement

After FFmpeg completes:

```bash
ffprobe -v error -show_entries format=duration,size -of json "{output_path}"
ffprobe -v error -select_streams a:0 \
  -show_entries stream=codec_name,bit_rate \
  -of csv=p=0 "{output_path}"
```

Verify:
- [ ] Output file exists and size > 0
- [ ] Duration matches input ±1 second
- [ ] Audio codec = `aac`
- [ ] Video codec still = `h264` (not re-encoded)

**If any check fails:** Report the FFmpeg error output and suggest re-running manually.

### 5. Final Summary

"**Remotion Edit — Complete**

**Original Render:**
- File: {input_path}
- Size: {input_size}
- Duration: {duration}s

**Enhanced Version:** {enhanced or 'skipped'}
- File: {output_path}
- Size: {output_size}
- Audio: AAC 192kbps, -16 LUFS (EBU R128)
- Video: copied losslessly (no re-encode)

**Project Files:**
- Remotion project: {project_path}/
- QA Report: {project_path}/qa-report.md
- Theme config: {project_path}/src/theme.ts

**Pipeline Complete.** The video is ready for review by the Editor agent or direct publishing via the Publisher agent.

**Next Steps:**
- Review with the **Editor** agent for quality feedback
- Schedule with the **Publisher** agent for distribution"

---

## SYSTEM SUCCESS/FAILURE METRICS

### SUCCESS:

- Input MP4 detected and verified with ffprobe
- FFmpeg command runs with all 8 audio filters (highpass, lowpass, afftdn, 3x EQ, acompressor, loudnorm)
- `-c:v copy` used (no video re-encode)
- Output verified: correct duration, AAC audio, H.264 video
- Clear summary with both file paths and sizes

### FAILURE:

- Re-encoding the video track (omitting `-c:v copy`)
- Not verifying output file after enhancement
- Running enhancement without user confirmation
- Missing any of the 8 audio filters in the chain
