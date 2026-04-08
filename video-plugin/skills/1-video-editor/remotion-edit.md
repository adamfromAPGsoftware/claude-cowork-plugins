---
name: remotion-edit
description: Compile approved storyboard to final video via Remotion
menu-code: RE
---

# [RE] Remotion Edit

**Goal:** Take an approved storyboard and compile it into a fully functional Remotion project — scaffolding, theme configuration, segment components, composition assembly, QA, and rendering.

**Role:** Remotion build engineer. Expertise in Remotion architecture, React component generation, video composition, and render pipeline management.

---

## HARD RULES (NO EXCEPTIONS)

1. ALL `<OffthreadVideo>` MUST have `muted` prop
2. ALL `<OffthreadVideo>` MUST have `style={{ width: '100%', height: '100%', objectFit: 'cover' }}`
3. ALL `<OffthreadVideo>` and `<Audio>` MUST have `pauseWhenBuffering`
4. One `<Audio>` element PER video clip — extract audio from each proxy separately, place each in its own `<Sequence>` matching the video timing. Use the same `startFrom` on both Audio and OffthreadVideo. NEVER concatenate audio files.
5. All B-roll is video — no `<Img>`, no KenBurns, no static screenshots
6. Zero frame gaps between segments
7. All `<Sequence>` elements MUST have `premountFor={30}`
8. All `<Sequence>` elements MUST have descriptive `name` prop

---

## Multi-Clip Composition

When storyboard includes both intro and body clips:
1. **Separate audio tracks:** Extract audio from each proxy independently (`ffmpeg -i proxy.mp4 -vn -c:a aac -b:a 128k audio.m4a`). One `<Audio>` per clip inside its own `<Sequence>`, with the same `startFrom` as the video. NEVER concatenate audio files.
2. **Intro segments:** Full Remotion segment decomposition (Patterns 1-7)
3. **Transition:** WhiteFlash Sequence (12 frames) after last intro segment
4. **Body video:** Single OffthreadVideo Sequence (Pattern 8)
5. **Theme constants:** BODY and TRANSITION exports in theme.ts
6. **Total frames:** intro segments + transition + body

---

## Step 1: Preflight

Load approved storyboard. Validate all referenced assets exist (B-roll clips, MG files, audio). Check format (16:9 or 9:16). Verify clipped transcript JSON available for caption sync.

## Step 1b: B-Roll Verify

Verify each B-roll clip matches storyboard intent. If Gemini available, spot-check 1 frame per clip against description. Re-extract if mismatch.

## Step 2: Scaffold

Create Remotion project directory structure:
- `src/` — components and composition
- `public/` — video assets, audio, MG clips
- `remotion.config.ts` — Remotion configuration

Copy required assets to `public/`. Configure `package.json` with Remotion dependencies.

## Step 3: Theme

Generate `theme.ts` with:
- Color palette from storyboard brand settings
- Timing constants (segment frame counts from storyboard)
- Typography settings
- BODY and TRANSITION constants (multi-clip mode)

## Step 4: Segments

Generate TypeScript segment components (Seg01.tsx, Seg02.tsx, etc.) using Patterns 1-9:
- **Pattern 1-7:** Various visual overlay patterns (MG, B-roll, captions, PiP, zoom)
- **Pattern 8:** Body passthrough (single OffthreadVideo)
- **Pattern 9:** PiP Speaker (talking head + screen share)

Include transition template support between segments.

## Step 5: Composition

Assemble `Root.tsx` composition:
- Import all segment components
- Single `<Audio>` element at composition level
- `<Sequence>` chain with zero gaps and `premountFor={30}`
- Total duration from theme.ts constants

## Step 6: QA (18-Point Checklist)

1. Every OffthreadVideo has `muted`
2. Every OffthreadVideo has correct style
3. Every OffthreadVideo/Audio has `pauseWhenBuffering`
4. Exactly one Audio element
5. All B-roll is video (no Img)
6. Zero frame gaps
7. All Sequences have `premountFor={30}`
8. All Sequences have descriptive `name`
9. Theme.ts exports match segment count
10. All asset paths resolve
11. Caption sync matches clipped transcript timestamps
12. No TypeScript errors
13. Total frames match expected duration
14. Transitions present between sections
15. MG clips referenced correctly
16. B-roll clips referenced correctly
17. Audio file path correct
18. Configuration matches target format (fps, resolution, codec)

## Step 6b: Content Verify

Content verification pass + final audio re-analysis if needed.

## Step 7: Render

Preview in Remotion Studio. When approved:
```bash
npx remotion render src/index.tsx {composition-id} {output_path}
```

## Step 7b: Studio Preflight (Optional)

Optional pre-render check in Remotion Studio for visual verification.

## Step 8: Audio Enhancement (Optional)

Post-render audio normalization and enhancement if needed.
