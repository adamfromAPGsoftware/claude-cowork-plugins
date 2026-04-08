"""
Silero VAD wrapper — outputs speech regions and per-frame probabilities as JSON.
Uses the official silero-vad pip package (v6+).

Usage: python3 vad.py <audio.wav>

Dependencies: pip3 install silero-vad

The model is auto-downloaded and cached by the silero-vad package on first run.
"""

import sys
import json
import os
import torch

torch.set_num_threads(1)

SAMPLE_RATE = 16000
WINDOW_SIZE_SAMPLES = 512  # 32ms at 16kHz


def main():
    if len(sys.argv) < 2:
        print("Usage: python3 vad.py <audio.wav>", file=sys.stderr)
        sys.exit(1)

    audio_path = sys.argv[1]
    if not os.path.exists(audio_path):
        print(f"Error: Audio file not found: {audio_path}", file=sys.stderr)
        sys.exit(1)

    try:
        from silero_vad import load_silero_vad, read_audio, get_speech_timestamps
    except ImportError:
        print("Error: silero-vad not installed. Run: pip3 install silero-vad", file=sys.stderr)
        sys.exit(1)

    # Load model (auto-downloads and caches on first run)
    print("Loading Silero VAD model...", file=sys.stderr)
    model = load_silero_vad()

    # Read audio (handles resampling to 16kHz automatically)
    print(f"Reading audio: {audio_path}", file=sys.stderr)
    try:
        wav = read_audio(audio_path, sampling_rate=SAMPLE_RATE)
    except Exception as e:
        # Fallback: read WAV directly with wave module (audio is already 16kHz mono from ffmpeg)
        print(f"read_audio failed ({e}), falling back to direct WAV reading...", file=sys.stderr)
        import wave
        import numpy as np
        with wave.open(audio_path, "rb") as wf:
            raw = wf.readframes(wf.getnframes())
        samples = np.frombuffer(raw, dtype=np.int16).astype(np.float32) / 32768.0
        wav = torch.from_numpy(samples)
    duration = len(wav) / SAMPLE_RATE
    print(f"Audio duration: {duration:.1f}s ({len(wav)} samples)", file=sys.stderr)

    # Get speech timestamps using the official API
    speech_timestamps = get_speech_timestamps(
        wav,
        model,
        sampling_rate=SAMPLE_RATE,
        return_seconds=False,  # get sample-level precision
        threshold=0.5,
        min_speech_duration_ms=250,
        min_silence_duration_ms=100,
    )

    # Convert sample timestamps to seconds for the speech regions
    speech_regions = []
    for ts in speech_timestamps:
        start_sec = ts["start"] / SAMPLE_RATE
        end_sec = ts["end"] / SAMPLE_RATE
        speech_regions.append({
            "start": round(start_sec, 4),
            "end": round(end_sec, 4),
            "probability": 0.9,  # get_speech_timestamps only returns regions above threshold
        })

    print(f"Found {len(speech_regions)} speech regions.", file=sys.stderr)

    # Compute per-frame probabilities by running the model directly on chunks
    print("Computing per-frame probabilities...", file=sys.stderr)
    model.reset_states()
    frame_probabilities = []
    total_samples = len(wav)

    for i in range(0, total_samples, WINDOW_SIZE_SAMPLES):
        chunk = wav[i : i + WINDOW_SIZE_SAMPLES]
        if len(chunk) < WINDOW_SIZE_SAMPLES:
            # Pad the last chunk
            chunk = torch.nn.functional.pad(chunk, (0, WINDOW_SIZE_SAMPLES - len(chunk)))

        # Get speech probability for this chunk
        speech_prob = model(chunk, SAMPLE_RATE).item()
        time_sec = i / SAMPLE_RATE
        frame_probabilities.append({
            "time": round(time_sec, 4),
            "probability": round(speech_prob, 4),
        })

    # Refine speech region probabilities using frame data
    for region in speech_regions:
        start_sample = int(region["start"] * SAMPLE_RATE)
        end_sample = int(region["end"] * SAMPLE_RATE)
        probs_in_region = [
            fp["probability"] for fp in frame_probabilities
            if fp["time"] >= region["start"] and fp["time"] <= region["end"]
        ]
        if probs_in_region:
            region["probability"] = round(sum(probs_in_region) / len(probs_in_region), 4)

    print(f"Computed {len(frame_probabilities)} frame probabilities.", file=sys.stderr)

    # Output JSON to stdout
    result = {
        "speech_regions": speech_regions,
        "frame_probabilities": frame_probabilities,
    }
    print(json.dumps(result))


if __name__ == "__main__":
    main()
