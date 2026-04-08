#!/usr/bin/env python3
"""
Run Gemini 3.1 Pro narrative production analysis on a single Instagram Reel.
Usage: python run-narrative-analysis.py <shortcode> [--video-dir DIR] [--prompt-file FILE]
"""
import argparse
import sys
from pathlib import Path

def main():
    parser = argparse.ArgumentParser(description="Run Gemini narrative analysis on an Instagram Reel")
    parser.add_argument("shortcode", help="Instagram shortcode (e.g., DRXZJeHiAES)")
    parser.add_argument("--video-dir", default=str(Path(__file__).parent), help="Directory containing video files")
    parser.add_argument("--prompt-file", default=str(Path(__file__).parent.parent / "production-analysis-narrative-prompt.md"), help="Path to prompt file")
    parser.add_argument("--api-key", default=None, help="Gemini API key (or set GEMINI_API_KEY env var)")
    args = parser.parse_args()

    import os

    # Get API key
    api_key = args.api_key or os.environ.get("GEMINI_API_KEY")
    if not api_key:
        # Try loading from .env
        env_path = Path(__file__).resolve()
        # Walk up to find .env
        for parent in env_path.parents:
            env_file = parent / ".env"
            if env_file.exists():
                for line in env_file.read_text().splitlines():
                    if line.startswith("GEMINI_API_KEY="):
                        api_key = line.split("=", 1)[1].strip()
                        break
                if api_key:
                    break

    if not api_key:
        print("ERROR: No GEMINI_API_KEY found", file=sys.stderr)
        sys.exit(1)

    # Check video file
    video_path = Path(args.video_dir) / f"{args.shortcode}.mp4"
    if not video_path.exists():
        print(f"ERROR: Video not found: {video_path}", file=sys.stderr)
        sys.exit(1)

    # Load prompt — extract sections between "## System Prompt" and "## API Configuration"
    prompt_path = Path(args.prompt_file)
    prompt_text = prompt_path.read_text()

    # Extract the analysis prompt (system prompt + analysis sections + output format)
    start_marker = "## System Prompt for Gemini"
    end_marker = "## API Configuration"
    start_idx = prompt_text.find(start_marker)
    end_idx = prompt_text.find(end_marker)

    if start_idx == -1 or end_idx == -1:
        print("ERROR: Could not find prompt markers in prompt file", file=sys.stderr)
        sys.exit(1)

    analysis_prompt = prompt_text[start_idx:end_idx].strip()

    # Read video bytes
    print(f"Loading video: {video_path} ({video_path.stat().st_size / 1024 / 1024:.1f} MB)")
    video_bytes = video_path.read_bytes()

    # Call Gemini
    from google import genai
    from google.genai import types

    client = genai.Client(api_key=api_key)

    video_part = types.Part(
        inline_data=types.Blob(data=video_bytes, mime_type="video/mp4"),
        video_metadata=types.VideoMetadata(fps=1.0)
    )

    print(f"Sending to Gemini 3.1 Pro (thinking_budget=8192, media_resolution=HIGH)...")

    response = client.models.generate_content(
        model="gemini-3.1-pro-preview",
        contents=[video_part, analysis_prompt],
        config=types.GenerateContentConfig(
            temperature=0.3,
            thinking_config=types.ThinkingConfig(thinking_budget=8192),
            media_resolution=types.MediaResolution.MEDIA_RESOLUTION_HIGH,
        )
    )

    # Save output
    output_path = Path(args.video_dir) / f"{args.shortcode}-production-analysis.md"
    output_path.write_text(response.text)
    print(f"✅ Saved: {output_path}")
    print(f"   Length: {len(response.text)} chars, ~{len(response.text.split())} words")

if __name__ == "__main__":
    main()
