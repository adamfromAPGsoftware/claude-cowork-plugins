---
name: 'step-05-composition'
description: 'Generate Root.tsx with single Audio element, Sequences with premountFor={30}'

nextStepFile: './step-06-qa.md'
---

# Step 5: Generate Composition (Root.tsx)

## STEP GOAL:

Generate the `Root.tsx` composition file that assembles all segments into a single Remotion composition with exactly ONE `<Audio>` element and all `<Sequence>` wrappers with `premountFor={30}` and descriptive `name` props.

## MANDATORY EXECUTION RULES (READ FIRST):

### Universal Rules:

- CRITICAL: Read the complete step file before taking any action
- CRITICAL: When loading next step with 'C', ensure entire file is read
- YOU MUST ALWAYS SPEAK OUTPUT in your Agent communication style with the config `{communication_language}`

### Step-Specific Rules:

- This is an automated step — no user interaction
- Exactly ONE `<Audio>` element in the entire composition
- EVERY `<Sequence>` must have `premountFor={30}`
- EVERY `<Sequence>` must have a descriptive `name` prop
- Zero frame gaps between sequences

## MANDATORY SEQUENCE

### 1. Build Imports

Import all generated segment components and Remotion modules:

```typescript
import { Composition, Sequence, Audio } from 'remotion';
import { OffthreadVideo } from '@remotion/media-utils';
import { PROJECT, SEGMENTS } from './theme';
import { Seg01 } from './Seg01';
import { Seg02 } from './Seg02';
// ... all segments
```

**VideoRenderer mode (preferred):** If `VideoRenderer.tsx` exists in the project, use simplified imports:

```typescript
import React, { useEffect } from 'react';
import { Composition, Sequence, Audio, AbsoluteFill } from 'remotion';
import { preloadVideo } from '@remotion/preload';
import { PROJECT, SEGMENTS } from './theme';
import { SegmentRenderer } from './VideoRenderer';
import type { Segment } from './VideoRenderer';
```

No per-segment imports needed.

**Video preloading (add inside Main component):**
```typescript
useEffect(() => {
  // Preload the main speaker video to reduce seek delays at segment boundaries
  const unpreload = preloadVideo(PROJECT.sourceFile);
  return () => unpreload();
}, []);
```

The sequence chain becomes:

```typescript
{(SEGMENTS as unknown as Segment[]).map((seg, i) => (
  <Sequence
    key={seg.id}
    from={seg.startFrame}
    durationInFrames={seg.durationInFrames}
    premountFor={30}
    name={`${seg.section} - ${seg.template}`}
  >
    {seg.visualType === 'transition' ? (
      <AbsoluteFill>
        <SegmentRenderer segment={seg} />
      </AbsoluteFill>
    ) : (
      <SegmentRenderer segment={seg} />
    )}
  </Sequence>
))}
```

This replaces the manual segment-by-segment Sequence chain. Same rules apply: zero frame gaps, premountFor={30}, descriptive names, single Audio element.

### 2. Build Audio Element

Exactly ONE `<Audio>` element using the audio source from theme.ts. Accept `audioOffsetMs` from input props and convert to frames:

```typescript
const { audioOffsetMs } = props;
const audioOffsetFrames = Math.round((audioOffsetMs / 1000) * PROJECT.fps);

{audioOffsetFrames > 0 ? (
  <Sequence from={audioOffsetFrames} name="Audio Offset">
    <Audio src={PROJECT.audioSource} pauseWhenBuffering />
  </Sequence>
) : (
  <Audio src={PROJECT.audioSource} pauseWhenBuffering />
)}
```

**CRITICAL:** This is the ONLY `<Audio>` element in the entire project. No segment component may contain an `<Audio>` tag. The `audioOffsetMs` prop is adjustable live in Remotion Studio's sidebar — tweak until lip sync matches, then render.

### 3. Build Sequence Chain

For each segment, wrap in a `<Sequence>` with:
- `from={segment.startFrame}` — absolute frame position
- `durationInFrames={segment.durationInFrames}`
- `premountFor` — MANDATORY on every Sequence. Use `premountFor={60}` for long-form compositions (total duration > 60s at composition FPS) to give the browser more buffer time for video seeks. Use `premountFor={30}` for short-form (≤60s).
- `name={descriptive_name}` — e.g., "Hook - Speaker with SubtleZoom"

```typescript
<Sequence
  from={SEGMENTS[0].startFrame}
  durationInFrames={SEGMENTS[0].durationInFrames}
  premountFor={30}
  name="Hook - Speaker SubtleZoom"
>
  <Seg01 />
</Sequence>
```

**CRITICAL:** Verify zero frame gaps:
- Segment N's `from` + `durationInFrames` MUST equal Segment N+1's `from`

### 4. Build Composition Registration

```typescript
export const RemotionRoot: React.FC = () => {
  return (
    <>
      <Composition
        id={PROJECT.compositionId}
        component={Main}
        durationInFrames={PROJECT.totalDurationInFrames}
        fps={PROJECT.fps}
        width={PROJECT.width}
        height={PROJECT.height}
        defaultProps={{ audioOffsetMs: PROJECT.audioOffsetMs }}
      />
    </>
  );
};
```

**CRITICAL:** The `defaultProps` exposes `audioOffsetMs` as an editable number field in the Remotion Studio sidebar UI. This is how the user adjusts lip sync live during preview.

### 5. Write Root.tsx

Assemble the complete file and write to `{project_path}/src/Root.tsx`.

### 6. Self-Validate Root.tsx

**Mandatory checks:**
- [ ] Exactly ONE `<Audio>` element (count occurrences)
- [ ] `<Audio>` has `pauseWhenBuffering`
- [ ] Every `<Sequence>` has `premountFor` (30 for short-form ≤60s, 60 for long-form >60s)
- [ ] Every `<Sequence>` has `name` prop
- [ ] Zero frame gaps between sequences
- [ ] Total frames = sum of all sequence durations
- [ ] All segment imports present
- [ ] If audioOffsetMs > 0, Audio wrapped in Sequence with correct from value
- [ ] audioOffsetMs exposed via defaultProps on Composition

**If any violation found:** Fix immediately.

### 7. Auto-Proceed

"**Composition Generated — Root.tsx**

- Audio elements: 1 (single source)
- Sequences: {count}
- Total frames: {total}
- Frame gap check: {pass/fail}
- All premountFor={30}: verified
- All name props: verified

Proceeding to QA..."

Load, read entire file, then execute {nextStepFile}.

---

## SYSTEM SUCCESS/FAILURE METRICS

### SUCCESS:

- Exactly ONE `<Audio>` element
- Every `<Sequence>` has `premountFor={30}` and descriptive `name`
- Zero frame gaps
- All segment imports present
- Root.tsx written to project src/

### FAILURE:

- Multiple `<Audio>` elements
- Missing `premountFor={30}` on any Sequence
- Missing `name` prop on any Sequence
- Frame gaps between sequences
- Audio in segment files instead of Root.tsx

**Master Rule:** ONE Audio. premountFor on EVERY Sequence (30 short-form, 60 long-form). Zero gaps. Preload main video via `@remotion/preload`.
