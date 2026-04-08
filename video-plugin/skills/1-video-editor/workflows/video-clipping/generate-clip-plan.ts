/**
 * Deterministic Clip Plan Generator — Audio-Only Cleanup
 *
 * Takes audio-analysis.json, applies gap handling rules (silence, breaths,
 * fillers, noise), and generates FFmpeg commands. No LLM needed — fully
 * deterministic. Does NOT handle false starts/retakes — that requires
 * language understanding and is handled by the workflow agent.
 *
 * Usage:
 *   npx tsx generate-clip-plan.ts \
 *     --analysis <audio-analysis.json> \
 *     --video <source-video.mp4> \
 *     --type intro|main \
 *     [--output <clip-plan.md>] \
 *     [--execute]
 */

import { readFileSync, writeFileSync, existsSync, statSync } from 'node:fs';
import { resolve, dirname, join, basename, extname } from 'node:path';
import { execSync } from 'node:child_process';

// --- Types ---
interface ClassifiedRegion {
  startMs: number;
  endMs: number;
  durationMs: number;
  classification: 'SPEECH' | 'SILENCE' | 'BREATH' | 'NOISE';
  confidence: number;
  avgDb: number;
  vadProb: number;
}

interface FillerRegion {
  startMs: number;
  endMs: number;
  durationMs: number;
  word: string;
}

interface BoundaryPoint {
  timeMs: number;
  rmsDbfs: number;
  peakDbfs: number;
  vadProb: number;
}

interface BoundaryDetail {
  regionIdx: number;
  startMs: number;
  endMs: number;
  durationMs: number;
  onset: BoundaryPoint[];
  offset: BoundaryPoint[];
}

interface AudioMetadata {
  duration_ms: number;
  overall_rms_dbfs: number;
  peak_dbfs: number;
  noise_floor_dbfs: number;
  dynamic_range_db: number;
  total_speech_ms: number;
  total_silence_ms: number;
  total_breath_ms: number;
  total_noise_ms: number;
}

interface AnalysisJson {
  source_file: string;
  source_path: string;
  content_type: string;
  denoised: boolean;
  audio_metadata: AudioMetadata;
  classified_regions: ClassifiedRegion[];
  speech_boundary_detail: BoundaryDetail[];
  filler_regions: FillerRegion[];
}

interface KeepSegment {
  startMs: number;
  endMs: number;
  durationMs: number;
  source: string;
}

interface GapAction {
  startMs: number;
  endMs: number;
  classification: string;
  action: 'CUT' | 'COMPRESS' | 'KEEP' | 'TRIM';
  originalDurationMs: number;
  resultDurationMs: number;
  savedMs: number;
}

// --- Content-type-specific thresholds ---
const THRESHOLDS = {
  intro: {
    buffer_ms: 150,
    silence_cut_threshold_ms: 1000,       // Cut silences >= 1s
    silence_compress_min_ms: 300,          // Compress silences 300ms-999ms
    silence_compress_target_ms: 150,       // Compress to 150ms
    silence_keep_max_ms: 300,              // Keep silences < 300ms
    breath_cut_threshold_ms: 100,          // Cut breaths >= 100ms
    breath_adjacent_keep_ms: 100,          // Keep breaths < 100ms if adjacent to speech
    filler_always_cut: true,               // Always cut fillers in intros
    min_keep_segment_ms: 80,              // Minimum viable keep segment
  },
  main: {
    buffer_ms: 300,
    silence_cut_threshold_ms: 2000,        // Cut silences >= 2s
    silence_compress_min_ms: 500,          // Compress silences 500ms-1999ms
    silence_compress_target_ms: 300,       // Compress to 300ms
    silence_keep_max_ms: 500,              // Keep silences < 500ms
    breath_cut_threshold_ms: 999999,       // Don't cut breaths in main (trim instead)
    breath_trim_target_ms: 150,            // Trim breaths to 150ms
    filler_always_cut: false,              // Only cut isolated fillers in main
    filler_isolation_gap_ms: 200,          // Gap required on at least one side
    min_keep_segment_ms: 100,             // Minimum viable keep segment
  },
  short: {
    buffer_ms: 100,
    silence_cut_threshold_ms: 300,         // Cut silences >= 300ms (aggressive)
    silence_compress_min_ms: 100,          // Compress silences 100ms-299ms
    silence_compress_target_ms: 50,        // Compress to 50ms
    silence_keep_max_ms: 100,              // Keep silences < 100ms
    breath_cut_threshold_ms: 80,           // Cut breaths >= 80ms
    breath_adjacent_keep_ms: 50,           // Keep breaths < 50ms if adjacent to speech
    filler_always_cut: true,               // Always cut fillers in short-form
    min_keep_segment_ms: 50,               // Minimum viable keep segment
  },
};

// --- CLI Args ---
function parseArgs() {
  const args = process.argv.slice(2);
  const get = (flag: string): string | undefined => {
    const idx = args.indexOf(flag);
    if (idx === -1 || idx + 1 >= args.length) return undefined;
    return args[idx + 1];
  };
  const has = (flag: string): boolean => args.includes(flag);

  const analysisPath = get('--analysis');
  const videoPath = get('--video');
  const contentType = (get('--type') ?? 'main') as 'intro' | 'main' | 'short';

  if (!analysisPath || !videoPath) {
    console.error('Usage: npx tsx generate-clip-plan.ts --analysis <json> --video <video> --type intro|main|short [--output <md>] [--execute] [--no-audio-enhance]');
    process.exit(1);
  }

  return {
    analysis: resolve(analysisPath),
    video: resolve(videoPath),
    contentType,
    output: get('--output') ? resolve(get('--output')!) : join(dirname(resolve(videoPath)), `${basename(videoPath, extname(videoPath))}-clip-plan.md`),
    execute: has('--execute'),
    audioEnhance: !has('--no-audio-enhance'),
  };
}

// --- Speech quality filters ---
function filterSpeechRegions(regions: ClassifiedRegion[]): { kept: ClassifiedRegion[]; discarded: ClassifiedRegion[] } {
  const kept: ClassifiedRegion[] = [];
  const discarded: ClassifiedRegion[] = [];

  const speechRegions = regions.filter(r => r.classification === 'SPEECH');

  for (const region of speechRegions) {
    // Min duration: 200ms
    if (region.durationMs < 200) {
      discarded.push(region);
      continue;
    }
    // Min confidence: 0.75
    if (region.confidence < 0.75) {
      discarded.push(region);
      continue;
    }
    // Energy floor: -35dB
    if (region.avgDb < -35) {
      discarded.push(region);
      continue;
    }
    // Isolated segment check: no adjacent speech within 500ms AND duration < 300ms
    if (region.durationMs < 300) {
      const hasNeighbor = speechRegions.some(
        other => other !== region &&
          (Math.abs(other.endMs - region.startMs) <= 500 || Math.abs(region.endMs - other.startMs) <= 500)
      );
      if (!hasNeighbor) {
        discarded.push(region);
        continue;
      }
    }
    kept.push(region);
  }

  return { kept, discarded };
}

// --- Apply speech boundary precision ---
function applyBoundaryPrecision(
  speechRegions: ClassifiedRegion[],
  boundaryDetail: BoundaryDetail[],
  totalDurationMs: number,
  bufferMs: number,
): { trimInMs: number; trimOutMs: number } {
  if (speechRegions.length === 0) return { trimInMs: 0, trimOutMs: totalDurationMs };

  const firstSpeech = speechRegions[0];
  const lastSpeech = speechRegions[speechRegions.length - 1];

  // Find boundary detail for first and last speech regions
  let speechStartMs = firstSpeech.startMs;
  let speechEndMs = lastSpeech.endMs;

  if (boundaryDetail.length > 0) {
    const firstBd = boundaryDetail[0];
    // Find onset point where VAD rises above 0.4 and RMS above -40
    for (const p of firstBd.onset) {
      if (p.vadProb > 0.4 && p.rmsDbfs > -40) {
        speechStartMs = p.timeMs;
        break;
      }
    }

    const lastBd = boundaryDetail[boundaryDetail.length - 1];
    // Find offset point where VAD drops below 0.4
    const offsets = [...lastBd.offset].reverse();
    for (const p of offsets) {
      if (p.vadProb > 0.4 && p.rmsDbfs > -40) {
        speechEndMs = p.timeMs;
        break;
      }
    }
  }

  const trimInMs = Math.max(0, speechStartMs - bufferMs);
  const trimOutMs = Math.min(totalDurationMs, speechEndMs + bufferMs);

  return { trimInMs, trimOutMs };
}

// --- Apply gap handling rules ---
function applyGapHandling(
  regions: ClassifiedRegion[],
  fillerRegions: FillerRegion[],
  trimInMs: number,
  trimOutMs: number,
  contentType: 'intro' | 'main' | 'short',
): { keepSegments: KeepSegment[]; gapActions: GapAction[] } {
  const t = THRESHOLDS[contentType];
  const gapActions: GapAction[] = [];

  // Build a list of filler time ranges for cross-referencing
  const fillerRanges = fillerRegions.map(f => ({ startMs: f.startMs, endMs: f.endMs, word: f.word }));

  // Process each region within trim boundaries
  const activeRegions = regions.filter(r => r.endMs > trimInMs && r.startMs < trimOutMs);
  const keepIntervals: Array<{ startMs: number; endMs: number }> = [];

  for (const region of activeRegions) {
    const regionStart = Math.max(region.startMs, trimInMs);
    const regionEnd = Math.min(region.endMs, trimOutMs);
    const regionDuration = regionEnd - regionStart;

    if (region.classification === 'SPEECH') {
      // Check for filler words within this speech region
      const fillersInRegion = fillerRanges.filter(
        f => f.startMs >= regionStart && f.endMs <= regionEnd
      );

      if (fillersInRegion.length > 0 && shouldCutFillers(fillersInRegion, region, regions, contentType)) {
        // Split speech region around fillers
        let pos = regionStart;
        for (const filler of fillersInRegion) {
          if (filler.startMs > pos) {
            keepIntervals.push({ startMs: pos, endMs: filler.startMs });
          }
          gapActions.push({
            startMs: filler.startMs,
            endMs: filler.endMs,
            classification: `FILLER(${filler.word})`,
            action: 'CUT',
            originalDurationMs: filler.endMs - filler.startMs,
            resultDurationMs: 0,
            savedMs: filler.endMs - filler.startMs,
          });
          pos = filler.endMs;
        }
        if (pos < regionEnd) {
          keepIntervals.push({ startMs: pos, endMs: regionEnd });
        }
      } else {
        keepIntervals.push({ startMs: regionStart, endMs: regionEnd });
      }
      continue;
    }

    // Non-speech region handling
    if (region.classification === 'SILENCE') {
      if (regionDuration >= t.silence_cut_threshold_ms) {
        gapActions.push({
          startMs: regionStart, endMs: regionEnd, classification: 'SILENCE',
          action: 'CUT', originalDurationMs: regionDuration, resultDurationMs: 0, savedMs: regionDuration,
        });
      } else if (regionDuration >= t.silence_compress_min_ms) {
        const target = t.silence_compress_target_ms;
        keepIntervals.push({ startMs: regionStart, endMs: regionStart + target });
        gapActions.push({
          startMs: regionStart, endMs: regionEnd, classification: 'SILENCE',
          action: 'COMPRESS', originalDurationMs: regionDuration, resultDurationMs: target, savedMs: regionDuration - target,
        });
      } else {
        // Keep short silences
        keepIntervals.push({ startMs: regionStart, endMs: regionEnd });
        gapActions.push({
          startMs: regionStart, endMs: regionEnd, classification: 'SILENCE',
          action: 'KEEP', originalDurationMs: regionDuration, resultDurationMs: regionDuration, savedMs: 0,
        });
      }
    } else if (region.classification === 'BREATH') {
      if (contentType === 'intro' || contentType === 'short') {
        if (regionDuration >= t.breath_cut_threshold_ms) {
          gapActions.push({
            startMs: regionStart, endMs: regionEnd, classification: 'BREATH',
            action: 'CUT', originalDurationMs: regionDuration, resultDurationMs: 0, savedMs: regionDuration,
          });
        } else {
          // Short breath adjacent to speech — keep
          keepIntervals.push({ startMs: regionStart, endMs: regionEnd });
          gapActions.push({
            startMs: regionStart, endMs: regionEnd, classification: 'BREATH',
            action: 'KEEP', originalDurationMs: regionDuration, resultDurationMs: regionDuration, savedMs: 0,
          });
        }
      } else {
        // Main content: trim breaths to 150ms
        const target = THRESHOLDS.main.breath_trim_target_ms!;
        if (regionDuration > target) {
          keepIntervals.push({ startMs: regionStart, endMs: regionStart + target });
          gapActions.push({
            startMs: regionStart, endMs: regionEnd, classification: 'BREATH',
            action: 'TRIM', originalDurationMs: regionDuration, resultDurationMs: target, savedMs: regionDuration - target,
          });
        } else {
          keepIntervals.push({ startMs: regionStart, endMs: regionEnd });
          gapActions.push({
            startMs: regionStart, endMs: regionEnd, classification: 'BREATH',
            action: 'KEEP', originalDurationMs: regionDuration, resultDurationMs: regionDuration, savedMs: 0,
          });
        }
      }
    } else if (region.classification === 'NOISE') {
      gapActions.push({
        startMs: regionStart, endMs: regionEnd, classification: 'NOISE',
        action: 'CUT', originalDurationMs: regionDuration, resultDurationMs: 0, savedMs: regionDuration,
      });
    }
  }

  // Merge overlapping/adjacent keep intervals and filter tiny segments
  const merged = mergeIntervals(keepIntervals, t.min_keep_segment_ms);

  const keepSegments: KeepSegment[] = merged.map(seg => ({
    startMs: seg.startMs,
    endMs: seg.endMs,
    durationMs: seg.endMs - seg.startMs,
    source: 'audio-cleanup',
  }));

  return { keepSegments, gapActions };
}

// --- Should we cut these fillers? ---
function shouldCutFillers(
  fillers: Array<{ startMs: number; endMs: number; word: string }>,
  speechRegion: ClassifiedRegion,
  allRegions: ClassifiedRegion[],
  contentType: 'intro' | 'main' | 'short',
): boolean {
  if (contentType === 'intro' || contentType === 'short') return true; // Always cut fillers in intros/shorts

  // For main content: only cut if filler is isolated (gap >= 200ms on at least one side)
  const gapThreshold = THRESHOLDS.main.filler_isolation_gap_ms!;

  for (const filler of fillers) {
    // Check for silence/breath gap before the filler
    const gapBefore = allRegions.find(
      r => r.classification !== 'SPEECH' && r.endMs >= filler.startMs - gapThreshold && r.endMs <= filler.startMs
    );
    // Check for silence/breath gap after the filler
    const gapAfter = allRegions.find(
      r => r.classification !== 'SPEECH' && r.startMs >= filler.endMs && r.startMs <= filler.endMs + gapThreshold
    );

    if (gapBefore || gapAfter) return true;
  }

  return false;
}

// --- Merge overlapping intervals ---
function mergeIntervals(intervals: Array<{ startMs: number; endMs: number }>, minDuration: number): Array<{ startMs: number; endMs: number }> {
  if (intervals.length === 0) return [];

  const sorted = [...intervals].sort((a, b) => a.startMs - b.startMs);
  const merged: Array<{ startMs: number; endMs: number }> = [sorted[0]];

  for (let i = 1; i < sorted.length; i++) {
    const prev = merged[merged.length - 1];
    const curr = sorted[i];
    if (curr.startMs <= prev.endMs) {
      prev.endMs = Math.max(prev.endMs, curr.endMs);
    } else {
      merged.push({ ...curr });
    }
  }

  // Filter out segments shorter than minimum
  return merged.filter(seg => (seg.endMs - seg.startMs) >= minDuration);
}

// --- Format timestamp ---
function formatMs(ms: number): string {
  const m = Math.floor(ms / 60000);
  const s = (ms % 60000) / 1000;
  return `${m}:${s.toFixed(3).padStart(6, '0')}`;
}

// --- Generate FFmpeg command ---
function generateFfmpegCommand(videoPath: string, keepSegments: KeepSegment[], outputPath: string, audioEnhance: boolean): string {
  if (keepSegments.length === 0) return '# No segments to keep';

  const filters: string[] = [];
  const vLabels: string[] = [];
  const aLabels: string[] = [];

  for (let i = 0; i < keepSegments.length; i++) {
    const seg = keepSegments[i];
    const startSec = (seg.startMs / 1000).toFixed(3);
    const endSec = (seg.endMs / 1000).toFixed(3);
    filters.push(`[0:v]trim=start=${startSec}:end=${endSec},setpts=PTS-STARTPTS[v${i}]`);
    filters.push(`[0:a]atrim=start=${startSec}:end=${endSec},asetpts=PTS-STARTPTS[a${i}]`);
    vLabels.push(`[v${i}]`);
    aLabels.push(`[a${i}]`);
  }

  const concatInput = keepSegments.map((_, i) => `[v${i}][a${i}]`).join('');

  if (audioEnhance) {
    filters.push(`${concatInput}concat=n=${keepSegments.length}:v=1:a=1[outv][outa_raw]`);
    // Studio audio chain: rumble removal → noise gate → compressor → broadcast loudness
    filters.push(`[outa_raw]highpass=f=80,agate=threshold=0.01:ratio=2:attack=5:release=50,acompressor=threshold=-18dB:ratio=3:attack=5:release=50:makeup=2dB,loudnorm=I=-16:TP=-1.5:LRA=11[outa]`);
  } else {
    filters.push(`${concatInput}concat=n=${keepSegments.length}:v=1:a=1[outv][outa]`);
  }

  return `ffmpeg -i "${basename(videoPath)}" -filter_complex "\n  ${filters.join(';\n  ')}\n" -map "[outv]" -map "[outa]" -c:v libx264 -preset fast -crf 18 -c:a aac -b:a 192k "${outputPath}"`;
}

// --- Build clip plan markdown ---
function buildClipPlan(
  videoPath: string,
  contentType: string,
  denoised: boolean,
  audioEnhance: boolean,
  totalDurationMs: number,
  trimInMs: number,
  trimOutMs: number,
  keepSegments: KeepSegment[],
  gapActions: GapAction[],
  fillerRegions: FillerRegion[],
  ffmpegCommand: string,
): string {
  const totalKeptMs = keepSegments.reduce((sum, s) => sum + s.durationMs, 0);
  const totalRemovedMs = totalDurationMs - totalKeptMs;
  const reductionPct = ((totalRemovedMs / totalDurationMs) * 100).toFixed(1);

  const silenceCut = gapActions.filter(g => g.classification === 'SILENCE' && g.action === 'CUT');
  const silenceCompressed = gapActions.filter(g => g.classification === 'SILENCE' && g.action === 'COMPRESS');
  const silenceKept = gapActions.filter(g => g.classification === 'SILENCE' && g.action === 'KEEP');
  const breathActions = gapActions.filter(g => g.classification === 'BREATH' && g.action !== 'KEEP');
  const noiseCut = gapActions.filter(g => g.classification === 'NOISE');
  const fillerCut = gapActions.filter(g => g.classification.startsWith('FILLER'));

  let md = `# Clip Plan

**Source:** \`${basename(videoPath)}\`
**Date:** ${new Date().toISOString().split('T')[0]}
**Content Type:** ${contentType}
**Denoised Analysis:** ${denoised ? 'Yes (highpass 80Hz + arnndn RNNoise)' : 'No'}
**Audio Enhancement:** ${audioEnhance ? 'Yes (gate + compressor + loudnorm -16 LUFS)' : 'No'}
**Buffer:** ${THRESHOLDS[contentType as keyof typeof THRESHOLDS].buffer_ms}ms

## Summary

| Metric | Value |
|--------|-------|
| Original duration | ${formatMs(totalDurationMs)} (${(totalDurationMs / 1000).toFixed(1)}s) |
| Start dead air removed | ${formatMs(trimInMs)} |
| End dead air removed | ${formatMs(totalDurationMs - trimOutMs)} |
| Silence cut | ${silenceCut.length} regions, ${silenceCut.reduce((s, g) => s + g.savedMs, 0)}ms |
| Silence compressed | ${silenceCompressed.length} regions, ${silenceCompressed.reduce((s, g) => s + g.savedMs, 0)}ms saved |
| Silence kept | ${silenceKept.length} regions |
| Breath trimmed/cut | ${breathActions.length} regions, ${breathActions.reduce((s, g) => s + g.savedMs, 0)}ms saved |
| Noise cut | ${noiseCut.length} regions, ${noiseCut.reduce((s, g) => s + g.savedMs, 0)}ms |
| Filler words cut | ${fillerCut.length} regions, ${fillerCut.reduce((s, g) => s + g.savedMs, 0)}ms |
| **Total removed** | **${formatMs(totalRemovedMs)} (${(totalRemovedMs / 1000).toFixed(1)}s)** |
| **Final duration** | **${formatMs(totalKeptMs)} (${(totalKeptMs / 1000).toFixed(1)}s)** |
| **Reduction** | **${reductionPct}%** |
| Keep segments | ${keepSegments.length} |

## Gap Actions

| # | Start | End | Type | Action | Original | Result | Saved |
|---|-------|-----|------|--------|----------|--------|-------|
`;

  gapActions.forEach((g, i) => {
    md += `| ${i + 1} | ${formatMs(g.startMs)} | ${formatMs(g.endMs)} | ${g.classification} | ${g.action} | ${g.originalDurationMs}ms | ${g.resultDurationMs}ms | ${g.savedMs}ms |\n`;
  });

  if (fillerRegions.length > 0) {
    md += `\n## Filler Words Detected\n\n| # | Start | End | Word | Cut? |\n|---|-------|-----|------|------|\n`;
    for (let i = 0; i < fillerRegions.length; i++) {
      const f = fillerRegions[i];
      const wasCut = fillerCut.some(g => g.startMs === f.startMs);
      md += `| ${i + 1} | ${formatMs(f.startMs)} | ${formatMs(f.endMs)} | "${f.word}" | ${wasCut ? 'Yes' : 'No'} |\n`;
    }
  }

  md += `\n## Keep Segments\n\n| # | Start | End | Duration |\n|---|-------|-----|----------|\n`;
  keepSegments.forEach((seg, i) => {
    md += `| ${i + 1} | ${formatMs(seg.startMs)} | ${formatMs(seg.endMs)} | ${(seg.durationMs / 1000).toFixed(2)}s |\n`;
  });

  md += `\n## FFmpeg Command\n\n\`\`\`bash\n${ffmpegCommand}\n\`\`\`\n`;

  return md;
}

// --- Main ---
function main() {
  const { analysis, video, contentType, output, execute, audioEnhance } = parseArgs();

  if (!existsSync(analysis)) {
    console.error(`Error: Analysis file not found: ${analysis}`);
    process.exit(1);
  }
  if (!existsSync(video)) {
    console.error(`Error: Video file not found: ${video}`);
    process.exit(1);
  }

  console.log(`Analysis: ${analysis}`);
  console.log(`Video: ${video}`);
  console.log(`Content type: ${contentType}`);
  console.log(`Audio enhance: ${audioEnhance ? 'yes (gate + compressor + loudnorm)' : 'no'}`);
  console.log();

  // Load analysis JSON
  const data: AnalysisJson = JSON.parse(readFileSync(analysis, 'utf-8'));
  const totalDurationMs = data.audio_metadata.duration_ms;
  const t = THRESHOLDS[contentType];

  console.log(`Duration: ${(totalDurationMs / 1000).toFixed(1)}s`);
  console.log(`Denoised: ${data.denoised ? 'yes' : 'no'}`);
  console.log(`Classified regions: ${data.classified_regions.length}`);
  console.log(`Filler regions: ${data.filler_regions?.length ?? 0}`);
  console.log();

  // Step 1: Filter speech regions
  const { kept: filteredSpeech, discarded } = filterSpeechRegions(data.classified_regions);
  console.log(`Speech regions: ${filteredSpeech.length} kept, ${discarded.length} discarded`);
  if (discarded.length > 0) {
    console.log('  Discarded:');
    for (const d of discarded) {
      console.log(`    ${d.startMs}ms-${d.endMs}ms (${d.durationMs}ms) conf=${d.confidence} db=${d.avgDb}`);
    }
  }

  // Step 2: Apply boundary precision
  const { trimInMs, trimOutMs } = applyBoundaryPrecision(
    filteredSpeech, data.speech_boundary_detail ?? [], totalDurationMs, t.buffer_ms
  );
  console.log(`Trim: ${trimInMs}ms → ${trimOutMs}ms (removing ${trimInMs}ms start, ${totalDurationMs - trimOutMs}ms end)`);

  // Step 3: Apply gap handling
  const { keepSegments, gapActions } = applyGapHandling(
    data.classified_regions, data.filler_regions ?? [], trimInMs, trimOutMs, contentType
  );

  const totalKeptMs = keepSegments.reduce((sum, s) => sum + s.durationMs, 0);
  const totalRemovedMs = totalDurationMs - totalKeptMs;
  console.log(`\nResult: ${keepSegments.length} keep segments`);
  console.log(`  Kept: ${(totalKeptMs / 1000).toFixed(1)}s`);
  console.log(`  Removed: ${(totalRemovedMs / 1000).toFixed(1)}s (${((totalRemovedMs / totalDurationMs) * 100).toFixed(1)}%)`);

  // Step 4: Generate FFmpeg command
  const outputVideo = join(dirname(video), `${basename(video, extname(video))}-cleaned${extname(video)}`);
  const ffmpegCommand = generateFfmpegCommand(video, keepSegments, basename(outputVideo), audioEnhance);

  // Step 5: Write clip plan
  const clipPlan = buildClipPlan(
    video, contentType, data.denoised, audioEnhance, totalDurationMs,
    trimInMs, trimOutMs, keepSegments, gapActions,
    data.filler_regions ?? [], ffmpegCommand,
  );
  writeFileSync(output, clipPlan, 'utf-8');
  console.log(`\nClip plan written to: ${output}`);

  // Step 6: Execute if requested
  if (execute) {
    console.log('\nExecuting FFmpeg command...');
    try {
      execSync(`cd "${dirname(video)}" && ${ffmpegCommand}`, {
        encoding: 'utf-8',
        stdio: 'inherit',
        timeout: 600000,
      });
      console.log(`\nOutput: ${outputVideo}`);
    } catch (err) {
      console.error('FFmpeg execution failed:', err instanceof Error ? err.message : err);
      process.exit(1);
    }
  } else {
    console.log(`\nTo execute: cd "${dirname(video)}" && run the FFmpeg command from the clip plan.`);
    console.log(`Or re-run with --execute flag.`);
  }
}

main();
