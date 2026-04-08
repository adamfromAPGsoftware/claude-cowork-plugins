import { writeFileSync, existsSync, unlinkSync, readFileSync, statSync, mkdirSync } from 'node:fs';
import { resolve, dirname, join, basename, extname } from 'node:path';
import { fileURLToPath } from 'node:url';
import { execSync } from 'node:child_process';

const __dirname = dirname(fileURLToPath(import.meta.url));

// --- Constants ---
const SAMPLE_RATE = 16000; // 16kHz mono — required by Silero VAD
const WINDOW_MS = 20; // dB waveform window size in milliseconds
const WINDOW_SAMPLES = Math.floor(SAMPLE_RATE * (WINDOW_MS / 1000)); // 320 samples per window
const SILENCE_THRESHOLD_DB = -35; // dBFS threshold for silence detection
const SILENCE_MIN_DURATION = 0.15; // minimum silence duration in seconds (150ms)
const BREATH_MAX_DURATION_MS = 500; // max duration for breath classification (ms)
const NOISE_MIN_DURATION_MS = 500; // min duration for noise classification (ms)
const VAD_SPEECH_THRESHOLD = 0.5; // VAD probability threshold for speech
const BOUNDARY_WINDOW_MS = 150; // ±ms window around speech onset/offset for boundary detail
const MIN_REGION_DURATION_MS = 80; // minimum non-SPEECH region duration before absorption

// --- Denoising Constants ---
const RNNOISE_MODEL_URL = 'https://github.com/richardpl/arnndn-models/raw/master/std.rnnn';
const DENOISE_MIX = 0.95; // aggressive denoising for analysis (not output audio)
const HIGHPASS_FREQ = 80; // Hz — removes low-frequency rumble (HVAC, traffic)

// --- Filler Word Constants ---
const FILLER_WORDS = new Set([
  'uh', 'um', 'ah', 'er', 'eh', 'hm', 'hmm', 'mm', 'mhm', 'uh-huh',
]);

// --- CLI Args ---
function parseArgs(): { video: string; output: string; transcript: string | null; denoise: boolean; contentType: string } {
  const args = process.argv.slice(2);
  const get = (flag: string): string | undefined => {
    const idx = args.indexOf(flag);
    if (idx === -1 || idx + 1 >= args.length) return undefined;
    return args[idx + 1];
  };
  const has = (flag: string): boolean => args.includes(flag);

  const videoRaw = get('--video');
  if (!videoRaw) {
    console.error('Usage: npx tsx analyze-audio.ts --video <path> [options]');
    console.error('  --video          Path to the video file (required)');
    console.error('  --output         Path for output markdown (default: {video-dir}/{video-name}-audio-analysis.md)');
    console.error('  --transcript     Path to Deepgram transcript for pre-filtered output (optional)');
    console.error('  --content-type   Content type: intro | main | short (default: main)');
    console.error('  --no-denoise     Skip audio denoising preprocessing');
    process.exit(1);
  }

  const video = resolve(videoRaw);
  if (!existsSync(video)) {
    console.error(`Error: Video file not found: ${video}`);
    process.exit(1);
  }

  const outputRaw = get('--output');
  const output = outputRaw
    ? resolve(outputRaw)
    : join(dirname(video), `${basename(video, extname(video))}-audio-analysis.md`);

  const transcriptRaw = get('--transcript');
  let transcript: string | null = null;
  if (transcriptRaw) {
    transcript = resolve(transcriptRaw);
    if (!existsSync(transcript)) {
      console.error(`Error: Transcript file not found: ${transcript}`);
      process.exit(1);
    }
  }

  const denoise = !has('--no-denoise');
  const contentType = get('--content-type') ?? 'main';
  if (!['intro', 'main', 'short'].includes(contentType)) {
    console.error(`Error: --content-type must be 'intro', 'main', or 'short', got '${contentType}'`);
    process.exit(1);
  }

  return { video, output, transcript, denoise, contentType };
}

// --- Get video duration via ffprobe ---
function getVideoDuration(videoPath: string): number {
  try {
    const result = execSync(
      `ffprobe -v error -show_entries format=duration -of csv=p=0 "${videoPath}"`,
      { encoding: 'utf-8' },
    );
    return parseFloat(result.trim());
  } catch {
    return 0;
  }
}

// --- Denoise audio for analysis ---
// Uses FFmpeg arnndn (RNNoise) to remove background noise + highpass to remove rumble.
// Denoised audio is used ONLY for analysis — final clip commands reference the original video.
// Timestamps remain perfectly aligned since denoising doesn't alter timing.
function denoiseAudio(wavPath: string): string {
  const modelDir = join(__dirname, 'models');
  const modelPath = join(modelDir, 'std.rnnn');

  // Auto-download RNNoise model if missing
  if (!existsSync(modelPath)) {
    console.log('  Downloading RNNoise model for denoising...');
    if (!existsSync(modelDir)) mkdirSync(modelDir, { recursive: true });
    try {
      execSync(`curl -sL "${RNNOISE_MODEL_URL}" -o "${modelPath}"`, { encoding: 'utf-8', timeout: 30000 });
      console.log('  RNNoise model downloaded.');
    } catch {
      console.error('  Warning: Failed to download RNNoise model. Skipping denoising.');
      return wavPath;
    }
  }

  const denoisedPath = join(dirname(wavPath), `_denoised_${Date.now()}.wav`);

  try {
    console.log(`  Applying highpass ${HIGHPASS_FREQ}Hz + RNNoise arnndn (mix=${DENOISE_MIX})...`);
    execSync(
      `ffmpeg -i "${wavPath}" -af "highpass=f=${HIGHPASS_FREQ},arnndn=m='${modelPath}':mix=${DENOISE_MIX}" -ar ${SAMPLE_RATE} -ac 1 -acodec pcm_s16le "${denoisedPath}" -y 2>/dev/null`,
      { encoding: 'utf-8', maxBuffer: 50 * 1024 * 1024 },
    );
    console.log('  Audio denoised successfully.');
    return denoisedPath;
  } catch (err) {
    console.error(`  Warning: Denoising failed (${err instanceof Error ? err.message : 'unknown error'}). Using original audio.`);
    return wavPath;
  }
}

// --- Filler region extraction from transcript ---
interface FillerRegion {
  startMs: number;
  endMs: number;
  durationMs: number;
  word: string;
}

function extractFillerRegions(transcript: ParsedTranscript): FillerRegion[] {
  const fillers: FillerRegion[] = [];
  for (const word of transcript.words) {
    const clean = word.word.toLowerCase().replace(/[^a-z-]/g, '');
    if (FILLER_WORDS.has(clean)) {
      const startMs = Math.round(word.start * 1000);
      const endMs = Math.round(word.end * 1000);
      fillers.push({ startMs, endMs, durationMs: endMs - startMs, word: word.word });
    }
  }
  return fillers;
}

// --- Extract audio as raw PCM (16-bit signed LE, 16kHz, mono) ---
function extractRawAudio(videoPath: string): string {
  const rawPath = join(dirname(videoPath), `_temp_audio_${Date.now()}.raw`);
  try {
    execSync(
      `ffmpeg -i "${videoPath}" -vn -ar ${SAMPLE_RATE} -ac 1 -f s16le -acodec pcm_s16le "${rawPath}" -y 2>/dev/null`,
      { encoding: 'utf-8' },
    );
    return rawPath;
  } catch {
    console.error('Error: ffmpeg audio extraction failed. Ensure ffmpeg is installed.');
    process.exit(1);
  }
}

// --- Extract audio as WAV for VAD (Silero needs a file format it can read) ---
function extractWavAudio(videoPath: string): string {
  const wavPath = join(dirname(videoPath), `_temp_audio_${Date.now()}.wav`);
  try {
    execSync(
      `ffmpeg -i "${videoPath}" -vn -ar ${SAMPLE_RATE} -ac 1 -acodec pcm_s16le "${wavPath}" -y 2>/dev/null`,
      { encoding: 'utf-8' },
    );
    return wavPath;
  } catch {
    console.error('Error: ffmpeg WAV extraction failed.');
    process.exit(1);
  }
}

// --- Layer 1: ffmpeg silencedetect ---
interface SilenceRegion {
  startMs: number;
  endMs: number;
  durationMs: number;
}

function runSilenceDetect(videoPath: string): SilenceRegion[] {
  console.log(`Running ffmpeg silencedetect (threshold: ${SILENCE_THRESHOLD_DB}dB, min duration: ${SILENCE_MIN_DURATION}s)...`);
  try {
    const output = execSync(
      `ffmpeg -i "${videoPath}" -af silencedetect=n=${SILENCE_THRESHOLD_DB}dB:d=${SILENCE_MIN_DURATION} -vn -f null - 2>&1`,
      { encoding: 'utf-8', maxBuffer: 50 * 1024 * 1024 },
    );

    const regions: SilenceRegion[] = [];
    const lines = output.split('\n');

    let currentStart: number | null = null;
    for (const line of lines) {
      const startMatch = line.match(/silence_start:\s*([\d.]+)/);
      if (startMatch) {
        currentStart = parseFloat(startMatch[1]);
      }
      const endMatch = line.match(/silence_end:\s*([\d.]+)\s*\|\s*silence_duration:\s*([\d.]+)/);
      if (endMatch && currentStart !== null) {
        const endSec = parseFloat(endMatch[1]);
        const durSec = parseFloat(endMatch[2]);
        regions.push({
          startMs: Math.round(currentStart * 1000),
          endMs: Math.round(endSec * 1000),
          durationMs: Math.round(durSec * 1000),
        });
        currentStart = null;
      }
    }

    console.log(`  Found ${regions.length} silence regions.`);
    return regions;
  } catch (err: unknown) {
    // silencedetect writes to stderr even on success; try parsing
    const msg = err instanceof Error ? (err as Error & { stderr?: string }).stderr || '' : '';
    if (msg.includes('silence_start')) {
      // Parse from error output (ffmpeg writes filter output to stderr)
      const regions: SilenceRegion[] = [];
      const lines = msg.split('\n');
      let currentStart: number | null = null;
      for (const line of lines) {
        const startMatch = line.match(/silence_start:\s*([\d.]+)/);
        if (startMatch) currentStart = parseFloat(startMatch[1]);
        const endMatch = line.match(/silence_end:\s*([\d.]+)\s*\|\s*silence_duration:\s*([\d.]+)/);
        if (endMatch && currentStart !== null) {
          regions.push({
            startMs: Math.round(currentStart * 1000),
            endMs: Math.round(parseFloat(endMatch[1]) * 1000),
            durationMs: Math.round(parseFloat(endMatch[2]) * 1000),
          });
          currentStart = null;
        }
      }
      console.log(`  Found ${regions.length} silence regions.`);
      return regions;
    }
    console.error('Warning: silencedetect failed, continuing without silence data.');
    return [];
  }
}

// --- Layer 2: Compute dB waveform from raw PCM ---
interface WaveformPoint {
  timeMs: number;
  rmsDbfs: number;
  peakDbfs: number;
  vadProb: number; // filled in later from VAD results
}

function computeWaveform(rawPath: string): WaveformPoint[] {
  console.log(`Computing dB waveform (${WINDOW_MS}ms windows)...`);
  const buffer = readFileSync(rawPath);
  const samples = new Int16Array(buffer.buffer, buffer.byteOffset, buffer.byteLength / 2);
  const totalSamples = samples.length;
  const points: WaveformPoint[] = [];

  for (let i = 0; i + WINDOW_SAMPLES <= totalSamples; i += WINDOW_SAMPLES) {
    let sumSquares = 0;
    let peak = 0;

    for (let j = 0; j < WINDOW_SAMPLES; j++) {
      const sample = samples[i + j] / 32768.0; // normalize to [-1, 1]
      sumSquares += sample * sample;
      const abs = Math.abs(sample);
      if (abs > peak) peak = abs;
    }

    const rms = Math.sqrt(sumSquares / WINDOW_SAMPLES);
    const rmsDbfs = rms > 0 ? 20 * Math.log10(rms) : -96;
    const peakDbfs = peak > 0 ? 20 * Math.log10(peak) : -96;
    const timeMs = Math.round((i / SAMPLE_RATE) * 1000);

    points.push({ timeMs, rmsDbfs: Math.round(rmsDbfs * 10) / 10, peakDbfs: Math.round(peakDbfs * 10) / 10, vadProb: 0 });
  }

  console.log(`  Computed ${points.length} waveform points over ${Math.round(totalSamples / SAMPLE_RATE)}s.`);
  return points;
}

// --- Layer 3: Silero VAD via Python subprocess ---
interface VADRegion {
  startMs: number;
  endMs: number;
  durationMs: number;
  avgProbability: number;
}

interface VADResult {
  regions: VADRegion[];
  probabilities: Array<{ timeMs: number; probability: number }>;
}

function runVAD(wavPath: string): VADResult {
  console.log('Running Silero VAD (ONNX)...');
  const vadScript = join(__dirname, 'vad.py');

  try {
    const output = execSync(
      `python3 "${vadScript}" "${wavPath}"`,
      { encoding: 'utf-8', maxBuffer: 100 * 1024 * 1024 },
    );

    const result = JSON.parse(output.trim()) as {
      speech_regions: Array<{ start: number; end: number; probability: number }>;
      frame_probabilities: Array<{ time: number; probability: number }>;
    };

    const regions: VADRegion[] = result.speech_regions.map((r) => ({
      startMs: Math.round(r.start * 1000),
      endMs: Math.round(r.end * 1000),
      durationMs: Math.round((r.end - r.start) * 1000),
      avgProbability: Math.round(r.probability * 1000) / 1000,
    }));

    const probabilities = result.frame_probabilities.map((p) => ({
      timeMs: Math.round(p.time * 1000),
      probability: Math.round(p.probability * 1000) / 1000,
    }));

    console.log(`  Found ${regions.length} speech regions.`);
    return { regions, probabilities };
  } catch (err) {
    const msg = err instanceof Error ? err.message : String(err);
    console.error(`Error: Silero VAD failed. Ensure Python 3.8+ and required packages are installed.`);
    console.error(`  pip3 install onnxruntime numpy`);
    console.error(`  Details: ${msg}`);
    process.exit(1);
  }
}

// --- Cross-reference and classify ---
type Classification = 'SPEECH' | 'BREATH' | 'SILENCE' | 'NOISE';

interface ClassifiedRegion {
  startMs: number;
  endMs: number;
  durationMs: number;
  classification: Classification;
  confidence: number;
  avgDb: number;
  vadProb: number;
}

function classifyRegions(
  silenceRegions: SilenceRegion[],
  waveform: WaveformPoint[],
  vad: VADResult,
  totalDurationMs: number,
): ClassifiedRegion[] {
  // Build a timeline at 20ms resolution
  const resolution = WINDOW_MS;
  const totalSlots = Math.ceil(totalDurationMs / resolution);

  // Initialize arrays
  const dbValues = new Float32Array(totalSlots).fill(-96);
  const vadValues = new Float32Array(totalSlots).fill(0);
  const isSilent = new Uint8Array(totalSlots).fill(0);

  // Fill dB values from waveform
  for (const point of waveform) {
    const slot = Math.floor(point.timeMs / resolution);
    if (slot < totalSlots) dbValues[slot] = point.rmsDbfs;
  }

  // Fill VAD probabilities
  for (const prob of vad.probabilities) {
    const slot = Math.floor(prob.timeMs / resolution);
    if (slot < totalSlots) vadValues[slot] = prob.probability;
  }

  // Mark silence regions
  for (const region of silenceRegions) {
    const startSlot = Math.floor(region.startMs / resolution);
    const endSlot = Math.ceil(region.endMs / resolution);
    for (let i = startSlot; i < endSlot && i < totalSlots; i++) {
      isSilent[i] = 1;
    }
  }

  // Classify each slot
  const slotClassifications: Classification[] = new Array(totalSlots);
  for (let i = 0; i < totalSlots; i++) {
    const db = dbValues[i];
    const vadProb = vadValues[i];
    const silent = isSilent[i];

    if (vadProb >= VAD_SPEECH_THRESHOLD) {
      slotClassifications[i] = 'SPEECH';
    } else if (silent && db < SILENCE_THRESHOLD_DB) {
      slotClassifications[i] = 'SILENCE';
    } else if (db >= SILENCE_THRESHOLD_DB && vadProb < VAD_SPEECH_THRESHOLD) {
      // Energy present but not speech — could be breath or noise (determined by region duration later)
      slotClassifications[i] = 'BREATH'; // provisional — may become NOISE based on run length
    } else {
      slotClassifications[i] = 'SILENCE';
    }
  }

  // Merge consecutive slots with same classification into regions
  const rawRegions: ClassifiedRegion[] = [];
  let regionStart = 0;
  let currentClass = slotClassifications[0];

  for (let i = 1; i <= totalSlots; i++) {
    const cls = i < totalSlots ? slotClassifications[i] : null;
    if (cls !== currentClass || i === totalSlots) {
      const startMs = regionStart * resolution;
      const endMs = i * resolution;
      const durationMs = endMs - startMs;

      // Compute averages for this region
      let dbSum = 0;
      let vadSum = 0;
      let count = 0;
      for (let j = regionStart; j < i && j < totalSlots; j++) {
        dbSum += dbValues[j];
        vadSum += vadValues[j];
        count++;
      }
      const avgDb = count > 0 ? Math.round((dbSum / count) * 10) / 10 : -96;
      const avgVad = count > 0 ? Math.round((vadSum / count) * 1000) / 1000 : 0;

      // Reclassify BREATH vs NOISE based on duration
      let finalClass = currentClass;
      if (currentClass === 'BREATH') {
        finalClass = durationMs > BREATH_MAX_DURATION_MS ? 'NOISE' : 'BREATH';
      }

      // Confidence: how strongly the signals agree
      let confidence: number;
      switch (finalClass) {
        case 'SPEECH':
          confidence = avgVad; // VAD probability is the confidence
          break;
        case 'SILENCE':
          confidence = 1 - avgVad; // inverse VAD = confidence it's not speech
          break;
        case 'BREATH':
          confidence = Math.min(0.9, (1 - avgVad) * 0.8 + 0.2); // moderate confidence
          break;
        case 'NOISE':
          confidence = Math.min(0.8, (1 - avgVad) * 0.7 + 0.1); // lower confidence
          break;
      }

      rawRegions.push({
        startMs,
        endMs: Math.min(endMs, totalDurationMs),
        durationMs: Math.min(durationMs, totalDurationMs - startMs),
        classification: finalClass,
        confidence: Math.round(confidence * 1000) / 1000,
        avgDb,
        vadProb: avgVad,
      });

      regionStart = i;
      if (i < totalSlots) currentClass = slotClassifications[i];
    }
  }

  // Pass 1: Merge very short non-speech regions (< 200ms) between speech regions into speech
  // This prevents micro-gaps from VAD probability fluctuations splitting continuous speech
  const smoothed: ClassifiedRegion[] = [];
  for (let i = 0; i < rawRegions.length; i++) {
    const region = rawRegions[i];
    if (
      region.classification !== 'SPEECH' &&
      region.durationMs < 200 &&
      smoothed.length > 0 &&
      smoothed[smoothed.length - 1].classification === 'SPEECH' &&
      i + 1 < rawRegions.length &&
      rawRegions[i + 1].classification === 'SPEECH'
    ) {
      // Absorb short non-speech gap into surrounding speech
      const prev = smoothed[smoothed.length - 1];
      prev.endMs = region.endMs;
      prev.durationMs = prev.endMs - prev.startMs;
    } else {
      smoothed.push({ ...region });
    }
  }

  // Pass 2: Merge consecutive regions with same classification
  const merged: ClassifiedRegion[] = [];
  for (const region of smoothed) {
    if (merged.length > 0 && merged[merged.length - 1].classification === region.classification) {
      const prev = merged[merged.length - 1];
      // Weighted average for dB and VAD
      const prevWeight = prev.durationMs;
      const curWeight = region.durationMs;
      const totalWeight = prevWeight + curWeight;
      prev.avgDb = Math.round(((prev.avgDb * prevWeight + region.avgDb * curWeight) / totalWeight) * 10) / 10;
      prev.vadProb = Math.round(((prev.vadProb * prevWeight + region.vadProb * curWeight) / totalWeight) * 1000) / 1000;
      prev.confidence = Math.round(((prev.confidence * prevWeight + region.confidence * curWeight) / totalWeight) * 1000) / 1000;
      prev.endMs = region.endMs;
      prev.durationMs = prev.endMs - prev.startMs;
    } else {
      merged.push({ ...region });
    }
  }

  // Pass 3: Absorb micro non-SPEECH regions (< MIN_REGION_DURATION_MS) into longer neighbor
  const absorbed: ClassifiedRegion[] = [];
  for (let i = 0; i < merged.length; i++) {
    const region = merged[i];
    if (region.classification !== 'SPEECH' && region.durationMs < MIN_REGION_DURATION_MS) {
      // Find the longer neighbor to absorb into
      const prev = absorbed.length > 0 ? absorbed[absorbed.length - 1] : null;
      const next = i + 1 < merged.length ? merged[i + 1] : null;
      const prevDur = prev ? prev.durationMs : 0;
      const nextDur = next ? next.durationMs : 0;

      if (prev && prevDur >= nextDur) {
        // Absorb into previous (weighted avg)
        const prevWeight = prev.durationMs;
        const curWeight = region.durationMs;
        const totalWeight = prevWeight + curWeight;
        prev.avgDb = Math.round(((prev.avgDb * prevWeight + region.avgDb * curWeight) / totalWeight) * 10) / 10;
        prev.vadProb = Math.round(((prev.vadProb * prevWeight + region.vadProb * curWeight) / totalWeight) * 1000) / 1000;
        prev.confidence = Math.round(((prev.confidence * prevWeight + region.confidence * curWeight) / totalWeight) * 1000) / 1000;
        prev.endMs = region.endMs;
        prev.durationMs = prev.endMs - prev.startMs;
      } else if (next) {
        // Absorb into next (weighted avg — modify next in place so it picks up the absorbed region)
        const nextWeight = next.durationMs;
        const curWeight = region.durationMs;
        const totalWeight = nextWeight + curWeight;
        next.avgDb = Math.round(((next.avgDb * nextWeight + region.avgDb * curWeight) / totalWeight) * 10) / 10;
        next.vadProb = Math.round(((next.vadProb * nextWeight + region.vadProb * curWeight) / totalWeight) * 1000) / 1000;
        next.confidence = Math.round(((next.confidence * nextWeight + region.confidence * curWeight) / totalWeight) * 1000) / 1000;
        next.startMs = region.startMs;
        next.durationMs = next.endMs - next.startMs;
      } else {
        // No neighbor — keep as-is
        absorbed.push({ ...region });
      }
    } else {
      absorbed.push({ ...region });
    }
  }

  // Pass 3b: Re-run same-classification merge after absorption
  const finalMerged: ClassifiedRegion[] = [];
  for (const region of absorbed) {
    if (finalMerged.length > 0 && finalMerged[finalMerged.length - 1].classification === region.classification) {
      const prev = finalMerged[finalMerged.length - 1];
      const prevWeight = prev.durationMs;
      const curWeight = region.durationMs;
      const totalWeight = prevWeight + curWeight;
      prev.avgDb = Math.round(((prev.avgDb * prevWeight + region.avgDb * curWeight) / totalWeight) * 10) / 10;
      prev.vadProb = Math.round(((prev.vadProb * prevWeight + region.vadProb * curWeight) / totalWeight) * 1000) / 1000;
      prev.confidence = Math.round(((prev.confidence * prevWeight + region.confidence * curWeight) / totalWeight) * 1000) / 1000;
      prev.endMs = region.endMs;
      prev.durationMs = prev.endMs - prev.startMs;
    } else {
      finalMerged.push({ ...region });
    }
  }

  return finalMerged;
}

// --- Overlay VAD probabilities onto waveform ---
function overlayVADOnWaveform(waveform: WaveformPoint[], vad: VADResult): void {
  // Build a lookup from VAD probabilities
  const vadMap = new Map<number, number>();
  for (const p of vad.probabilities) {
    vadMap.set(Math.round(p.timeMs / WINDOW_MS) * WINDOW_MS, p.probability);
  }

  for (const point of waveform) {
    const prob = vadMap.get(point.timeMs);
    if (prob !== undefined) {
      point.vadProb = Math.round(prob * 1000) / 1000;
    }
  }
}

// --- Compute boundary detail for speech regions ---
interface BoundaryDetail {
  regionIdx: number;
  startMs: number;
  endMs: number;
  durationMs: number;
  onset: WaveformPoint[];
  offset: WaveformPoint[];
}

function computeBoundaryDetail(
  classified: ClassifiedRegion[],
  waveform: WaveformPoint[],
): BoundaryDetail[] {
  // Build a lookup map from timeMs → waveform point for fast access
  const waveformMap = new Map<number, WaveformPoint>();
  for (const p of waveform) {
    waveformMap.set(p.timeMs, p);
  }

  const details: BoundaryDetail[] = [];

  classified.forEach((region, idx) => {
    if (region.classification !== 'SPEECH') return;

    // Onset: BOUNDARY_WINDOW_MS before and after speech start at 20ms resolution
    const onsetStart = Math.max(0, region.startMs - BOUNDARY_WINDOW_MS);
    const onsetEnd = region.startMs + BOUNDARY_WINDOW_MS;
    const onsetPoints: WaveformPoint[] = [];
    for (let t = onsetStart; t <= onsetEnd; t += WINDOW_MS) {
      const p = waveformMap.get(t);
      if (p) onsetPoints.push(p);
    }

    // Offset: BOUNDARY_WINDOW_MS before and after speech end at 20ms resolution
    const offsetStart = Math.max(0, region.endMs - BOUNDARY_WINDOW_MS);
    const offsetEnd = region.endMs + BOUNDARY_WINDOW_MS;
    const offsetPoints: WaveformPoint[] = [];
    for (let t = offsetStart; t <= offsetEnd; t += WINDOW_MS) {
      const p = waveformMap.get(t);
      if (p) offsetPoints.push(p);
    }

    details.push({
      regionIdx: idx,
      startMs: region.startMs,
      endMs: region.endMs,
      durationMs: region.durationMs,
      onset: onsetPoints,
      offset: offsetPoints,
    });
  });

  return details;
}

// --- Compute overall audio stats ---
interface AudioStats {
  overallRmsDbfs: number;
  peakDbfs: number;
  noiseFloorDbfs: number;
  dynamicRangeDb: number;
  totalSpeechMs: number;
  totalSilenceMs: number;
  totalBreathMs: number;
  totalNoiseMs: number;
}

function computeOverallStats(waveform: WaveformPoint[], classified: ClassifiedRegion[]): AudioStats {
  let rmsSum = 0;
  let peak = -96;
  const sortedRms = waveform.map((p) => p.rmsDbfs).sort((a, b) => a - b);

  for (const point of waveform) {
    // RMS of RMS values (convert back to linear, average, convert back to dB)
    const linear = Math.pow(10, point.rmsDbfs / 20);
    rmsSum += linear * linear;
    if (point.peakDbfs > peak) peak = point.peakDbfs;
  }

  const overallRms = Math.sqrt(rmsSum / waveform.length);
  const overallRmsDbfs = overallRms > 0 ? Math.round(20 * Math.log10(overallRms) * 10) / 10 : -96;

  // Noise floor: 10th percentile of RMS values
  const noiseFloorIdx = Math.floor(sortedRms.length * 0.1);
  const noiseFloorDbfs = sortedRms[noiseFloorIdx] ?? -96;

  const stats: Record<Classification, number> = { SPEECH: 0, SILENCE: 0, BREATH: 0, NOISE: 0 };
  for (const region of classified) {
    stats[region.classification] += region.durationMs;
  }

  return {
    overallRmsDbfs,
    peakDbfs: Math.round(peak * 10) / 10,
    noiseFloorDbfs: Math.round(noiseFloorDbfs * 10) / 10,
    dynamicRangeDb: Math.round((peak - noiseFloorDbfs) * 10) / 10,
    totalSpeechMs: stats.SPEECH,
    totalSilenceMs: stats.SILENCE,
    totalBreathMs: stats.BREATH,
    totalNoiseMs: stats.NOISE,
  };
}

// --- Format timestamp ---
function formatMs(ms: number): string {
  const m = Math.floor(ms / 60000);
  const s = (ms % 60000) / 1000;
  return `${m}:${s.toFixed(3).padStart(6, '0')}`;
}

// --- Build output markdown ---
function buildOutput(
  videoFile: string,
  durationSec: number,
  silenceRegions: SilenceRegion[],
  vadResult: VADResult,
  boundaryDetail: BoundaryDetail[],
  classified: ClassifiedRegion[],
  stats: AudioStats,
): string {
  const date = new Date().toISOString().split('T')[0];
  const durationMs = Math.round(durationSec * 1000);

  let md = `---
sourceVideo: '${basename(videoFile)}'
duration: '${formatMs(durationMs)}'
analysisDate: '${date}'
silenceThreshold: '${SILENCE_THRESHOLD_DB} dBFS'
vadModel: 'Silero VAD v5 (ONNX)'
sampleRate: ${SAMPLE_RATE}
windowMs: ${WINDOW_MS}
denoised: true
denoiseConfig: 'highpass ${HIGHPASS_FREQ}Hz + arnndn RNNoise (mix=${DENOISE_MIX})'
---

# Audio Analysis: ${basename(videoFile)}

## Section 1 — Audio Metadata

| Field | Value |
|-------|-------|
| **Source Video** | ${basename(videoFile)} |
| **Duration** | ${formatMs(durationMs)} (${durationSec.toFixed(1)}s) |
| **Sample Rate** | ${SAMPLE_RATE} Hz (mono) |
| **Analysis Date** | ${date} |
| **Overall RMS** | ${stats.overallRmsDbfs} dBFS |
| **Peak Level** | ${stats.peakDbfs} dBFS |
| **Noise Floor** | ${stats.noiseFloorDbfs} dBFS |
| **Dynamic Range** | ${stats.dynamicRangeDb} dB |
| **Total Speech** | ${formatMs(stats.totalSpeechMs)} (${Math.round(stats.totalSpeechMs / durationMs * 100)}%) |
| **Total Silence** | ${formatMs(stats.totalSilenceMs)} (${Math.round(stats.totalSilenceMs / durationMs * 100)}%) |
| **Total Breath** | ${formatMs(stats.totalBreathMs)} (${Math.round(stats.totalBreathMs / durationMs * 100)}%) |
| **Total Noise** | ${formatMs(stats.totalNoiseMs)} (${Math.round(stats.totalNoiseMs / durationMs * 100)}%) |

## Section 2 — Silence Regions

| # | Start (ms) | End (ms) | Duration (ms) |
|---|-----------|---------|--------------|
`;

  silenceRegions.forEach((r, i) => {
    md += `| ${i + 1} | ${r.startMs} | ${r.endMs} | ${r.durationMs} |\n`;
  });

  md += `\n## Section 3 — VAD Speech Regions\n\n`;
  md += `| # | Start (ms) | End (ms) | Duration (ms) | Avg Probability |\n`;
  md += `|---|-----------|---------|--------------|----------------|\n`;

  vadResult.regions.forEach((r, i) => {
    md += `| ${i + 1} | ${r.startMs} | ${r.endMs} | ${r.durationMs} | ${r.avgProbability} |\n`;
  });

  // Speech Boundary Detail — 20ms resolution at speech onset/offset (±150ms window)
  md += `\n## Section 4 — Speech Boundary Detail (20ms resolution at onset/offset)\n\n`;
  md += `> Only shows ±${BOUNDARY_WINDOW_MS}ms around each speech region boundary. Full waveform data available in the JSON sidecar file.\n\n`;

  for (const bd of boundaryDetail) {
    md += `### Region ${bd.regionIdx + 1}: ${bd.startMs}–${bd.endMs}ms (SPEECH, ${bd.durationMs}ms)\n\n`;

    md += `**Onset:**\n\n`;
    md += `| Time (ms) | RMS dBFS | Peak dBFS | VAD |\n`;
    md += `|----------|---------|----------|-----|\n`;
    for (const p of bd.onset) {
      md += `| ${p.timeMs} | ${p.rmsDbfs} | ${p.peakDbfs} | ${p.vadProb} |\n`;
    }

    md += `\n**Offset:**\n\n`;
    md += `| Time (ms) | RMS dBFS | Peak dBFS | VAD |\n`;
    md += `|----------|---------|----------|-----|\n`;
    for (const p of bd.offset) {
      md += `| ${p.timeMs} | ${p.rmsDbfs} | ${p.peakDbfs} | ${p.vadProb} |\n`;
    }
    md += `\n`;
  }

  md += `\n## Section 5 — Classified Regions\n\n`;
  md += `| # | Start (ms) | End (ms) | Duration (ms) | Classification | Confidence | Avg dB | VAD Prob |\n`;
  md += `|---|-----------|---------|--------------|---------------|-----------|--------|----------|\n`;

  classified.forEach((r, i) => {
    md += `| ${i + 1} | ${r.startMs} | ${r.endMs} | ${r.durationMs} | ${r.classification} | ${r.confidence} | ${r.avgDb} | ${r.vadProb} |\n`;
  });

  return md;
}

// --- Transcript Parsing & Pre-Filtering ---
interface TranscriptWord {
  start: number; // seconds
  end: number;   // seconds
  word: string;
}

interface TranscriptSegment {
  start: string; // M:SS format
  end: string;
  text: string;
}

interface ParsedTranscript {
  words: TranscriptWord[];
  segments: TranscriptSegment[];
  fullText: string;
  metadata: Record<string, string>;
}

/** Convert timestamp string to seconds. Handles both "2.560" and "0:02.560" / "1:30.500" formats. */
function parseTimestamp(ts: string): number {
  if (ts.includes(':')) {
    const [minPart, secPart] = ts.split(':');
    return parseInt(minPart, 10) * 60 + parseFloat(secPart);
  }
  return parseFloat(ts);
}

function parseTranscript(transcriptPath: string): ParsedTranscript {
  const content = readFileSync(transcriptPath, 'utf-8');
  const lines = content.split('\n');

  const metadata: Record<string, string> = {};
  const words: TranscriptWord[] = [];
  const segments: TranscriptSegment[] = [];
  let fullText = '';

  let section: 'none' | 'frontmatter' | 'full-transcript' | 'segments' | 'words' = 'none';
  let inFrontmatter = false;

  for (const line of lines) {
    // Frontmatter detection
    if (line.trim() === '---') {
      if (!inFrontmatter) {
        inFrontmatter = true;
        section = 'frontmatter';
        continue;
      } else {
        inFrontmatter = false;
        section = 'none';
        continue;
      }
    }

    if (section === 'frontmatter') {
      const match = line.match(/^(\w+):\s*'?(.+?)'?\s*$/);
      if (match) metadata[match[1]] = match[2];
      continue;
    }

    // Section detection
    if (line.startsWith('## Full Transcript')) { section = 'full-transcript'; continue; }
    if (line.startsWith('## Timestamped Segments')) { section = 'segments'; continue; }
    if (line.startsWith('## Word-Level Timestamps')) { section = 'words'; continue; }
    if (line.startsWith('## ') && section !== 'none') { section = 'none'; continue; }

    // Skip table headers and separators
    if (line.trim().startsWith('| Start') || line.trim().startsWith('| Field') || line.trim().startsWith('|---')) continue;

    if (section === 'full-transcript') {
      const trimmed = line.trim();
      if (trimmed) fullText += (fullText ? ' ' : '') + trimmed;
    }

    if (section === 'words') {
      // Support both plain float (2.560) and M:SS.mmm (0:02.560) timestamp formats
      const match = line.match(/^\|\s*([\d:.]+)\s*\|\s*([\d:.]+)\s*\|\s*(.+?)\s*\|/);
      if (match) {
        words.push({
          start: parseTimestamp(match[1]),
          end: parseTimestamp(match[2]),
          word: match[3].trim(),
        });
      }
    }

    if (section === 'segments') {
      // Support both M:SS and M:SS.mmm timestamp formats
      const match = line.match(/^\|\s*([\d:.]+)\s*\|\s*([\d:.]+)\s*\|\s*(.+?)\s*\|/);
      if (match) {
        segments.push({
          start: match[1],
          end: match[2],
          text: match[3].trim(),
        });
      }
    }
  }

  return { words, segments, fullText, metadata };
}

function buildPreFilteredTranscript(
  videoFile: string,
  transcriptPath: string,
  outputPath: string,
  transcript: ParsedTranscript,
  classified: ClassifiedRegion[],
  totalDurationMs: number,
): void {
  console.log('\nGenerating pre-filtered transcript...');

  const date = new Date().toISOString().split('T')[0];
  const originalWordCount = transcript.words.length;

  // Classify each word as kept or removed based on which classified region it falls in
  const keptWords: TranscriptWord[] = [];
  const removedWords: TranscriptWord[] = [];

  for (const word of transcript.words) {
    const wordMidMs = ((word.start + word.end) / 2) * 1000;
    // Find the classified region this word falls in
    let inSpeech = false;
    for (const region of classified) {
      if (wordMidMs >= region.startMs && wordMidMs < region.endMs) {
        inSpeech = region.classification === 'SPEECH';
        break;
      }
    }
    if (inSpeech) {
      keptWords.push(word);
    } else {
      removedWords.push(word);
    }
  }

  const filteredWordCount = keptWords.length;
  const reduction = originalWordCount > 0
    ? Math.round((1 - filteredWordCount / originalWordCount) * 100)
    : 0;

  // Compute durations by classification
  let silenceCount = 0, silenceDurMs = 0;
  let breathCount = 0, breathDurMs = 0;
  let noiseCount = 0, noiseDurMs = 0;
  let speechDurMs = 0;
  let gapMarkerCount = 0;

  for (const region of classified) {
    switch (region.classification) {
      case 'SPEECH': speechDurMs += region.durationMs; break;
      case 'SILENCE': silenceCount++; silenceDurMs += region.durationMs; break;
      case 'BREATH': breathCount++; breathDurMs += region.durationMs; break;
      case 'NOISE': noiseCount++; noiseDurMs += region.durationMs; break;
    }
  }

  // Build full transcript with gap markers
  // Walk through classified regions in order; for SPEECH regions, emit words; for non-SPEECH, emit gap markers
  let filteredFullText = '';
  let wordIdx = 0;

  for (const region of classified) {
    if (region.classification === 'SPEECH') {
      // Emit all kept words that fall within this speech region
      while (wordIdx < transcript.words.length) {
        const word = transcript.words[wordIdx];
        const wordMidMs = ((word.start + word.end) / 2) * 1000;
        if (wordMidMs >= region.endMs) break;
        if (wordMidMs >= region.startMs) {
          filteredFullText += (filteredFullText.length > 0 && !filteredFullText.endsWith('\n') ? ' ' : '') + word.word;
        }
        wordIdx++;
      }
    } else {
      // Non-speech region — emit gap marker if duration is significant (≥300ms)
      if (region.durationMs >= 300) {
        const durationSec = (region.durationMs / 1000).toFixed(1);
        const types: string[] = [];
        if (region.classification === 'SILENCE') types.push('silence');
        if (region.classification === 'BREATH') types.push('breath');
        if (region.classification === 'NOISE') types.push('noise');
        filteredFullText += ` [--- ${durationSec}s removed: ${types.join('/')} ---] `;
        gapMarkerCount++;
      }
      // Skip words that fall in non-speech regions
      while (wordIdx < transcript.words.length) {
        const word = transcript.words[wordIdx];
        const wordMidMs = ((word.start + word.end) / 2) * 1000;
        if (wordMidMs >= region.endMs) break;
        wordIdx++;
      }
    }
  }

  // Build filtered segment table
  // Re-derive segments from kept words, grouping by gaps
  const filteredSegments: Array<{ start: number; end: number; text: string }> = [];
  let segStart = -1;
  let segEnd = -1;
  let segWords: string[] = [];

  for (let i = 0; i < keptWords.length; i++) {
    const word = keptWords[i];
    if (segStart < 0) {
      segStart = word.start;
      segEnd = word.end;
      segWords = [word.word];
    } else if (word.start - segEnd > 1.0) {
      // Gap > 1 second — new segment
      filteredSegments.push({ start: segStart, end: segEnd, text: segWords.join(' ') });
      segStart = word.start;
      segEnd = word.end;
      segWords = [word.word];
    } else {
      segEnd = word.end;
      segWords.push(word.word);
    }
  }
  if (segWords.length > 0) {
    filteredSegments.push({ start: segStart, end: segEnd, text: segWords.join(' ') });
  }

  // Build output markdown
  let md = `---
sourceVideo: '${basename(videoFile)}'
originalTranscript: '${basename(transcriptPath)}'
audioAnalysis: '${basename(outputPath)}'
filterDate: '${date}'
---

# Pre-Filtered Transcript: ${basename(videoFile)}

## Filter Summary
| Metric | Value |
|--------|-------|
| Original Word Count | ${originalWordCount} |
| Filtered Word Count | ${filteredWordCount} |
| Reduction | ${reduction}% |
| Original Duration | ${formatMs(totalDurationMs)} |
| Speech Duration | ${formatMs(speechDurMs)} |
| Removed Duration | ${formatMs(silenceDurMs + breathDurMs + noiseDurMs)} |
| Silence Removed | ${silenceCount} regions (${formatMs(silenceDurMs)}) |
| Breath Removed | ${breathCount} regions (${formatMs(breathDurMs)}) |
| Noise Removed | ${noiseCount} regions (${formatMs(noiseDurMs)}) |
| Gap Markers | ${gapMarkerCount} |

## Full Transcript (Filtered)
${filteredFullText.trim()}

## Timestamped Segments (Filtered)
| Start | End | Text |
|-------|-----|------|
`;

  for (const seg of filteredSegments) {
    md += `| ${seg.start.toFixed(2)} | ${seg.end.toFixed(2)} | ${seg.text} |\n`;
  }

  md += `\n## Word-Level Timestamps (Filtered)\n| Start | End | Word |\n|-------|-----|------|\n`;
  for (const word of keptWords) {
    md += `| ${word.start.toFixed(2)} | ${word.end.toFixed(2)} | ${word.word} |\n`;
  }

  // Write pre-filtered transcript
  const preFilterPath = join(
    dirname(outputPath),
    `${basename(outputPath, extname(outputPath)).replace('-audio-analysis', '')}-pre-filtered-transcript.md`,
  );
  writeFileSync(preFilterPath, md, 'utf-8');

  console.log(`Pre-filtered transcript written to: ${preFilterPath}`);
  console.log(`  Original words: ${originalWordCount}, Filtered words: ${filteredWordCount} (${reduction}% reduction)`);
  console.log(`  Speech: ${formatMs(speechDurMs)}, Removed: ${formatMs(silenceDurMs + breathDurMs + noiseDurMs)}`);
  console.log(`  Gap markers: ${gapMarkerCount}`);
  console.log(`  File size: ${(statSync(preFilterPath).size / 1024).toFixed(1)} KB`);
}

// --- Build audio-analysis.json (deterministic, no LLM parsing needed) ---
function buildAnalysisJson(
  video: string,
  durationSec: number,
  contentType: string,
  denoised: boolean,
  silenceRegions: SilenceRegion[],
  vadResult: VADResult,
  boundaryDetail: BoundaryDetail[],
  classified: ClassifiedRegion[],
  stats: AudioStats,
  fillerRegions: FillerRegion[],
): Record<string, unknown> {
  const durationMs = Math.round(durationSec * 1000);
  return {
    source_file: basename(video),
    source_path: video,
    content_type: contentType,
    analysis_date: new Date().toISOString(),
    workflowType: 'audio-analysis',
    sample_rate: SAMPLE_RATE,
    denoised,
    denoise_config: denoised ? { highpass_hz: HIGHPASS_FREQ, arnndn_mix: DENOISE_MIX, model: 'std.rnnn' } : null,
    audio_metadata: {
      duration_ms: durationMs,
      overall_rms_dbfs: stats.overallRmsDbfs,
      peak_dbfs: stats.peakDbfs,
      noise_floor_dbfs: stats.noiseFloorDbfs,
      dynamic_range_db: stats.dynamicRangeDb,
      total_speech_ms: stats.totalSpeechMs,
      total_silence_ms: stats.totalSilenceMs,
      total_breath_ms: stats.totalBreathMs,
      total_noise_ms: stats.totalNoiseMs,
    },
    silence_regions: silenceRegions,
    speech_regions: vadResult.regions.map((r) => ({
      startMs: r.startMs,
      endMs: r.endMs,
      durationMs: r.durationMs,
      avgProbability: r.avgProbability,
    })),
    speech_boundary_detail: boundaryDetail.map((bd) => ({
      regionIdx: bd.regionIdx,
      startMs: bd.startMs,
      endMs: bd.endMs,
      durationMs: bd.durationMs,
      onset: bd.onset,
      offset: bd.offset,
    })),
    classified_regions: classified,
    filler_regions: fillerRegions,
  };
}

// --- Main ---
async function main() {
  const { video, output, transcript: transcriptPath, denoise, contentType } = parseArgs();
  const duration = getVideoDuration(video);

  console.log(`Video: ${video}`);
  console.log(`Duration: ${duration.toFixed(1)}s`);
  console.log(`Content type: ${contentType}`);
  console.log(`Denoising: ${denoise ? 'enabled' : 'disabled'}`);
  console.log();

  // Extract audio as WAV (base format for all processing)
  console.log('Extracting audio...');
  const wavPath = extractWavAudio(video);
  console.log('  WAV extracted.');

  const tempFiles: string[] = [wavPath];

  try {
    // Denoise audio for analysis (timestamps remain aligned to original)
    let analysisPath = wavPath;
    if (denoise) {
      console.log('Denoising audio for analysis...');
      const denoisedPath = denoiseAudio(wavPath);
      if (denoisedPath !== wavPath) {
        analysisPath = denoisedPath;
        tempFiles.push(denoisedPath);
      }
    }

    // Extract raw PCM from analysis audio (for waveform computation)
    const rawPath = extractRawAudio(analysisPath);
    tempFiles.push(rawPath);
    console.log();

    // Layer 1: Silence detection on analysis audio (denoised if enabled)
    const silenceRegions = runSilenceDetect(analysisPath);

    // Layer 2: dB waveform from analysis PCM
    const waveform = computeWaveform(rawPath);

    // Layer 3: Silero VAD on analysis audio
    const vadResult = runVAD(analysisPath);

    // Overlay VAD probabilities onto waveform points
    overlayVADOnWaveform(waveform, vadResult);

    // Cross-reference and classify
    const totalDurationMs = Math.round(duration * 1000);
    console.log('\nCross-referencing layers and classifying regions...');
    const classified = classifyRegions(silenceRegions, waveform, vadResult, totalDurationMs);

    const speechRegions = classified.filter((r) => r.classification === 'SPEECH');
    const breathRegions = classified.filter((r) => r.classification === 'BREATH');
    const silentRegions = classified.filter((r) => r.classification === 'SILENCE');
    const noiseRegions = classified.filter((r) => r.classification === 'NOISE');

    console.log(`  SPEECH: ${speechRegions.length} regions`);
    console.log(`  SILENCE: ${silentRegions.length} regions`);
    console.log(`  BREATH: ${breathRegions.length} regions`);
    console.log(`  NOISE: ${noiseRegions.length} regions`);

    // Compute boundary detail for speech regions
    const boundaryDetail = computeBoundaryDetail(classified, waveform);
    console.log(`  Boundary detail computed for ${boundaryDetail.length} speech regions.`);

    // Compute overall stats
    const stats = computeOverallStats(waveform, classified);

    // Extract filler regions from transcript (if provided)
    let fillerRegions: FillerRegion[] = [];
    let parsedTranscript: ParsedTranscript | null = null;
    if (transcriptPath) {
      parsedTranscript = parseTranscript(transcriptPath);
      if (parsedTranscript.words.length > 0) {
        fillerRegions = extractFillerRegions(parsedTranscript);
        console.log(`  Filler words detected: ${fillerRegions.length}`);
      }
    }

    // Build and write markdown output (human-readable)
    console.log('\nBuilding output...');
    const md = buildOutput(video, duration, silenceRegions, vadResult, boundaryDetail, classified, stats);
    writeFileSync(output, md, 'utf-8');
    console.log(`\nMarkdown analysis written to: ${output}`);
    console.log(`  File size: ${(statSync(output).size / 1024).toFixed(1)} KB`);

    // Write audio-analysis.json (deterministic, directly consumable by clipping workflow)
    const jsonPath = join(dirname(output), `${basename(output, extname(output))}.json`);
    const analysisJson = buildAnalysisJson(
      video, duration, contentType, denoise, silenceRegions, vadResult, boundaryDetail, classified, stats, fillerRegions,
    );
    writeFileSync(jsonPath, JSON.stringify(analysisJson, null, 2), 'utf-8');
    console.log(`JSON analysis written to: ${jsonPath}`);
    console.log(`  JSON size: ${(statSync(jsonPath).size / 1024).toFixed(1)} KB`);

    // Write JSON sidecar with full-resolution waveform data
    const sidecarPath = join(dirname(output), `${basename(output, extname(output))}-sidecar.json`);
    const sidecar = JSON.stringify({
      waveform,
      classifiedRegions: classified,
      vadRegions: vadResult.regions,
      vadProbabilities: vadResult.probabilities,
      fillerRegions,
      contentType,
      denoised: denoise,
    });
    writeFileSync(sidecarPath, sidecar, 'utf-8');
    console.log(`JSON sidecar written to: ${sidecarPath}`);
    console.log(`  Sidecar size: ${(statSync(sidecarPath).size / 1024).toFixed(1)} KB`);

    // Pre-filtered transcript (if --transcript flag provided)
    if (parsedTranscript && parsedTranscript.words.length > 0) {
      buildPreFilteredTranscript(video, transcriptPath!, output, parsedTranscript, classified, totalDurationMs);
    } else if (transcriptPath) {
      console.error('\nWarning: No word-level timestamps found in transcript. Skipping pre-filtered output.');
    }
  } finally {
    // Clean up all temp files
    for (const f of tempFiles) {
      try { unlinkSync(f); } catch { /* ignore */ }
    }
  }

  console.log('Done!');
}

main().catch((err) => {
  console.error('Fatal error:', err);
  process.exit(1);
});
