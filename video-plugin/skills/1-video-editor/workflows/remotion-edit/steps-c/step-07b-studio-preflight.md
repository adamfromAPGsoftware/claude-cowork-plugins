---
name: 'step-07b-studio-preflight'
description: 'Diagnose and fix Remotion Studio media playback issues before launch'
---

# Step 7b: Studio Preflight — Media Playback Diagnostic

## STEP GOAL:

Before launching Remotion Studio, run a series of diagnostic checks that catch the most common causes of `media-playback-error` and blank composition renders. Fix any issues automatically. Only proceed to Studio launch after all checks pass.

## MANDATORY EXECUTION RULES (READ FIRST):

### Universal Rules:

- CRITICAL: Read the complete step file before taking any action
- This is an automated step — no user interaction unless a check cannot be auto-fixed
- All checks must be run and logged, even if earlier ones fail
- Fix all auto-fixable issues before reporting results

---

## MANDATORY SEQUENCE

### Check 1: Entrypoint Exists

Verify `src/index.ts` exists in the project root:

```bash
ls {project_path}/src/index.ts
```

**If missing:** Create it:
```typescript
import { registerRoot } from 'remotion';
import { RemotionRoot } from './Root';

registerRoot(RemotionRoot);
```

**Status:** PASS / FIXED / FAIL

---

### Check 2: No Symlinks in public/

Scan `public/` for symlinks — Remotion's webpack dev server does not serve symlinked media with HTTP Range headers, causing `media-playback-error` in the browser.

```bash
find {project_path}/public -maxdepth 2 -type l
```

**If symlinks found:** Replace each with a hardlink:
```bash
target=$(readlink "{symlink_path}")
rm "{symlink_path}"
ln "$target" "{symlink_path}" || cp "$target" "{symlink_path}"
```

Re-verify with `ls -la public/*.mp4` — link count must be ≥ 2 (hardlink), NOT `lrwxr-xr-x` (symlink).

**Status:** PASS / FIXED ({count} symlinks replaced) / FAIL

---

### Check 3: Video Codec Compatibility

Remotion Studio uses the browser's HTML5 video decoder. Only H.264 (avc1) is universally supported.

For each `.mp4` in `public/`:
```bash
ffprobe -v error -select_streams v:0 \
  -show_entries stream=codec_name,codec_tag_string \
  -of csv=p=0 "{file}"
```

**Compatible:** `h264`, `avc1`
**Incompatible (needs transcode):** `hevc`, `hvc1`, `vp9`, `av1`, `mpeg4`

**If incompatible codec found:** Transcode to H.264:
```bash
# Hardware-accelerated transcode (Mac Studio M4 Max — Apple VideoToolbox)
ffmpeg -y -i "{input}" -c:v h264_videotoolbox -q:v 80 \
  -c:a aac -b:a 192k "{output_h264.mp4}"
# Replace the original in public/
mv "{output_h264.mp4}" "{input}"
```

**Status:** PASS / FIXED ({count} files transcoded) / FAIL

---

### Check 4: File Permissions

All media files in `public/` must be readable by the current user:

```bash
for f in {project_path}/public/**/*.{mp4,png,jpg,webp}; do
  [[ -r "$f" ]] || echo "UNREADABLE: $f"
done
```

**If unreadable files found:** `chmod 644 {file}`

**Status:** PASS / FIXED / FAIL

---

### Check 5: Port 3000 Available

Remotion Studio defaults to port 3000. Check if it's already in use:

```bash
lsof -ti:3000
```

**If port in use:** Check if it's a stale Remotion process from a previous session:
```bash
lsof -ti:3000 | xargs ps -p 2>/dev/null | grep -i remotion
```

- If stale Remotion process: `pkill -f "remotion studio"` then re-check
- If another process: Report the PID and suggest `npx remotion studio --port 3001`

**Status:** PASS / FIXED (stale process killed) / BLOCKED (port {N} in use by {process})

---

### Check 6: node_modules Installed

Verify `node_modules/remotion` exists:

```bash
ls {project_path}/node_modules/remotion/package.json
```

**If missing:** Run `npm install` in the project directory.

**Status:** PASS / FIXED (ran npm install) / FAIL

---

### Check 7: Remotion Version ≥4.0.432

Remotion `4.0.0` does NOT include Chrome Headless Shell — it is only bundled/auto-downloaded starting from `~4.0.100+`. Versions below `4.0.432` will fail silently with "got no response" on the first render frame.

```bash
node -e "
  const v = require('./node_modules/remotion/package.json').version;
  const [major, minor, patch] = v.split('.').map(Number);
  console.log('Remotion version:', v);
  if (major < 4 || (major === 4 && minor === 0 && patch < 432)) {
    console.log('OUTDATED');
    process.exit(1);
  } else {
    console.log('OK');
  }
"
```

**If outdated (exit code 1):** Upgrade all Remotion packages:
```bash
cd {project_path} && npm install remotion@^4.0.432 @remotion/cli@^4.0.432 @remotion/renderer@^4.0.432 @remotion/player@^4.0.432
```

Re-run the version check to confirm upgrade succeeded.

**Status:** PASS / FIXED (upgraded to {new_version}) / FAIL

---

## Report & Proceed

Print a preflight summary:

```
Studio Preflight — {composition-name}
──────────────────────────────────────
✓ Check 1: Entrypoint src/index.ts    PASS
✓ Check 2: No symlinks in public/     FIXED (6 symlinks → hardlinks)
✓ Check 3: Video codec compatibility  PASS (all h264)
✓ Check 4: File permissions           PASS
✓ Check 5: Port 3000 available        PASS
✓ Check 6: node_modules installed     PASS
✓ Check 7: Remotion version ≥4.0.432  PASS (4.0.432)
──────────────────────────────────────
All checks passed. Launching Studio...
```

**If all checks PASS or FIXED:**
- Auto-proceed to Studio launch
- Command: `npx remotion studio src/index.ts`

**If any check FAIL (cannot auto-fix):**
- Display the failure with specific remediation steps
- Wait for user to resolve, then re-run preflight
- Do NOT launch Studio with unresolved failures

---

## SYSTEM SUCCESS/FAILURE METRICS

### SUCCESS:

- All 7 checks pass or auto-fixed
- Studio launches without media-playback-error
- Browser can seek through video files (Content-Range headers served correctly)

### FAILURE:

- Launching Studio with symlinked media files
- Launching Studio with incompatible video codecs
- Launching Studio without src/index.ts entrypoint
- Skipping preflight and going directly to `npx remotion studio`
