# Storyboard Standards

## Required Frontmatter Fields

```yaml
---
status: DRAFT | APPROVED      # Must be APPROVED for Remotion Edit
scope: intro-only | full-video
stepsCompleted: []             # Array of completed step names
lastStep: ''                   # Name of last completed step
date: ''                       # Creation date
user_name: ''                  # Creator
video_id: ''                   # Video identifier
project_slug: ''               # Project identifier
target_content_type: ''        # Segment being storyboarded (e.g., intro) — speaker map + timeline timestamps
main_content_type: ''          # Main video scanned for B-roll (e.g., body) — video-extract sources
---
```

## Required Sections

Every complete storyboard MUST contain these sections (in order):

1. **Production Brief** — Video overview, section breakdown, B-roll candidates, timing calibration
2. **Speaker Position Map** — Where the speaker appears at each timestamp (may note "unavailable" if no visual analysis)
3. **Visual Asset Source Map** — Definitive list of all visual assets: video-extracts, motion graphics, branded templates — with IDs, types, sources, and status
4. **Text Placement Strategy** — Caption positions per section, template assignments, density rules
5. **Master Timeline** — Every segment with all required fields
6. **Pacing Validation Report** — Visual events/min per section with pass/fail status

## Timeline Row Schema

Every row in the Master Timeline MUST have:

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| segment_id | string | Yes | Sequential: seg-001, seg-002, etc. |
| start_time | timestamp | Yes | HH:MM:SS.mmm format |
| end_time | timestamp | Yes | HH:MM:SS.mmm format |
| duration_frames | integer | Yes | Duration in frames at 30fps |
| visual_type | enum | Yes | speaker / video-extract / motion-graphic / branded-template / chapter-card / cta |
| template | string | Yes | Remotion template name — must match visual_type: video-extract→BRollOverlay, motion-graphic→MotionGraphic, speaker→SubtleZoom/PowerCaption |
| source_file | path | Yes | Path to video/image file |
| asset_ref | string | No | Visual Asset Source Map ID (required if visual_type is video-extract, motion-graphic, or branded-template) |
| caption_text | string | No | Caption or overlay text |
| caption_position | enum | No | top-left / top-right / bottom-left / bottom-right / bottom-center |
| section | string | Yes | Production brief section this belongs to |
| notes | string | No | Special instructions for Remotion Edit |

## Timeline Integrity Rules

1. **Zero gaps:** Each segment's end_time MUST equal the next segment's start_time
2. **No overlaps:** No two segments may claim the same time range
3. **Total duration:** Sum of all segment durations must match production brief total
4. **Template validity:** Every template referenced must exist in the template library
5. **Asset references:** Every asset_ref must exist in the Visual Asset Source Map

## Transition Rules

Fade/flash transitions (the opacity fade in/out on BRollOverlay and motion-graphic segments) only apply when there is a **visual type change** between segments.

| From → To | Transition |
|-----------|-----------|
| speaker → b-roll/motion-graphic | Fade in on the b-roll/MG (built into BRollOverlay) |
| b-roll/motion-graphic → speaker | Fade out on the b-roll/MG (built into BRollOverlay) |
| speaker → speaker | **Hard cut — NO transition.** Seamless since both use the same source video with `startFrom` |
| speaker → branded-template | Fade in on branded template (built into component) |
| branded-template → speaker | Fade out on branded template (built into component) |
| b-roll → b-roll | Both segments have their own fade in/out |

**Key principle:** Two consecutive speaker segments (whether SubtleZoom, PowerCaption, or bare speaker) must be a seamless hard cut — the viewer should not perceive any transition between them because they are showing the same continuous speaker footage.

## Visual Asset Source Map Entry Schema

### Video Extract

| Field | Required | Description |
|-------|----------|-------------|
| broll-id | Yes | Unique identifier |
| type | Yes | `video-extract` |
| source_video | Yes | Path to full-resolution MAIN source video (raw, not proxy) |
| start_time | Yes | Extraction start timestamp in the MAIN video's timeline (verified via main video visual analysis) |
| end_time | Yes | Extraction end timestamp in the MAIN video's timeline (verified via main video visual analysis) |
| description | Yes | What's shown in this clip |
| context | No | What's being discussed at this point (from main video transcript) |
| status | Yes | pending-extraction / extracted |

### Motion Graphic

| Field | Required | Description |
|-------|----------|-------------|
| mg-id | Yes | Unique identifier |
| type | Yes | `motion-graphic` |
| prompt | Yes | Production-ready Hera Video prompt. Must follow the 5-part structure: (1) Subject, (2) Motion, (3) Style, (4) Color, (5) Duration hint. Use motion design vocabulary. Vague prompts are not acceptable. |
| duration | Yes | 1-5 seconds |
| aspect_ratio | Yes | 16:9 / 9:16 / 1:1 |
| reference_image | Conditional | Path to reference image — REQUIRED when MG involves brands/logos/specific visuals. Not needed for abstract/text-only MG |
| image_source | Yes | Where the reference image comes from. Valid values: `branded-assets`, `frame-extract`, `canvas-build`, `none`. Always populated — use `none` when no reference image is needed. Type C entries should default to `frame-extract` or `canvas-build` (not `none`) |
| tool_name | Conditional | Named tool/platform referenced by this MG (required for Type B/C/D entries that reference a specific tool) |
| tool_visual_details | Conditional | Tool's visual identity from `tool-visual-reference.md`: primary hex codes, UI layout, key visual elements (required when `tool_name` is populated) |
| description | Yes | What this MG conveys |
| status | Yes | pending-generation / generated |

### Branded Template

| Field | Required | Description |
|-------|----------|-------------|
| bt-id | Yes | Unique identifier |
| type | Yes | `branded-template` |
| template_name | Yes | Remotion component name (e.g., UpworkProfile, AgencyBrand) |
| description | Yes | What this template displays |
| status | Yes | `ready` (branded templates are always available) |

## Validation Checklist

### Document Structure (7 checks)
- Frontmatter has all required fields
- Production Brief present
- Speaker Position Map present
- Visual Asset Source Map present
- Text Placement Strategy present
- Master Timeline present
- Pacing Validation Report present

### Prerequisites (2 checks — HARD BLOCK)
- Transcript JSON exists and was loaded
- Visual Analysis JSON exists and was loaded

### Timeline Integrity (6 checks)
- All segments have required fields
- Zero gaps between segments
- No overlaps
- Total duration matches
- All templates valid
- All visual asset references valid

### Visual Asset Source Map (6 checks)
- All entries have unique IDs
- Video-extract entries have source + timestamps verified against visual analysis
- Motion-graphic entries have production-ready prompt (5-part structure: subject, motion, style, color, duration hint) + duration + aspect ratio
- Motion-graphic entries have `image_source` populated with valid enum (`branded-assets`, `frame-extract`, `canvas-build`, `none`) — and `reference_image` set when `image_source` is not `none`
- Type B/C/D motion-graphic entries referencing a named tool must have `tool_name` and `tool_visual_details` populated (from `tool-visual-reference.md`)
- Type C motion-graphic entries should default `image_source` to `frame-extract` or `canvas-build` (not `none`)
- Branded-template entries reference valid template names
- All statuses are valid enum values

### Pacing Compliance (4 checks)
- Hook sections meet 15+ events/min target
- Intro sections meet 12-15 events/min target
- Body sections meet 7-10 events/min target
- No section has zero visual events

### Visual Asset Density (9 checks)
- D1: Talking head intro has ≥ 1 visual per 8s
- D2: Intro hook has ≥ 2 MGs in first 15s
- D3: No 15s+ speaker-only stretches in talking head intro
- D4: Total MG count meets minimum for intro duration
- D5: B-roll count ≥ 2 for intros > 45s
- D6: Body sections have visual break per 15s of speaker footage
- D7: Screen share sections have visual change per 15s
- D8: Talking head intro duration ≤ 90s (WARN if exceeded)
- D9: Talking head intro duration ≤ 120s (FAIL if exceeded)

### Production Readiness (4 checks)
- Status is APPROVED
- All stepsCompleted listed
- B-roll asset readiness summary
- Motion graphic asset readiness summary

### Visual Asset Density (9 checks — section-aware)

**Section identification:** Density gates require knowing which sections are "talking head intro" vs "screen share/agenda" vs "body". Use visual analysis frame classification as the primary signal — the transition from full-frame speaker to screen share/slides marks the intro boundary. Do NOT rely solely on script section labels.

**Gates D1–D5 apply to talking head intro sections only (high density):**

- **D1 (FAIL):** Talking head intro sections must have ≥ 1 B-roll or MG per 8 seconds of timeline
- **D2 (FAIL):** Intro hook (first 15s) must have ≥ 2 motion graphics (Type A or B)
- **D3 (FAIL):** Any section > 15s with zero B-roll or MG entries — no 15s+ speaker-only stretches
- **D4 (FAIL):** Total MG count for full talking head intro must be ≥ (intro_duration_seconds / 8)
- **D5 (FAIL):** B-roll extraction count must be ≥ 2 for talking head intros > 45s

**Gates D6 applies to body sections:**

- **D6 (FAIL):** Body sections: ≥ 1 visual break (B-roll, MG, or screen share) per 15s of speaker footage

**Caption density gate (body sections):**

- **D10 (WARN):** Body speaker segments with captions should average ≤ 1 caption burst per 10s of speaker footage. Most body speaker segments should have `captionText: null` — reserve captions for power moments only (numbers, tool names on first mention, key takeaway phrases, emotional hooks)

**Gates D7–D9 are section boundary checks:**

- **D7 (WARN):** Screen share/agenda sections should have ≥ 1 visual change per 15s (pan/zoom/highlight counts)
- **D8 (WARN):** Talking head intro > 90s — flag as potentially over-long
- **D9 (FAIL):** Talking head intro > 120s — almost certainly includes agenda content that should be separated
