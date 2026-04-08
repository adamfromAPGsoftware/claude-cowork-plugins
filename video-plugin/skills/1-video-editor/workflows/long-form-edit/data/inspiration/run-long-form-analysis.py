#!/usr/bin/env python3
"""
Run Gemini 3.1 Pro long-form production & MG analysis on YouTube tutorial videos.

Production analysis (existing):
  Pass intro: First 3 min at 1.0 fps — detailed intro editing breakdown
  Pass full:  First 5 min at 0.2 fps — structural overview

MG analysis (new):
  Pass mg-intro:   First 90s at 1.0 fps — frame-level MG events (short-form depth)
  Pass mg-body:    3-7 x 2-min sample windows at 0.5 fps — body MG events
  Pass mg-density: Full video at 0.1 fps — chapter structure, MG density per chapter

Usage:
  # Existing production passes
  python run-long-form-analysis.py --video-id QoQBzR1NIqI --pass intro
  python run-long-form-analysis.py --video-id QoQBzR1NIqI --pass full
  python run-long-form-analysis.py --video-id QoQBzR1NIqI --merge

  # New MG passes
  python run-long-form-analysis.py --video-id QoQBzR1NIqI --pass mg-intro
  python run-long-form-analysis.py --video-id QoQBzR1NIqI --pass mg-body
  python run-long-form-analysis.py --video-id QoQBzR1NIqI --pass mg-density
  python run-long-form-analysis.py --video-id QoQBzR1NIqI --merge-mg

  # Batch
  python run-long-form-analysis.py --batch --pass mg-intro
  python run-long-form-analysis.py --batch-mg          # all MG passes + merge
  python run-long-form-analysis.py --batch              # all production passes + merge
"""
from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
import sys
import tempfile
import time
from pathlib import Path
from typing import Optional

SCRIPT_DIR = Path(__file__).parent
PRODUCTION_PROMPT_FILE = SCRIPT_DIR / "long-form-production-analysis-prompt.md"
MG_PROMPT_FILE = SCRIPT_DIR / "long-form-mg-analysis-prompt.md"
VIDEOS_FILE = SCRIPT_DIR / "videos.yaml"

INTRO_DURATION_SECS = 180  # 3 min for production intro pass
FULL_DURATION_SECS = 300   # 5 min for production full pass
MG_INTRO_DURATION_SECS = 90  # 90s for MG intro pass
MG_BODY_WINDOW_SECS = 120    # 2 min per body sample window

ALL_PRODUCTION_PASSES = ["intro", "full"]
ALL_MG_PASSES = ["mg-intro", "mg-body", "mg-density"]
ALL_PASSES = ALL_PRODUCTION_PASSES + ALL_MG_PASSES


def get_api_key(cli_key: str | None) -> str:
    """Resolve Gemini API key from CLI arg, env var, or .env file."""
    if cli_key:
        return cli_key
    key = os.environ.get("GEMINI_API_KEY")
    if key:
        return key
    for parent in Path(__file__).resolve().parents:
        env_file = parent / ".env"
        if env_file.exists():
            for line in env_file.read_text().splitlines():
                if line.startswith("GEMINI_API_KEY="):
                    return line.split("=", 1)[1].strip().strip('"').strip("'")
    print("ERROR: No GEMINI_API_KEY found (set env var, pass --api-key, or add to .env)", file=sys.stderr)
    sys.exit(1)


def load_prompt(prompt_file: Path, start_marker: str, end_marker: str) -> str:
    """Extract prompt text between markers."""
    text = prompt_file.read_text()
    start = text.find(start_marker)
    end = text.find(end_marker)
    if start == -1 or end == -1:
        print(f"ERROR: Could not find prompt markers in {prompt_file.name}", file=sys.stderr)
        print(f"  Looking for: '{start_marker}' ... '{end_marker}'", file=sys.stderr)
        sys.exit(1)
    return text[start:end].strip()


def load_production_prompt() -> str:
    """Load the production analysis prompt."""
    return load_prompt(PRODUCTION_PROMPT_FILE, "## System Prompt for Gemini", "## API Configuration")


def load_mg_prompt(pass_type: str) -> str:
    """Load the appropriate MG analysis prompt for the given pass type."""
    marker_map = {
        "mg-intro": ("## System Prompt for Gemini — Pass A (Intro MG)", "## System Prompt for Gemini — Pass B"),
        "mg-body": ("## System Prompt for Gemini — Pass B (Body Sample Windows)", "## System Prompt for Gemini — Pass C"),
        "mg-density": ("## System Prompt for Gemini — Pass C (MG Density)", "## API Configuration"),
    }
    start_marker, end_marker = marker_map[pass_type]
    return load_prompt(MG_PROMPT_FILE, start_marker, end_marker)


def load_videos() -> list[dict]:
    """Load video entries from videos.yaml."""
    import yaml
    data = yaml.safe_load(VIDEOS_FILE.read_text())
    return data["videos"]


def get_video_entry(video_id: str) -> dict:
    """Look up the full video entry for a video ID."""
    for v in load_videos():
        if v["id"] == video_id:
            return v
    print(f"ERROR: Unknown video ID: {video_id}", file=sys.stderr)
    sys.exit(1)


def get_video_folder(video_id: str) -> str:
    """Look up the folder name for a video ID."""
    return get_video_entry(video_id)["folder"]


def parse_timestamp_to_seconds(ts: str) -> int:
    """Parse MM:SS or H:MM:SS timestamp to total seconds."""
    parts = ts.split(":")
    if len(parts) == 2:
        return int(parts[0]) * 60 + int(parts[1])
    elif len(parts) == 3:
        return int(parts[0]) * 3600 + int(parts[1]) * 60 + int(parts[2])
    else:
        raise ValueError(f"Cannot parse timestamp: {ts}")


def extract_clip(video_path: Path, duration_secs: int, start_secs: int = 0) -> Path:
    """Extract a clip from video using FFmpeg. Returns temp file path."""
    tmp = tempfile.NamedTemporaryFile(suffix=".mp4", delete=False)
    tmp.close()
    cmd = [
        "ffmpeg", "-y",
        "-ss", str(start_secs),
        "-i", str(video_path),
        "-t", str(duration_secs),
        "-c", "copy",
        tmp.name,
    ]
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        # If copy fails (e.g., keyframe issues), re-encode
        cmd = [
            "ffmpeg", "-y",
            "-ss", str(start_secs),
            "-i", str(video_path),
            "-t", str(duration_secs),
            "-c:v", "libx264", "-preset", "fast", "-crf", "23",
            "-c:a", "aac",
            tmp.name,
        ]
        subprocess.run(cmd, check=True, capture_output=True, text=True)
    return Path(tmp.name)


def run_gemini(video_path: Path, fps: float, prompt_text: str, api_key: str,
               thinking_budget: int = 8192, media_resolution: str = "HIGH",
               max_retries: int = 2) -> str:
    """Send video to Gemini and return analysis text.

    For files >100MB, uses the Gemini File API (upload then reference) instead of
    inline data to avoid 500 errors on large payloads.
    """
    from google import genai
    from google.genai import types

    client = genai.Client(api_key=api_key)

    file_size_mb = video_path.stat().st_size / 1024 / 1024
    print(f"  Loading video: {video_path.name} ({file_size_mb:.1f} MB)")

    resolution = (
        types.MediaResolution.MEDIA_RESOLUTION_HIGH
        if media_resolution == "HIGH"
        else types.MediaResolution.MEDIA_RESOLUTION_MEDIUM
    )

    # For large files (>100MB), use the File API to upload first
    use_file_api = file_size_mb > 100

    if use_file_api:
        print(f"  Large file ({file_size_mb:.0f}MB) — uploading via File API...")
        uploaded_file = client.files.upload(
            file=video_path,
            config=types.UploadFileConfig(mime_type="video/mp4"),
        )
        # Wait for file to be ready (ACTIVE state)
        import time as _time
        while uploaded_file.state == "PROCESSING":
            print(f"  File processing... (state={uploaded_file.state})")
            _time.sleep(5)
            uploaded_file = client.files.get(name=uploaded_file.name)

        if uploaded_file.state != "ACTIVE":
            raise RuntimeError(f"File upload failed: state={uploaded_file.state}")

        print(f"  File ready: {uploaded_file.name}")
        video_part = types.Part(
            file_data=types.FileData(
                file_uri=uploaded_file.uri,
                mime_type="video/mp4",
            ),
            video_metadata=types.VideoMetadata(fps=fps),
        )
    else:
        video_bytes = video_path.read_bytes()
        video_part = types.Part(
            inline_data=types.Blob(data=video_bytes, mime_type="video/mp4"),
            video_metadata=types.VideoMetadata(fps=fps),
        )

    print(f"  Sending to Gemini 3.1 Pro (fps={fps}, thinking_budget={thinking_budget}, media_resolution={media_resolution})...")

    last_error = None
    for attempt in range(1, max_retries + 1):
        try:
            response = client.models.generate_content(
                model="gemini-3.1-pro-preview",
                contents=[video_part, prompt_text],
                config=types.GenerateContentConfig(
                    temperature=0.3,
                    thinking_config=types.ThinkingConfig(thinking_budget=thinking_budget),
                    media_resolution=resolution,
                ),
            )
            # Clean up uploaded file if we used the File API
            if use_file_api:
                try:
                    client.files.delete(name=uploaded_file.name)
                except Exception:
                    pass  # Best effort cleanup
            return response.text
        except Exception as e:
            last_error = e
            if attempt < max_retries:
                wait = 30 * attempt
                print(f"  Attempt {attempt} failed ({type(e).__name__}), retrying in {wait}s...")
                import time as _time
                _time.sleep(wait)
            else:
                # Clean up on final failure
                if use_file_api:
                    try:
                        client.files.delete(name=uploaded_file.name)
                    except Exception:
                        pass
                raise last_error


# --- Production Analysis (existing) ---

def process_production_pass(video_id: str, pass_type: str, api_key: str) -> None:
    """Run a production analysis pass (intro or full)."""
    folder = get_video_folder(video_id)
    video_dir = SCRIPT_DIR / folder
    video_path = video_dir / "video.mp4"

    if not video_path.exists():
        print(f"ERROR: Video not found: {video_path}", file=sys.stderr)
        sys.exit(1)

    prompt_text = load_production_prompt()

    if pass_type == "intro":
        output_path = video_dir / "intro-analysis.md"
        if output_path.exists():
            print(f"  SKIP: {folder}/intro-analysis.md already exists (delete to re-run)")
            return

        pass_context = (
            "\n\n**Analysis pass context:** This is a high-detail intro pass (first 3 min, 1 fps). "
            "Focus especially on Sections 1, 2, 3, 4, 5, 7 (intro structure) with maximum detail."
        )
        print(f"  Extracting first {INTRO_DURATION_SECS}s for intro pass...")
        clip = extract_clip(video_path, INTRO_DURATION_SECS)
        try:
            result = run_gemini(clip, fps=1.0, prompt_text=prompt_text + pass_context, api_key=api_key)
        finally:
            clip.unlink(missing_ok=True)

        output_path.write_text(result)
        print(f"  OK: {folder}/intro-analysis.md ({len(result)} chars, ~{len(result.split())} words)")

    elif pass_type == "full":
        output_path = video_dir / "full-analysis.md"
        if output_path.exists():
            print(f"  SKIP: {folder}/full-analysis.md already exists (delete to re-run)")
            return

        pass_context = (
            "\n\n**Analysis pass context:** This is a structural overview pass (first 5 min, 0.2 fps). "
            "Focus especially on Sections 1, 2, 6, 8 (section transitions), 9, 10 with structural patterns across the full segment."
        )
        print(f"  Extracting first {FULL_DURATION_SECS}s for full pass...")
        clip = extract_clip(video_path, FULL_DURATION_SECS)
        try:
            result = run_gemini(clip, fps=0.2, prompt_text=prompt_text + pass_context, api_key=api_key)
        finally:
            clip.unlink(missing_ok=True)

        output_path.write_text(result)
        print(f"  OK: {folder}/full-analysis.md ({len(result)} chars, ~{len(result.split())} words)")


def merge_production(video_id: str) -> None:
    """Merge intro and full analyses into a single production analysis."""
    folder = get_video_folder(video_id)
    video_dir = SCRIPT_DIR / folder

    intro_path = video_dir / "intro-analysis.md"
    full_path = video_dir / "full-analysis.md"
    output_path = video_dir / "production-analysis.md"

    if not intro_path.exists():
        print(f"  SKIP merge: {folder}/intro-analysis.md not found")
        return
    if not full_path.exists():
        print(f"  SKIP merge: {folder}/full-analysis.md not found")
        return

    intro_text = intro_path.read_text()
    full_text = full_path.read_text()

    merged = (
        f"# Production Analysis: {folder}\n\n"
        f"*Combined from intro pass (3 min @ 1fps) and full pass (5 min @ 0.2fps)*\n\n"
        f"---\n\n"
        f"## Part A: Intro Detail (First 3 Minutes)\n\n"
        f"{intro_text}\n\n"
        f"---\n\n"
        f"## Part B: Structural Overview (First 5 Minutes)\n\n"
        f"{full_text}\n"
    )

    output_path.write_text(merged)
    print(f"  OK: Merged → {folder}/production-analysis.md ({len(merged)} chars)")


# --- MG Analysis (new) ---

def process_mg_intro(video_id: str, api_key: str) -> None:
    """Run MG intro analysis pass (first 90s at 1fps, short-form depth)."""
    entry = get_video_entry(video_id)
    folder = entry["folder"]
    video_dir = SCRIPT_DIR / folder
    video_path = video_dir / "video.mp4"
    output_path = video_dir / "mg-analysis-intro.md"

    if not video_path.exists():
        print(f"ERROR: Video not found: {video_path}", file=sys.stderr)
        sys.exit(1)

    if output_path.exists():
        print(f"  SKIP: {folder}/mg-analysis-intro.md already exists (delete to re-run)")
        return

    prompt_text = load_mg_prompt("mg-intro")

    # Inject video metadata into prompt
    video_context = (
        f"\n\n**Video metadata:**\n"
        f"- Title: {entry['title']}\n"
        f"- Creator: {entry['creator']}\n"
        f"- Total Duration: {entry['duration']}\n"
        f"- Category: {entry.get('category', 'unknown')}\n"
        f"- Views: {entry.get('views', 'unknown')}\n"
    )

    print(f"  Extracting first {MG_INTRO_DURATION_SECS}s for MG intro pass...")
    clip = extract_clip(video_path, MG_INTRO_DURATION_SECS)
    try:
        result = run_gemini(
            clip, fps=1.0,
            prompt_text=prompt_text + video_context,
            api_key=api_key,
            thinking_budget=8192,
            media_resolution="HIGH",
        )
    finally:
        clip.unlink(missing_ok=True)

    output_path.write_text(result)
    print(f"  OK: {folder}/mg-analysis-intro.md ({len(result)} chars, ~{len(result.split())} words)")


def process_mg_body(video_id: str, api_key: str) -> None:
    """Run MG body sample window analysis (2-min windows at 0.5fps)."""
    entry = get_video_entry(video_id)
    folder = entry["folder"]
    video_dir = SCRIPT_DIR / folder
    video_path = video_dir / "video.mp4"
    output_path = video_dir / "mg-analysis-body-samples.md"

    if not video_path.exists():
        print(f"ERROR: Video not found: {video_path}", file=sys.stderr)
        sys.exit(1)

    if output_path.exists():
        print(f"  SKIP: {folder}/mg-analysis-body-samples.md already exists (delete to re-run)")
        return

    sample_windows = entry.get("sampleWindows", [])
    if not sample_windows:
        print(f"  SKIP: No sampleWindows defined for {folder} in videos.yaml")
        return

    prompt_template = load_mg_prompt("mg-body")
    all_window_results = []

    for i, window in enumerate(sample_windows, 1):
        start_ts = window["start"]
        end_ts = window["end"]
        context = window.get("context", "")
        start_secs = parse_timestamp_to_seconds(start_ts)
        end_secs = parse_timestamp_to_seconds(end_ts)
        duration = end_secs - start_secs

        print(f"  Window {i}/{len(sample_windows)}: {start_ts}–{end_ts} ({context})")

        # Inject window context into prompt
        window_context = (
            f"\n\n**Window context:**\n"
            f"- Video: {entry['title']} by {entry['creator']}\n"
            f"- Window: {start_ts} – {end_ts}\n"
            f"- Section context: {context}\n"
            f"- Video category: {entry.get('category', 'unknown')}\n"
        )

        clip = extract_clip(video_path, duration, start_secs=start_secs)
        try:
            result = run_gemini(
                clip, fps=0.5,
                prompt_text=prompt_template + window_context,
                api_key=api_key,
                thinking_budget=8192,
                media_resolution="HIGH",
            )
        finally:
            clip.unlink(missing_ok=True)

        all_window_results.append(f"# Window {i}: {start_ts}–{end_ts}\n\n{result}")

        # Wait between windows to avoid rate limits
        if i < len(sample_windows):
            print("  Waiting 30s before next window...")
            time.sleep(30)

    # Combine all windows into single file
    combined = (
        f"# MG Body Sample Analysis: {folder}\n\n"
        f"*{len(sample_windows)} sample windows analyzed at 0.5fps*\n\n"
        f"---\n\n"
        + "\n\n---\n\n".join(all_window_results)
    )

    output_path.write_text(combined)
    print(f"  OK: {folder}/mg-analysis-body-samples.md ({len(combined)} chars, ~{len(combined.split())} words)")


def process_mg_density(video_id: str, api_key: str) -> None:
    """Run MG density analysis pass (full video at 0.1fps)."""
    entry = get_video_entry(video_id)
    folder = entry["folder"]
    video_dir = SCRIPT_DIR / folder
    video_path = video_dir / "video.mp4"
    output_path = video_dir / "mg-density-analysis.md"

    if not video_path.exists():
        print(f"ERROR: Video not found: {video_path}", file=sys.stderr)
        sys.exit(1)

    if output_path.exists():
        print(f"  SKIP: {folder}/mg-density-analysis.md already exists (delete to re-run)")
        return

    prompt_text = load_mg_prompt("mg-density")

    # For very long videos (>1hr), we analyze the full video at 0.1fps
    # Gemini handles long videos natively via its 1M token context
    video_context = (
        f"\n\n**Video metadata:**\n"
        f"- Title: {entry['title']}\n"
        f"- Creator: {entry['creator']}\n"
        f"- Total Duration: {entry['duration']}\n"
        f"- Category: {entry.get('category', 'unknown')}\n"
    )

    duration_secs = entry.get("durationSeconds", 0)
    estimated_frames = int(duration_secs * 0.1)
    estimated_tokens = estimated_frames * 258 + duration_secs * 32
    print(f"  Full video density pass: {entry['duration']} (~{estimated_frames} frames, ~{estimated_tokens:,} tokens)")

    # For course-length videos, we may need to cap the analysis to avoid token limits
    # Videos >2hrs at 0.1fps: ~720 frames @ 258 tokens = ~185K frame tokens (fine)
    # Videos >8hrs at 0.1fps: ~2880 frames @ 258 tokens = ~743K frame tokens (pushing limit)
    # For 8hr+ videos, analyze first 4hrs + last 30min to stay within budget
    max_duration_secs = duration_secs
    analysis_note = ""
    if duration_secs > 4 * 3600:  # >4 hours
        max_duration_secs = 4 * 3600  # Cap at 4 hours for the main pass
        analysis_note = (
            f"\n\n**Note:** This video is {entry['duration']}. Analyzing first 4 hours at 0.1fps. "
            f"Chapters beyond 4:00:00 are estimated from section patterns observed."
        )

    clip = extract_clip(video_path, max_duration_secs)
    try:
        result = run_gemini(
            clip, fps=0.1,
            prompt_text=prompt_text + video_context + analysis_note,
            api_key=api_key,
            thinking_budget=4096,
            media_resolution="MEDIUM",
        )
    finally:
        clip.unlink(missing_ok=True)

    output_path.write_text(result)
    print(f"  OK: {folder}/mg-density-analysis.md ({len(result)} chars, ~{len(result.split())} words)")


def merge_mg_analysis(video_id: str) -> None:
    """Merge MG intro + body samples + density into unified mg-analysis.md."""
    entry = get_video_entry(video_id)
    folder = entry["folder"]
    video_dir = SCRIPT_DIR / folder

    intro_path = video_dir / "mg-analysis-intro.md"
    body_path = video_dir / "mg-analysis-body-samples.md"
    density_path = video_dir / "mg-density-analysis.md"
    output_md = video_dir / "mg-analysis.md"
    output_json = video_dir / "mg-analysis.json"

    parts = []
    parts.append(
        f"# MG Analysis: {entry['title']}\n\n"
        f"*Creator: {entry['creator']} | Duration: {entry['duration']} | "
        f"Category: {entry.get('category', 'unknown')}*\n\n"
        f"*Combined from MG intro pass (90s @ 1fps), body sample windows (2min @ 0.5fps), "
        f"and density pass (full @ 0.1fps)*\n"
    )

    if intro_path.exists():
        parts.append(f"\n---\n\n## Part A: Intro MG Analysis (First 90 Seconds)\n\n{intro_path.read_text()}")
    else:
        print(f"  WARN: {folder}/mg-analysis-intro.md not found — intro section will be empty")

    if body_path.exists():
        parts.append(f"\n---\n\n## Part B: Body Sample Windows\n\n{body_path.read_text()}")
    else:
        print(f"  WARN: {folder}/mg-analysis-body-samples.md not found — body section will be empty")

    if density_path.exists():
        parts.append(f"\n---\n\n## Part C: MG Density & Chapter Structure\n\n{density_path.read_text()}")
    else:
        print(f"  WARN: {folder}/mg-density-analysis.md not found — density section will be empty")

    merged = "\n".join(parts)
    output_md.write_text(merged)
    print(f"  OK: {folder}/mg-analysis.md ({len(merged)} chars)")

    # Extract JSON blocks from the markdown files and combine them
    # Each Gemini pass outputs a JSON block at the end — we merge them
    combined_json = _extract_and_merge_json(intro_path, body_path, density_path, entry)
    if combined_json:
        output_json.write_text(json.dumps(combined_json, indent=2))
        print(f"  OK: {folder}/mg-analysis.json ({output_json.stat().st_size} bytes)")
    else:
        print(f"  WARN: Could not extract JSON from analysis files — {folder}/mg-analysis.json not created")
        print(f"        You may need to manually extract the JSON blocks from the markdown files")


def _extract_and_merge_json(intro_path: Path, body_path: Path, density_path: Path, entry: dict) -> dict | None:
    """Extract JSON code blocks from markdown files and merge into unified structure."""
    result = {
        "videoMetadata": {
            "durationSeconds": entry.get("durationSeconds", 0),
            "creator": entry["creator"],
            "category": entry.get("category", "unknown"),
            "introEndTimestamp": "",
            "dominantAesthetic": "",
        },
        "introAnalysis": {},
        "bodyAnalysis": {
            "bodySampleWindows": [],
            "bodyMGPatterns": {},
            "sectionTransitions": [],
        },
    }

    has_data = False

    # Extract JSON from intro analysis
    if intro_path.exists():
        intro_json = _extract_json_block(intro_path.read_text())
        if intro_json:
            # The intro JSON should contain introAnalysis fields
            if "introAnalysis" in intro_json:
                result["introAnalysis"] = intro_json["introAnalysis"]
            elif "hookAnalysis" in intro_json:
                # Gemini may output the intro fields directly
                result["introAnalysis"] = intro_json
            else:
                result["introAnalysis"] = intro_json
            has_data = True

            # Pull metadata from intro analysis
            if "videoMetadata" in intro_json:
                result["videoMetadata"].update(intro_json["videoMetadata"])

    # Extract JSON from body samples
    if body_path.exists():
        body_text = body_path.read_text()
        # Body file may contain multiple JSON blocks (one per window + patterns summary)
        json_blocks = _extract_all_json_blocks(body_text)
        for block in json_blocks:
            if isinstance(block, list):
                # Array of sample windows
                result["bodyAnalysis"]["bodySampleWindows"].extend(block)
            elif isinstance(block, dict):
                # Gemini often wraps under "bodyAnalysis" key
                inner = block.get("bodyAnalysis", block)
                if isinstance(inner, dict):
                    if "bodySampleWindows" in inner:
                        windows = inner["bodySampleWindows"]
                        if isinstance(windows, list):
                            result["bodyAnalysis"]["bodySampleWindows"].extend(windows)
                    if "bodyMGPatterns" in inner:
                        # Merge patterns — last one wins (typically the summary block)
                        result["bodyAnalysis"]["bodyMGPatterns"] = inner["bodyMGPatterns"]
                    # Individual window object
                    if "windowStart" in inner:
                        result["bodyAnalysis"]["bodySampleWindows"].append(inner)
                # Also check top-level (no wrapper)
                if "bodySampleWindows" in block and block is not inner:
                    result["bodyAnalysis"]["bodySampleWindows"].extend(block["bodySampleWindows"])
                if "windowStart" in block:
                    result["bodyAnalysis"]["bodySampleWindows"].append(block)
        has_data = has_data or bool(json_blocks)

    # Extract JSON from density analysis
    if density_path.exists():
        density_json = _extract_json_block(density_path.read_text())
        if density_json:
            # Gemini often wraps under "bodyAnalysis" key
            inner = density_json.get("bodyAnalysis", density_json)
            if isinstance(inner, dict):
                if "sectionTransitions" in inner:
                    result["bodyAnalysis"]["sectionTransitions"] = inner["sectionTransitions"]
                if "ctaAnalysis" in inner:
                    result["bodyAnalysis"]["ctaAnalysis"] = inner["ctaAnalysis"]
                if "mgDensityByChapter" in inner:
                    result["bodyAnalysis"]["mgDensityByChapter"] = inner["mgDensityByChapter"]
                # Update metadata
                if "chapterCount" in inner:
                    result["videoMetadata"]["chapterCount"] = inner["chapterCount"]
            has_data = True

    return result if has_data else None


def _extract_json_block(text: str) -> dict | None:
    """Extract the last JSON code block from markdown text."""
    # Find all ```json ... ``` blocks
    pattern = r'```json\s*\n(.*?)\n```'
    matches = re.findall(pattern, text, re.DOTALL)
    if not matches:
        return None
    try:
        return json.loads(matches[-1])
    except json.JSONDecodeError:
        return None


def _extract_all_json_blocks(text: str) -> list:
    """Extract all JSON code blocks from markdown text."""
    pattern = r'```json\s*\n(.*?)\n```'
    matches = re.findall(pattern, text, re.DOTALL)
    results = []
    for match in matches:
        try:
            results.append(json.loads(match))
        except json.JSONDecodeError:
            continue
    return results


# --- CLI ---

def main():
    parser = argparse.ArgumentParser(
        description="Run Gemini long-form production & MG analysis",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument("--video-id", help="YouTube video ID (e.g., QoQBzR1NIqI)")
    parser.add_argument(
        "--pass", dest="pass_type",
        choices=ALL_PASSES,
        help="Which analysis pass to run",
    )
    parser.add_argument("--merge", action="store_true", help="Merge production intro + full passes")
    parser.add_argument("--merge-mg", action="store_true", help="Merge MG passes into unified mg-analysis.md/json")
    parser.add_argument("--batch", action="store_true", help="Process all videos (production passes)")
    parser.add_argument("--batch-mg", action="store_true", help="Run all MG passes on all videos + merge")
    parser.add_argument("--api-key", default=None, help="Gemini API key (or set GEMINI_API_KEY)")
    args = parser.parse_args()

    if not args.batch and not args.batch_mg and not args.video_id:
        parser.error("Either --video-id, --batch, or --batch-mg is required")

    # --- Merge operations (no API key needed) ---
    if args.merge:
        if args.batch or args.batch_mg:
            for v in load_videos():
                print(f"Merging production: {v['folder']}...")
                merge_production(v["id"])
        elif args.video_id:
            merge_production(args.video_id)
        return

    if args.merge_mg:
        if args.batch or args.batch_mg:
            for v in load_videos():
                print(f"Merging MG: {v['folder']}...")
                merge_mg_analysis(v["id"])
        elif args.video_id:
            merge_mg_analysis(args.video_id)
        return

    # --- Analysis runs (API key required) ---
    api_key = get_api_key(args.api_key)

    if args.batch_mg:
        # Run all MG passes on all videos, then merge
        videos = load_videos()
        total_steps = sum(1 + len(v.get("sampleWindows", [])) + 1 for v in videos)  # intro + windows + density
        done = 0

        for v in videos:
            vid = v["id"]
            folder = v["folder"]

            # MG intro
            done += 1
            print(f"\n[{done}/{total_steps}] {folder} — pass: mg-intro")
            process_mg_intro(vid, api_key)
            time.sleep(30)

            # MG body windows
            done += len(v.get("sampleWindows", []))
            print(f"\n[{done}/{total_steps}] {folder} — pass: mg-body ({len(v.get('sampleWindows', []))} windows)")
            process_mg_body(vid, api_key)
            time.sleep(30)

            # MG density
            done += 1
            print(f"\n[{done}/{total_steps}] {folder} — pass: mg-density")
            process_mg_density(vid, api_key)
            time.sleep(30)

        # Merge all
        print("\nMerging all MG analyses...")
        for v in videos:
            merge_mg_analysis(v["id"])

        return

    if args.batch:
        # Run production passes on all videos
        videos = load_videos()
        passes = ALL_PRODUCTION_PASSES if not args.pass_type else [args.pass_type]

        # Filter: if an MG pass is specified with --batch, run that MG pass on all videos
        if args.pass_type in ALL_MG_PASSES:
            for i, v in enumerate(videos):
                print(f"\n[{i+1}/{len(videos)}] {v['folder']} — pass: {args.pass_type}")
                if args.pass_type == "mg-intro":
                    process_mg_intro(v["id"], api_key)
                elif args.pass_type == "mg-body":
                    process_mg_body(v["id"], api_key)
                elif args.pass_type == "mg-density":
                    process_mg_density(v["id"], api_key)
                if i < len(videos) - 1:
                    print("  Waiting 30s before next video...")
                    time.sleep(30)
            return

        total = len(videos) * len(passes)
        done = 0
        for v in videos:
            for p in passes:
                done += 1
                print(f"\n[{done}/{total}] {v['folder']} — pass: {p}")
                process_production_pass(v["id"], p, api_key)
                if done < total:
                    print("  Waiting 30s before next API call...")
                    time.sleep(30)

        if not args.pass_type:
            print("\nMerging all production analyses...")
            for v in videos:
                merge_production(v["id"])
        return

    # --- Single video ---
    if args.pass_type:
        folder = get_video_folder(args.video_id)
        print(f"\n{folder} — pass: {args.pass_type}")
        if args.pass_type in ALL_PRODUCTION_PASSES:
            process_production_pass(args.video_id, args.pass_type, api_key)
        elif args.pass_type == "mg-intro":
            process_mg_intro(args.video_id, api_key)
        elif args.pass_type == "mg-body":
            process_mg_body(args.video_id, api_key)
        elif args.pass_type == "mg-density":
            process_mg_density(args.video_id, api_key)
    else:
        parser.error("--pass is required when using --video-id without --merge/--merge-mg")


if __name__ == "__main__":
    main()
