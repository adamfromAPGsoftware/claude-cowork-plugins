#!/usr/bin/env python3
"""
Run VSL production analysis via OpenRouter (Gemini 3 Pro).

Extracts frames at target FPS using FFmpeg, base64-encodes them,
and sends to OpenRouter for detailed production technique analysis.

Usage:
  # Pass A: Opening (first 2 min at 1.0 fps)
  python run-vsl-analysis.py --video apg-vsl-opening.mp4 --pass opening --fps 1.0

  # Pass B: Full video (at 0.2 fps)
  python run-vsl-analysis.py --video apg-vsl-full.mp4 --pass full --fps 0.2

  # Merge both passes
  python run-vsl-analysis.py --merge

  # All-in-one
  python run-vsl-analysis.py --all
"""
from __future__ import annotations

import argparse
import base64
import json
import os
import subprocess
import sys
import tempfile
import time
from pathlib import Path

SCRIPT_DIR = Path(__file__).parent
PROMPT_FILE = SCRIPT_DIR / "vsl-production-analysis-prompt.md"
MODEL = "google/gemini-3.1-pro-preview"
OPENROUTER_URL = "https://openrouter.ai/api/v1/chat/completions"

OPENING_VIDEO = "apg-vsl-opening.mp4"
FULL_VIDEO = "apg-vsl-full.mp4"
OUTPUT_PREFIX = "apg-vsl"


def get_api_key() -> str:
    key = os.environ.get("OPENROUTER_API_KEY")
    if key:
        return key
    for parent in Path(__file__).resolve().parents:
        env_file = parent / ".env"
        if env_file.exists():
            for line in env_file.read_text().splitlines():
                if line.startswith("OPENROUTER_API_KEY="):
                    return line.split("=", 1)[1].strip().strip('"').strip("'")
    print("ERROR: No OPENROUTER_API_KEY found", file=sys.stderr)
    sys.exit(1)


def load_prompt() -> str:
    """Load the analysis prompt, extracting the system prompt and analysis sections."""
    text = PROMPT_FILE.read_text()
    # Extract from "## System Prompt for Gemini" to "## Output Format" end
    start = text.find("## System Prompt for Gemini")
    if start == -1:
        # Fallback: use everything after the purpose section
        start = text.find("You are a world-class")
        if start == -1:
            start = 0
    # Get everything from system prompt through analysis sections and output format
    end = text.find("## API Configuration")
    if end == -1:
        end = len(text)
    return text[start:end].strip()


def extract_frames(video_path: Path, fps: float, max_frames: int = 300) -> list[str]:
    """Extract frames at target FPS, return as base64-encoded JPEG strings."""
    with tempfile.TemporaryDirectory() as tmpdir:
        cmd = [
            "ffmpeg", "-y", "-i", str(video_path),
            "-vf", f"fps={fps},scale=1280:720",
            "-q:v", "4",  # JPEG quality (2=best, 31=worst)
            "-frames:v", str(max_frames),
            f"{tmpdir}/frame_%05d.jpg"
        ]
        subprocess.run(cmd, capture_output=True, check=True)

        frames = []
        for frame_file in sorted(Path(tmpdir).glob("frame_*.jpg")):
            data = frame_file.read_bytes()
            b64 = base64.standard_b64encode(data).decode("ascii")
            frames.append(b64)

        return frames


def call_openrouter(api_key: str, prompt: str, frames: list[str], pass_name: str) -> str:
    """Send frames + prompt to OpenRouter Gemini 3 Pro."""
    import urllib.request
    import urllib.error

    # Build content: frames first, then prompt text (best practice for Gemini)
    content = []

    # Add frame images
    for i, b64 in enumerate(frames):
        content.append({
            "type": "image_url",
            "image_url": {
                "url": f"data:image/jpeg;base64,{b64}"
            }
        })

    # Add analysis prompt
    pass_context = ""
    if pass_name == "opening":
        pass_context = (
            "\n\nThis is Pass A (Opening): First 2 minutes of a VSL at 1 frame/second. "
            "Focus on frame-level editing detail in the hook and opening sections. "
            "Be extremely precise with timestamps, transitions, and effects."
        )
    elif pass_name == "full":
        pass_context = (
            "\n\nThis is Pass B (Full): The entire VSL at 1 frame/5 seconds. "
            "Focus on overall section structure, section boundaries, graphic timing, "
            "pacing arc across the full video, and the complete motion graphic inventory."
        )

    content.append({
        "type": "text",
        "text": prompt + pass_context
    })

    payload = {
        "model": MODEL,
        "messages": [
            {
                "role": "user",
                "content": content
            }
        ],
        "max_tokens": 16000,
        "temperature": 0.3,
    }

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}",
        "HTTP-Referer": "https://{YOUR_DOMAIN}",
        "X-Title": "VSL Analysis"
    }

    data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(OPENROUTER_URL, data=data, headers=headers, method="POST")

    print(f"  Sending {len(frames)} frames to {MODEL}...")
    print(f"  Payload size: {len(data) / 1024 / 1024:.1f}MB")

    try:
        with urllib.request.urlopen(req, timeout=600) as resp:
            result = json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        error_body = e.read().decode("utf-8") if e.fp else "no body"
        print(f"  HTTP {e.code}: {error_body[:500]}", file=sys.stderr)
        sys.exit(1)

    if "choices" not in result or not result["choices"]:
        print(f"  Unexpected response: {json.dumps(result)[:500]}", file=sys.stderr)
        sys.exit(1)

    text = result["choices"][0]["message"]["content"]

    # Log usage
    usage = result.get("usage", {})
    print(f"  Tokens — prompt: {usage.get('prompt_tokens', '?')}, completion: {usage.get('completion_tokens', '?')}")

    return text


def run_pass(pass_name: str, api_key: str):
    """Run a single analysis pass."""
    if pass_name == "opening":
        video_path = SCRIPT_DIR / OPENING_VIDEO
        fps = 1.0
        max_frames = 150  # 2 min at 1fps = 120 frames, plus buffer
    elif pass_name == "full":
        video_path = SCRIPT_DIR / FULL_VIDEO
        fps = 0.2
        max_frames = 120  # ~8 min at 0.2fps = ~96 frames, plus buffer
    else:
        print(f"Unknown pass: {pass_name}", file=sys.stderr)
        sys.exit(1)

    if not video_path.exists():
        print(f"Video not found: {video_path}", file=sys.stderr)
        sys.exit(1)

    output_file = SCRIPT_DIR / f"{OUTPUT_PREFIX}-{pass_name}-analysis.md"

    print(f"\n=== Pass: {pass_name} ===")
    print(f"  Video: {video_path.name}")
    print(f"  FPS: {fps}")

    # Extract frames
    print(f"  Extracting frames at {fps} fps...")
    frames = extract_frames(video_path, fps, max_frames)
    print(f"  Extracted {len(frames)} frames")

    # Load prompt
    prompt = load_prompt()

    # Call API
    analysis = call_openrouter(api_key, prompt, frames, pass_name)

    # Save
    header = f"# VSL Production Analysis — Pass {'A (Opening)' if pass_name == 'opening' else 'B (Full)'}\n\n"
    header += f"*{pass_name.title()} pass: {'First 2 min @ 1fps' if pass_name == 'opening' else 'Full video @ 0.2fps'}*\n\n---\n\n"
    output_file.write_text(header + analysis)
    print(f"  Saved: {output_file.name}")


def merge_passes():
    """Merge opening and full analysis into a combined document."""
    opening_file = SCRIPT_DIR / f"{OUTPUT_PREFIX}-opening-analysis.md"
    full_file = SCRIPT_DIR / f"{OUTPUT_PREFIX}-full-analysis.md"
    output_file = SCRIPT_DIR / f"{OUTPUT_PREFIX}-production-analysis.md"

    if not opening_file.exists():
        print(f"Missing: {opening_file.name}", file=sys.stderr)
        sys.exit(1)
    if not full_file.exists():
        print(f"Missing: {full_file.name}", file=sys.stderr)
        sys.exit(1)

    opening_text = opening_file.read_text()
    full_text = full_file.read_text()

    merged = f"""# Production Analysis: VSL

*Combined from opening pass (2 min @ 1fps) and full pass (entire video @ 0.2fps)*

---

## Part A: Opening Detail (First 2 Minutes)

{opening_text}

---

## Part B: Full Structure

{full_text}
"""

    output_file.write_text(merged)
    print(f"\nMerged analysis saved: {output_file.name}")


def main():
    parser = argparse.ArgumentParser(description="Run VSL production analysis via OpenRouter")
    parser.add_argument("--video", help="Video file path (relative to script dir)")
    parser.add_argument("--pass", dest="pass_name", choices=["opening", "full"], help="Which analysis pass")
    parser.add_argument("--fps", type=float, help="Override FPS")
    parser.add_argument("--merge", action="store_true", help="Merge both passes into combined analysis")
    parser.add_argument("--all", action="store_true", help="Run both passes then merge")
    parser.add_argument("--api-key", help="OpenRouter API key (or set OPENROUTER_API_KEY)")
    args = parser.parse_args()

    if args.merge:
        merge_passes()
        return

    api_key = args.api_key or get_api_key()

    if args.all:
        run_pass("opening", api_key)
        print("\nWaiting 10s between passes...")
        time.sleep(10)
        run_pass("full", api_key)
        merge_passes()
        return

    if not args.pass_name:
        parser.error("Specify --pass (opening|full), --merge, or --all")

    run_pass(args.pass_name, api_key)


if __name__ == "__main__":
    main()
