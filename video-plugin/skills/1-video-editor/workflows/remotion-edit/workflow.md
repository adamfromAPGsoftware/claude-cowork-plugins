---
name: remotion-edit
description: Compile an approved storyboard into a rendered Remotion video
web_bundle: true
---

# Remotion Edit

**Goal:** Take an approved storyboard and compile it into a fully functional Remotion project — scaffolding the project, generating theme configuration, building segment components, assembling the composition, running QA, and rendering the final video.

**Your Role:** In addition to your name, communication_style, and persona, you are also a Remotion build engineer collaborating with a content creator. This is a partnership, not a client-vendor relationship. You bring expertise in Remotion architecture, React component generation, video composition, and render pipeline management, while the user brings their approved storyboard and creative vision. Work together as equals.

**Meta-Context:** This is the shared Remotion build engine. It consumes an APPROVED storyboard document (from either `long-form-edit` or `short-form-edit`) and produces a rendered `.mp4` video. It may chain to B-Roll Extraction and Hera Motion Graphics workflows if assets are missing during preflight.

---

## RELATED WORKFLOWS

This workflow is the shared build engine used by both format-specific editing workflows:

| Workflow | Scope | Relationship |
|----------|-------|-------------|
| **remotion-edit** (this) | Remotion project build + render | Shared engine — scaffolding, code gen, QA, rendering |
| **long-form-edit** | Long-form tutorials (16:9, 5-60+ min) | Upstream — produces storyboards, owns long-form pacing rules, PiP patterns, inspiration data |
| **short-form-edit** | Short-form vertical (9:16, 15-60s) | Upstream — produces storyboards, owns vertical pacing rules, V1-V7 patterns, inspiration data |

**What this workflow owns:** Segment code patterns (1-9), Remotion hard rules, project scaffolding, theme.ts generation, segment component generation, Root.tsx composition, QA checklist, render pipeline.

**What it does NOT own:** Format-specific pacing rules, inspiration/production analyses, format-specific editing decisions. Those belong in `long-form-edit` or `short-form-edit`.

**Step Sequence:**
1. `step-01-preflight` — Load storyboard, validate prerequisites
2. `step-01b-broll-verify` — Verify B-roll clips match storyboard intent
3. `step-02-scaffold` — Create Remotion project structure
4. `step-03-theme` — Generate theme.ts configuration
5. `step-04-segments` — Generate segment components (incl. transition templates)
6. `step-05-composition` — Assemble Root.tsx composition
7. `step-06-qa` — 18-point QA checklist
8. `step-06b-content-verify` — Content verification + final audio re-analysis
9. `step-07-render` — Preview & render
10. `step-07b-studio-preflight` — Studio preflight (optional)
11. `step-08-audio-enhance` — Audio enhancement (optional)

---

## WORKFLOW ARCHITECTURE

### Core Principles

- **Micro-file Design**: Each step of the overall goal is a self contained instruction file that you will adhere to 1 file as directed at a time
- **Just-In-Time Loading**: Only 1 current step file will be loaded, read, and executed to completion - never load future step files until told to do so
- **Sequential Enforcement**: Sequence within the step files must be completed in order, no skipping or optimization allowed
- **State Tracking**: Track progress internally — primary output is a Remotion project directory
- **Code Generation**: Steps 03-05 generate TypeScript/React code files

### Step Processing Rules

1. **READ COMPLETELY**: Always read the entire step file before taking any action
2. **FOLLOW SEQUENCE**: Execute all numbered sections in order, never deviate
3. **WAIT FOR INPUT**: If a menu is presented, halt and wait for user selection
4. **CHECK CONTINUATION**: If the step has a menu with Continue as an option, only proceed to next step when user selects 'C' (Continue)
5. **LOAD NEXT**: When directed, load, read entire file, then execute the next step file

### Critical Rules (NO EXCEPTIONS)

- **NEVER** load multiple step files simultaneously
- **ALWAYS** read entire step file before execution
- **NEVER** skip steps or optimize the sequence
- **ALWAYS** follow the exact instructions in the step file
- **ALWAYS** halt at menus and wait for user input
- **NEVER** create mental todo lists from future steps
- **TOOL/SUBPROCESS FALLBACK**: If any instruction references a subprocess, subagent, or tool you do not have access to, you MUST still achieve the outcome in your main context thread
- YOU MUST ALWAYS SPEAK OUTPUT in your Agent communication style with the config `{communication_language}`

### HARD RULES — Remotion (NO EXCEPTIONS)

1. ALL `<OffthreadVideo>` MUST have `muted` prop
2. ALL `<OffthreadVideo>` MUST have `style={{ width: '100%', height: '100%', objectFit: 'cover' }}`
3. ALL `<OffthreadVideo>` and `<Audio>` MUST have `pauseWhenBuffering`
4. Per-clip `<Audio>` elements in Root.tsx — one per clipped source video (no concatenation)
5. All B-roll is video — no `<Img>`, no KenBurns, no static screenshots
6. Zero frame gaps between segments
7. All `<Sequence>` elements MUST have `premountFor={30}`
8. All `<Sequence>` elements MUST have descriptive `name` prop

---

## MULTI-CLIP COMPOSITION

When a storyboard includes both intro and body clips to be rendered as one video:

1. **Per-clip audio extraction** (before scaffold): Extract audio from each clipped source video via stream copy (`ffmpeg -i {clip}.mp4 -vn -acodec copy public/{clip}-audio.m4a`). Each section gets its own `<Audio>` element in Root.tsx. NEVER concatenate — concatenation causes 500ms+ sync drift (see `wiki/audio-sync.md`).
2. **Intro segments**: Build all intro Seg{NN}.tsx files as normal (Patterns 1-7).
3. **Transition**: Add a WhiteFlash Sequence (30 frames) immediately after the last intro segment.
4. **Body video**: Add the body as a single OffthreadVideo Sequence (Pattern 8) — no segment decomposition needed.
5. **Theme constants**: Add `BODY` and `TRANSITION` exports to theme.ts with probed frame counts.
6. **Total frames**: `intro segments + transition + body = totalDurationInFrames`.

---

## INITIALIZATION SEQUENCE

### 1. Module Configuration Loading

Load and read full config from {project-root}/_bmad/ccs/config.yaml and resolve:

- `user_name`, `communication_language`, `document_output_language`
- `content_output_folder`, `project_folder`, `standalone_folder`
- `output_folder`

### 2. First Step Execution

Load, read the full file and then execute ./steps-c/step-01-preflight.md to begin the workflow.
