---
name: 'step-02-scaffold'
description: 'Create Remotion project structure and copy templates from sidecar'

nextStepFile: './step-03-theme.md'
sidecarTemplatesPath: '{project-root}/_bmad/_memory/video-editor-sidecar/remotion-templates'
---

# Step 2: Scaffold Remotion Project

## STEP GOAL:

Create the Remotion project directory structure, initialize package.json and tsconfig, and copy the template `.tsx` files from the sidecar into the project's `src/` directory.

## MANDATORY EXECUTION RULES (READ FIRST):

### Universal Rules:

- CRITICAL: Read the complete step file before taking any action
- CRITICAL: When loading next step with 'C', ensure entire file is read
- YOU MUST ALWAYS SPEAK OUTPUT in your Agent communication style with the config `{communication_language}`

### Step-Specific Rules:

- This is an automated step — no user interaction
- Use the storyboard video-id as the composition name
- Copy ALL template files from sidecar — do not skip any

## MANDATORY SEQUENCE

### 1. Determine Project Path

Resolve the Remotion project directory:
- `{project_folder}/{project-slug}/video-editor/remotion/{composition-name}/`
- Where `{composition-name}` is derived from the video-id (kebab-case)

Create the directory structure:
```
{composition-name}/
├── package.json
├── tsconfig.json
├── src/
│   ├── Root.tsx          (generated in step 05)
│   ├── theme.ts          (generated in step 03)
│   ├── VideoRenderer.tsx  (copied from sidecar — generic segment dispatcher)
│   ├── ChapterCard.tsx    (copied from sidecar — branded chapter card)
│   ├── KineticCaption.tsx (copied from sidecar)
│   ├── Caption.tsx        (copied from sidecar)
│   ├── BRollOverlay.tsx   (copied from sidecar)
│   ├── SubtleZoom.tsx     (copied from sidecar)
│   └── SocialProofStack.tsx (copied from sidecar)
├── public/
│   ├── branded-assets/    (copied from sidecar)
│   │   ├── upwork-profile.png
│   │   └── apg-logo.png
│   └── (symlinks or copies of video assets)
└── qa-report.md          (generated in step 06)
```

### 2. Create package.json

```json
{
  "name": "{composition-name}",
  "version": "1.0.0",
  "private": true,
  "scripts": {
    "studio": "remotion studio src/index.ts",
    "render": "remotion render src/index.ts {CompositionId} out/{composition-name}.mp4 --codec h264 --crf 15 --gl=angle --hardware-acceleration if-possible",
    "build": "remotion render src/index.ts {CompositionId} out/{composition-name}.mp4 --codec h264 --crf 15 --concurrency=8 --gl=angle --hardware-acceleration if-possible"
  },
  "dependencies": {
    "@remotion/cli": "^4.0.432",
    "@remotion/player": "^4.0.432",
    "@remotion/renderer": "^4.0.432",
    "@remotion/preload": "^4.0.432",
    "react": "^18.0.0",
    "react-dom": "^18.0.0",
    "remotion": "^4.0.432"
  },
  "devDependencies": {
    "@types/react": "^18.0.0",
    "typescript": "^5.0.0"
  }
}
```

### 3. Create tsconfig.json

```json
{
  "compilerOptions": {
    "target": "ES2022",
    "module": "ESNext",
    "moduleResolution": "bundler",
    "jsx": "react-jsx",
    "strict": true,
    "esModuleInterop": true,
    "outDir": "dist",
    "rootDir": "src"
  },
  "include": ["src"]
}
```

### 4. Copy Sidecar Templates

Copy all `.tsx` files from {sidecarTemplatesPath} into the project's `src/` directory:

1. `KineticCaption.tsx`
2. `Caption.tsx`
3. `BRollOverlay.tsx`
4. `SubtleZoom.tsx`
5. `SocialProofStack.tsx`
6. `UpworkProfile.tsx` (branded template)
7. `AgencyBrand.tsx` (branded template)
8. `MotionGraphic.tsx`
9. `PiPSpeaker.tsx`
10. `WhiteFlash.tsx`
11. `VideoRenderer.tsx` (generic segment dispatcher — eliminates per-segment SegXX.tsx files)
12. `ChapterCard.tsx` (branded chapter transition card)

For each file copied, verify it exists at the destination.

**If sidecar templates directory is missing or empty:**
"WARNING: Sidecar templates not found at {sidecarTemplatesPath}. Template components will need to be created manually."

### 4b. Copy Showcase Components

Copy all `.tsx` files from `{project-root}/video-plugin/skills/2-remotion/references/template-showcase/src/components/` into `src/components/showcase/` (create the directory if it doesn't exist):

```bash
mkdir -p src/components/showcase
cp {project-root}/video-plugin/skills/2-remotion/references/template-showcase/src/components/*.tsx src/components/showcase/
```

These components are the default for all `showcase-mg` segments in long-form and VSL videos. Verify the directory contains the expected files (BoldStatement, ChecklistReveal, NumberCountUp, FlowchartAnimation, ToolLogoGrid, etc.).

**If showcase directory is missing:**
"WARNING: Showcase components not found at {showcase_path}. All `showcase-mg` segments will fail to render. Ensure `video-plugin` is installed and the template-showcase project exists."

### 5. Copy Branded Assets

Copy all files from `{project-root}/_bmad/_memory/video-editor-sidecar/branded-assets/` into `public/branded-assets/`:
- `upwork-profile.png`
- `apg-logo.png`
- Any other brand images present

**If branded assets folder is missing or empty:**
"WARNING: Branded assets not found. UpworkProfile and AgencyBrand templates will not render correctly. Add images to `_bmad/_memory/video-editor-sidecar/branded-assets/`."

### 6. Link Video Assets

**CRITICAL: Use hardlinks, not symlinks.** Remotion's webpack dev server does not serve symlinked media files with HTTP Range headers, causing `media-playback-error` in Studio.

For each video file referenced in the storyboard (source video, B-roll clips, motion graphics):

```bash
# Hardlink (zero disk cost, same inode, dev server serves correctly)
ln "{absolute_source_path}" "{project_path}/public/{filename}"

# If hardlink fails (cross-filesystem), fall back to copy:
cp "{absolute_source_path}" "{project_path}/public/{filename}"
```

Verify each file in `public/` is NOT a symlink:
```bash
ls -la public/*.mp4  # should show link count ≥ 2, NOT lrwxr-xr-x
```

### 7. Create Remotion Entrypoint

Create `src/index.ts` — required for `npx remotion studio src/index.ts`:

```typescript
import { registerRoot } from 'remotion';
import { RemotionRoot } from './Root';

registerRoot(RemotionRoot);
```

This file must be created at scaffold time (not deferred to step 05) so Remotion Studio can be launched correctly.

### 8. Auto-Proceed

"**Remotion Project Scaffolded**

- Project: {composition-name}/
- Sidecar templates copied: {count}/12 (9 standard + 2 branded + 1 renderer)
- Showcase components copied: {showcase_count} files → src/components/showcase/
- Video assets hardlinked: {asset_count} (no symlinks)

Proceeding to theme generation..."

Load, read entire file, then execute {nextStepFile}.

---

## SYSTEM SUCCESS/FAILURE METRICS

### SUCCESS:

- Project directory created with correct structure
- package.json and tsconfig.json created
- All 12 sidecar templates copied to src/ (9 standard + 2 branded + 1 renderer)
- Showcase components copied to src/components/showcase/ (all .tsx files from template-showcase)
- Branded assets copied to public/branded-assets/
- Video assets hardlinked (NOT symlinked) in public/
- src/index.ts created with registerRoot

### FAILURE:

- Missing any sidecar template without warning
- Not creating src/components/showcase/ or missing showcase component files
- Incorrect project structure
- Not creating package.json or tsconfig.json
- Using symlinks instead of hardlinks for video assets (causes media-playback-error in Studio)
- Missing src/index.ts (Studio cannot launch without entrypoint)
