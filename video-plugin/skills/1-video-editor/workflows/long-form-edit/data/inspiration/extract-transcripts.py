#!/usr/bin/env python3
"""
Extract word-level transcripts from YouTube tutorial audio using DeepGram Nova-3.

Usage:
  python extract-transcripts.py --video-id QoQBzR1NIqI
  python extract-transcripts.py --batch

Reads {folder}/full-audio.m4a files and produces {folder}/transcript.json with word-level timestamps.

Requires: DEEPGRAM_API_KEY env var or in .env file
"""
from __future__ import annotations

import argparse
import json
import os
import sys
import time
from pathlib import Path
from typing import Optional

SCRIPT_DIR = Path(__file__).parent
VIDEOS_FILE = SCRIPT_DIR / "videos.yaml"


def get_api_key(cli_key: str | None) -> str:
    """Resolve DeepGram API key from CLI arg, env var, or .env file."""
    if cli_key:
        return cli_key
    key = os.environ.get("DEEPGRAM_API_KEY")
    if key:
        return key
    for parent in Path(__file__).resolve().parents:
        env_file = parent / ".env"
        if env_file.exists():
            for line in env_file.read_text().splitlines():
                if line.startswith("DEEPGRAM_API_KEY="):
                    return line.split("=", 1)[1].strip().strip('"').strip("'")
    print("ERROR: No DEEPGRAM_API_KEY found (set env var, pass --api-key, or add to .env)", file=sys.stderr)
    sys.exit(1)


def load_videos() -> list[dict]:
    """Load video entries from videos.yaml."""
    import yaml
    data = yaml.safe_load(VIDEOS_FILE.read_text())
    return data["videos"]


def get_video_folder(video_id: str) -> str:
    """Look up the folder name for a video ID."""
    for v in load_videos():
        if v["id"] == video_id:
            return v["folder"]
    print(f"ERROR: Unknown video ID: {video_id}", file=sys.stderr)
    sys.exit(1)


def transcribe_audio(audio_path: Path, api_key: str) -> dict:
    """Send audio to DeepGram Nova-3 and return word-level transcript."""
    import httpx

    file_size_mb = audio_path.stat().st_size / 1024 / 1024
    print(f"  Uploading: {audio_path.parent.name}/full-audio.m4a ({file_size_mb:.1f} MB)")

    url = "https://api.deepgram.com/v1/listen"
    params = {
        "model": "nova-3",
        "smart_format": "true",
        "punctuate": "true",
        "paragraphs": "true",
        "utterances": "true",
        "diarize": "true",
        "language": "en",
    }
    headers = {
        "Authorization": f"Token {api_key}",
        "Content-Type": "audio/mp4",
    }

    with open(audio_path, "rb") as f:
        audio_bytes = f.read()

    print(f"  Sending to DeepGram Nova-3 ({file_size_mb:.1f} MB)...")

    # Use a long timeout for large files
    timeout = max(300, file_size_mb * 10)
    response = httpx.post(
        url,
        params=params,
        headers=headers,
        content=audio_bytes,
        timeout=timeout,
    )

    if response.status_code != 200:
        print(f"ERROR: DeepGram returned {response.status_code}: {response.text}", file=sys.stderr)
        sys.exit(1)

    return response.json()


def extract_word_timestamps(dg_response: dict) -> dict:
    """Extract structured word-level transcript from DeepGram response."""
    results = dg_response.get("results", {})
    channels = results.get("channels", [])
    if not channels:
        return {"words": [], "paragraphs": [], "metadata": {}}

    channel = channels[0]
    alternatives = channel.get("alternatives", [])
    if not alternatives:
        return {"words": [], "paragraphs": [], "metadata": {}}

    alt = alternatives[0]

    # Word-level data
    words = []
    for w in alt.get("words", []):
        words.append({
            "word": w["word"],
            "start": round(w["start"], 3),
            "end": round(w["end"], 3),
            "confidence": round(w.get("confidence", 0), 3),
            "speaker": w.get("speaker"),
            "punctuated_word": w.get("punctuated_word", w["word"]),
        })

    # Paragraph-level data
    paragraphs = []
    para_data = alt.get("paragraphs", {}).get("paragraphs", [])
    for p in para_data:
        sentences = []
        for s in p.get("sentences", []):
            sentences.append({
                "text": s["text"],
                "start": round(s["start"], 3),
                "end": round(s["end"], 3),
            })
        paragraphs.append({
            "speaker": p.get("speaker"),
            "start": round(p["start"], 3),
            "end": round(p["end"], 3),
            "sentences": sentences,
        })

    # Full transcript text
    transcript_text = alt.get("transcript", "")

    # Metadata
    metadata = {
        "duration": results.get("metadata", {}).get("duration"),
        "channels": results.get("metadata", {}).get("channels"),
        "model": results.get("metadata", {}).get("model_info", {}).get("name"),
        "word_count": len(words),
        "paragraph_count": len(paragraphs),
    }

    return {
        "transcript": transcript_text,
        "words": words,
        "paragraphs": paragraphs,
        "metadata": metadata,
    }


def process_video(video_id: str, api_key: str) -> None:
    """Transcribe a single video's audio."""
    folder = get_video_folder(video_id)
    video_dir = SCRIPT_DIR / folder
    audio_path = video_dir / "full-audio.m4a"
    output_path = video_dir / "transcript.json"

    if output_path.exists():
        print(f"  SKIP: {folder}/transcript.json already exists (delete to re-run)")
        return

    if not audio_path.exists():
        print(f"ERROR: Audio not found: {audio_path}", file=sys.stderr)
        print(f"  Run: bash download-videos.sh --video-id {video_id}", file=sys.stderr)
        sys.exit(1)

    dg_response = transcribe_audio(audio_path, api_key)
    result = extract_word_timestamps(dg_response)

    output_path.write_text(json.dumps(result, indent=2, ensure_ascii=False))
    word_count = result["metadata"].get("word_count", 0)
    duration = result["metadata"].get("duration") or 0
    print(f"  OK: {folder}/transcript.json ({word_count} words, {duration:.0f}s duration)")


def main():
    parser = argparse.ArgumentParser(description="Extract word-level transcripts via DeepGram Nova-3")
    parser.add_argument("--video-id", help="YouTube video ID (e.g., QoQBzR1NIqI)")
    parser.add_argument("--batch", action="store_true", help="Process all videos from videos.yaml")
    parser.add_argument("--api-key", default=None, help="DeepGram API key (or set DEEPGRAM_API_KEY)")
    args = parser.parse_args()

    if not args.batch and not args.video_id:
        parser.error("Either --video-id or --batch is required")

    api_key = get_api_key(args.api_key)

    if args.batch:
        videos = load_videos()
        for i, v in enumerate(videos):
            print(f"\n[{i + 1}/{len(videos)}] Transcribing {v['folder']}...")
            process_video(v["id"], api_key)
            if i < len(videos) - 1:
                print("  Waiting 5s before next API call...")
                time.sleep(5)
    else:
        folder = get_video_folder(args.video_id)
        print(f"\nTranscribing {folder}...")
        process_video(args.video_id, api_key)

    print("\nDone!")


if __name__ == "__main__":
    main()
