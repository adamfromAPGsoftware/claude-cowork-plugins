/**
 * Transcript Timestamp Refinement
 *
 * Cross-references DeepGram word timestamps with the 20ms-granularity
 * VAD probability curve from audio-analysis-sidecar.json to find actual
 * speech onset/offset, correcting drift up to +/-300ms.
 *
 * Usage:
 *   npx tsx refine-transcript.ts \
 *     --transcript <transcript.json> \
 *     --sidecar <audio-analysis-sidecar.json> \
 *     --output <refined-transcript.json>
 */

import { readFileSync, writeFileSync, existsSync } from 'node:fs';
import { resolve } from 'node:path';

// --- Types ---
interface WaveformPoint {
  timeMs: number;
  rmsDbfs: number;
  peakDbfs: number;
  vadProb: number;
}

interface TranscriptWord {
  word: string;
  start: number;
  end: number;
  confidence: number;
  punctuated_word: string;
}

interface RefinedWord extends TranscriptWord {
  originalStart: number;
  originalEnd: number;
}

interface TranscriptJson {
  metadata: Record<string, unknown>;
  speakers?: unknown;
  transcript?: string;
  utterances?: Array<{ start: number; end: number; text: string; confidence: number }>;
  words: TranscriptWord[];
}

interface SidecarJson {
  waveform: WaveformPoint[];
  contentType: string;
  denoised: boolean;
  [key: string]: unknown;
}

// --- Constants ---
const SEARCH_WINDOW_MS = 200;       // +/-200ms search window around DeepGram timestamp
const MAX_CORRECTION_MS = 300;      // Maximum correction cap
const VAD_ONSET_THRESHOLD = 0.3;    // VAD prob below which = no speech (for onset search)
const VAD_CONFIRM_THRESHOLD = 0.7;  // VAD prob above which = DeepGram confirmed, keep original
const ONSET_STEP_FORWARD_MS = 20;   // Step forward from silence edge into speech

// --- CLI Args ---
function parseArgs(): { transcript: string; sidecar: string; output: string } {
  const args = process.argv.slice(2);
  const get = (flag: string): string | undefined => {
    const idx = args.indexOf(flag);
    if (idx === -1 || idx + 1 >= args.length) return undefined;
    return args[idx + 1];
  };

  const transcriptPath = get('--transcript');
  const sidecarPath = get('--sidecar');
  const outputPath = get('--output');

  if (!transcriptPath || !sidecarPath) {
    console.error('Usage: npx tsx refine-transcript.ts --transcript <json> --sidecar <json> [--output <json>]');
    process.exit(1);
  }

  return {
    transcript: resolve(transcriptPath),
    sidecar: resolve(sidecarPath),
    output: outputPath ? resolve(outputPath) : resolve(transcriptPath.replace(/\.json$/, '-refined.json')),
  };
}

// --- Build a lookup index for fast waveform access ---
function buildWaveformIndex(waveform: WaveformPoint[]): {
  points: WaveformPoint[];
  stepMs: number;
  getPointsInRange: (startMs: number, endMs: number) => WaveformPoint[];
  getPointAt: (timeMs: number) => WaveformPoint | null;
} {
  if (waveform.length < 2) {
    throw new Error('Sidecar waveform has fewer than 2 points');
  }

  const stepMs = waveform[1].timeMs - waveform[0].timeMs; // Should be ~20ms
  const startTimeMs = waveform[0].timeMs;

  function indexFor(timeMs: number): number {
    return Math.round((timeMs - startTimeMs) / stepMs);
  }

  return {
    points: waveform,
    stepMs,
    getPointsInRange(startMs: number, endMs: number): WaveformPoint[] {
      const startIdx = Math.max(0, indexFor(startMs));
      const endIdx = Math.min(waveform.length - 1, indexFor(endMs));
      return waveform.slice(startIdx, endIdx + 1);
    },
    getPointAt(timeMs: number): WaveformPoint | null {
      const idx = indexFor(timeMs);
      if (idx < 0 || idx >= waveform.length) return null;
      return waveform[idx];
    },
  };
}

// --- Refine a single word's start timestamp ---
function refineStart(
  originalStartMs: number,
  waveformIndex: ReturnType<typeof buildWaveformIndex>,
): number {
  // Check if DeepGram timestamp is already confirmed by high VAD
  const pointAtOriginal = waveformIndex.getPointAt(originalStartMs);
  if (pointAtOriginal && pointAtOriginal.vadProb > VAD_CONFIRM_THRESHOLD) {
    return originalStartMs; // DeepGram is accurate here
  }

  // Search backward from DeepGram start to find where speech actually begins
  const searchStart = originalStartMs - SEARCH_WINDOW_MS;
  const searchEnd = originalStartMs + SEARCH_WINDOW_MS;
  const points = waveformIndex.getPointsInRange(searchStart, searchEnd);

  if (points.length === 0) return originalStartMs;

  // Find the original timestamp's position in the points array
  const origIdx = points.findIndex(p => p.timeMs >= originalStartMs);
  if (origIdx === -1) return originalStartMs;

  // Walk backward from DeepGram start to find where VAD drops below threshold
  // (i.e., find the edge of silence before speech)
  let onsetIdx = origIdx;
  for (let i = origIdx; i >= 0; i--) {
    if (points[i].vadProb < VAD_ONSET_THRESHOLD) {
      // Found silence — speech onset is the next point (back into speech)
      onsetIdx = Math.min(i + 1, points.length - 1);
      break;
    }
    onsetIdx = i; // Keep walking back while VAD is high
  }

  // Also check forward — DeepGram might be early (word hasn't started yet)
  if (pointAtOriginal && pointAtOriginal.vadProb < VAD_ONSET_THRESHOLD) {
    // DeepGram timestamp is in silence — walk forward to find speech onset
    for (let i = origIdx; i < points.length; i++) {
      if (points[i].vadProb >= VAD_ONSET_THRESHOLD) {
        onsetIdx = i;
        break;
      }
    }
  }

  const refinedMs = points[onsetIdx].timeMs;

  // Cap correction
  const correction = refinedMs - originalStartMs;
  if (Math.abs(correction) > MAX_CORRECTION_MS) {
    return originalStartMs + Math.sign(correction) * MAX_CORRECTION_MS;
  }

  return refinedMs;
}

// --- Refine a single word's end timestamp ---
function refineEnd(
  originalEndMs: number,
  waveformIndex: ReturnType<typeof buildWaveformIndex>,
): number {
  // Check if DeepGram timestamp is already confirmed by high VAD
  const pointAtOriginal = waveformIndex.getPointAt(originalEndMs);
  if (pointAtOriginal && pointAtOriginal.vadProb > VAD_CONFIRM_THRESHOLD) {
    return originalEndMs; // DeepGram is accurate here
  }

  const searchStart = originalEndMs - SEARCH_WINDOW_MS;
  const searchEnd = originalEndMs + SEARCH_WINDOW_MS;
  const points = waveformIndex.getPointsInRange(searchStart, searchEnd);

  if (points.length === 0) return originalEndMs;

  const origIdx = points.findIndex(p => p.timeMs >= originalEndMs);
  if (origIdx === -1) return originalEndMs;

  // Walk forward from DeepGram end to find where VAD drops (end of speech)
  let offsetIdx = origIdx;
  for (let i = origIdx; i < points.length; i++) {
    if (points[i].vadProb < VAD_ONSET_THRESHOLD) {
      offsetIdx = i;
      break;
    }
    offsetIdx = i; // Keep walking forward while VAD is high
  }

  // Also check backward — DeepGram might be late (word ended earlier)
  if (pointAtOriginal && pointAtOriginal.vadProb < VAD_ONSET_THRESHOLD) {
    // DeepGram timestamp is in silence — walk backward to find speech offset
    for (let i = origIdx; i >= 0; i--) {
      if (points[i].vadProb >= VAD_ONSET_THRESHOLD) {
        offsetIdx = i;
        break;
      }
    }
  }

  const refinedMs = points[offsetIdx].timeMs;

  // Cap correction
  const correction = refinedMs - originalEndMs;
  if (Math.abs(correction) > MAX_CORRECTION_MS) {
    return originalEndMs + Math.sign(correction) * MAX_CORRECTION_MS;
  }

  return refinedMs;
}

// --- Main ---
function main() {
  const { transcript: transcriptPath, sidecar: sidecarPath, output: outputPath } = parseArgs();

  if (!existsSync(transcriptPath)) {
    console.error(`Error: Transcript not found: ${transcriptPath}`);
    process.exit(1);
  }
  if (!existsSync(sidecarPath)) {
    console.error(`Error: Sidecar not found: ${sidecarPath}`);
    process.exit(1);
  }

  console.log(`Transcript: ${transcriptPath}`);
  console.log(`Sidecar: ${sidecarPath}`);
  console.log(`Output: ${outputPath}`);
  console.log();

  // Load inputs
  const rawTranscript = JSON.parse(readFileSync(transcriptPath, 'utf-8'));
  const sidecarData: SidecarJson = JSON.parse(readFileSync(sidecarPath, 'utf-8'));

  // Support both flat {words:[]} and DeepGram nested {results:{channels:[{alternatives:[{words:[]}]}]}} formats
  let transcriptData: TranscriptJson;
  if (rawTranscript.words) {
    transcriptData = rawTranscript as TranscriptJson;
  } else if (rawTranscript.results?.channels?.[0]?.alternatives?.[0]?.words) {
    const alt = rawTranscript.results.channels[0].alternatives[0];
    transcriptData = {
      metadata: rawTranscript.metadata ?? {},
      transcript: alt.transcript,
      utterances: rawTranscript.results.utterances,
      words: alt.words,
    };
  } else {
    console.error('Error: Transcript has no words array');
    process.exit(1);
  }

  if (!transcriptData.words || transcriptData.words.length === 0) {
    console.error('Error: Transcript has no words array');
    process.exit(1);
  }
  if (!sidecarData.waveform || sidecarData.waveform.length === 0) {
    console.error('Error: Sidecar has no waveform data');
    process.exit(1);
  }

  console.log(`Words: ${transcriptData.words.length}`);
  console.log(`Waveform points: ${sidecarData.waveform.length}`);
  console.log(`Waveform step: ${sidecarData.waveform.length >= 2 ? sidecarData.waveform[1].timeMs - sidecarData.waveform[0].timeMs : '?'}ms`);
  console.log();

  // Build waveform index
  const waveformIndex = buildWaveformIndex(sidecarData.waveform);

  // Refine each word
  const refinedWords: RefinedWord[] = [];
  let totalStartCorrection = 0;
  let totalEndCorrection = 0;
  let wordsModified = 0;

  for (const word of transcriptData.words) {
    const originalStartMs = word.start * 1000;
    const originalEndMs = word.end * 1000;

    const refinedStartMs = refineStart(originalStartMs, waveformIndex);
    const refinedEndMs = refineEnd(originalEndMs, waveformIndex);

    // Ensure start < end (with minimum 40ms word duration)
    let finalStartMs = refinedStartMs;
    let finalEndMs = Math.max(refinedEndMs, refinedStartMs + 40);

    // Convert back to seconds
    const refinedStart = finalStartMs / 1000;
    const refinedEnd = finalEndMs / 1000;

    const startDelta = Math.abs(refinedStart - word.start) * 1000;
    const endDelta = Math.abs(refinedEnd - word.end) * 1000;
    const modified = startDelta > 5 || endDelta > 5; // >5ms = meaningful change

    if (modified) {
      wordsModified++;
      totalStartCorrection += startDelta;
      totalEndCorrection += endDelta;
    }

    refinedWords.push({
      word: word.word,
      start: refinedStart,
      end: refinedEnd,
      confidence: word.confidence,
      punctuated_word: word.punctuated_word,
      originalStart: word.start,
      originalEnd: word.end,
    });
  }

  // Build output — same structure as input but with refined words
  const output: TranscriptJson & { refinement_metadata: Record<string, unknown> } = {
    ...transcriptData,
    words: refinedWords,
    refinement_metadata: {
      refined_at: new Date().toISOString(),
      source_transcript: transcriptPath,
      source_sidecar: sidecarPath,
      total_words: transcriptData.words.length,
      words_modified: wordsModified,
      words_unchanged: transcriptData.words.length - wordsModified,
      avg_start_correction_ms: wordsModified > 0 ? Math.round(totalStartCorrection / wordsModified) : 0,
      avg_end_correction_ms: wordsModified > 0 ? Math.round(totalEndCorrection / wordsModified) : 0,
      max_correction_cap_ms: MAX_CORRECTION_MS,
      search_window_ms: SEARCH_WINDOW_MS,
      vad_onset_threshold: VAD_ONSET_THRESHOLD,
      vad_confirm_threshold: VAD_CONFIRM_THRESHOLD,
    },
  };

  writeFileSync(outputPath, JSON.stringify(output, null, 2), 'utf-8');

  // Summary
  console.log(`Refinement complete:`);
  console.log(`  Words modified: ${wordsModified}/${transcriptData.words.length} (${((wordsModified / transcriptData.words.length) * 100).toFixed(1)}%)`);
  console.log(`  Avg start correction: ${wordsModified > 0 ? Math.round(totalStartCorrection / wordsModified) : 0}ms`);
  console.log(`  Avg end correction: ${wordsModified > 0 ? Math.round(totalEndCorrection / wordsModified) : 0}ms`);
  console.log(`\nOutput: ${outputPath}`);
}

main();
