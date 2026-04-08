#!/usr/bin/env python3
"""
generate-ad-video.py — Generate video creatives via fal.ai (Kling 3.0 or Veo 3.1).

Generates short-form video ads using fal.ai's queue API. Supports text-to-video
(Kling/Veo) and image-to-video (Kling) for Meta ad campaigns.

Veo 3.1 supports auto-chaining: durations >8s are automatically split into an
initial clip (8s max) + extend-video continuations. The model inherits character
and scene context from the previous clip's final frames, maintaining consistency.
Max total duration: 20s.

Usage:
    # Text-to-video with Kling
    python3 marketing-plugin/scripts/generate-ad-video.py \
        --prompt "Entrepreneur walking confidently toward camera..." \
        --model kling \
        --aspect 9:16 \
        --output /path/to/output.mp4

    # Image-to-video with Kling
    python3 marketing-plugin/scripts/generate-ad-video.py \
        --prompt "Slow zoom into the hero shot..." \
        --model kling \
        --image /path/to/hero.png \
        --aspect 9:16 \
        --duration 10 \
        --output /path/to/output.mp4

    # Text-to-video with Veo 3.1 (default, 8s single clip)
    python3 marketing-plugin/scripts/generate-ad-video.py \
        --prompt "Cinematic product showcase..." \
        --aspect 9:16 \
        --output /path/to/output.mp4

    # Veo 3.1 with auto-chaining (12s = 8s initial + 4s extend)
    python3 marketing-plugin/scripts/generate-ad-video.py \
        --prompt "Multi-scene UGC with 3 scenes..." \
        --aspect 9:16 \
        --duration 12 \
        --output /path/to/output.mp4

    # Veo 3.1 fast mode (cheaper, good for iteration)
    python3 marketing-plugin/scripts/generate-ad-video.py \
        --prompt "Quick test generation..." \
        --aspect 9:16 \
        --fast \
        --output /path/to/output.mp4

Requires:
    pip install requests python-dotenv
"""

import argparse
import base64
import os
import sys
import time
import warnings
from pathlib import Path

warnings.filterwarnings("ignore")

try:
    import requests
except ImportError:
    print("Error: 'requests' not installed. Run: pip install requests python-dotenv", file=sys.stderr)
    sys.exit(1)

try:
    from dotenv import load_dotenv
except ImportError:
    print("Error: 'python-dotenv' not installed. Run: pip install requests python-dotenv", file=sys.stderr)
    sys.exit(1)


# ─── Configuration ────────────────────────────────────────────────────────────

PLUGIN_ROOT = Path(__file__).parent.parent  # marketing-plugin/

FAL_QUEUE_BASE = "https://queue.fal.run"

# Model IDs
MODEL_IDS = {
    "kling-i2v": "fal-ai/kling-video/v3/pro/image-to-video",
    "kling-t2v": "fal-ai/kling-video/v3/pro/text-to-video",
    "veo": "fal-ai/veo3.1",
    "veo-fast": "fal-ai/veo3.1/fast",
    "veo-lite": "fal-ai/veo3.1/lite",
    "veo-lite-i2v": "fal-ai/veo3.1/lite/image-to-video",
    "veo-extend": "fal-ai/veo3.1/extend-video",
    "veo-extend-fast": "fal-ai/veo3.1/fast/extend-video",
    "heygen": "fal-ai/heygen/v2/video-agent",
}

VALID_ASPECTS = {"16:9", "9:16", "1:1"}
# Kling/HeyGen durations (Veo durations validated separately)
KLING_HEYGEN_DURATIONS = {5, 8, 10, 15, 30, 60, 90}
# Veo 3.1 single-clip durations (API constraint)
VEO_CLIP_DURATIONS = [4, 6, 8]
# Veo 3.1 max total duration with chaining (4 clips x 8s)
VEO_MAX_DURATION = 32
MAX_WAIT_SECONDS = 600
POLL_INTERVAL_SECONDS = 5
DOWNLOAD_CHUNK_SIZE = 8192

IMAGE_EXTENSIONS = {".jpg", ".jpeg", ".png", ".webp"}


# ─── Helpers ──────────────────────────────────────────────────────────────────

def load_env():
    """Load environment variables from .env (plugin dir first, then repo root)."""
    plugin_env = PLUGIN_ROOT / ".env"
    repo_env = PLUGIN_ROOT.parent / ".env"

    if plugin_env.exists():
        load_dotenv(plugin_env)
    elif repo_env.exists():
        load_dotenv(repo_env)

    api_key = os.environ.get("FAL_API_KEY")

    if not api_key:
        print("Error: FAL_API_KEY not set.", file=sys.stderr)
        print("  1. Add FAL_API_KEY to .env in the plugin or repo root directory", file=sys.stderr)
        print("  2. Get a key from: https://fal.ai/dashboard/keys", file=sys.stderr)
        sys.exit(1)

    return api_key


def image_to_data_url(path: Path) -> str:
    """Convert an image file to a data URL string."""
    data = path.read_bytes()
    b64 = base64.b64encode(data).decode()
    ext = path.suffix.lower().lstrip(".")
    mime = {"png": "image/png", "jpg": "image/jpeg", "jpeg": "image/jpeg",
            "webp": "image/webp"}.get(ext, "image/png")
    return f"data:{mime};base64,{b64}"


# ─── API Functions ────────────────────────────────────────────────────────────

def submit_job(api_key: str, model_id: str, input_payload: dict) -> dict:
    """Submit a video generation job to fal.ai queue. Returns full response with URLs."""
    url = f"{FAL_QUEUE_BASE}/{model_id}"

    resp = requests.post(
        url,
        headers={
            "Authorization": f"Key {api_key}",
            "Content-Type": "application/json",
        },
        json=input_payload,
        timeout=30,
    )

    if resp.status_code != 200:
        print(f"  ERROR: Submit failed — {resp.status_code} — {resp.text[:500]}", file=sys.stderr)
        sys.exit(1)

    result = resp.json()
    request_id = result.get("request_id")

    if not request_id:
        print(f"  ERROR: No request_id in response — {result}", file=sys.stderr)
        sys.exit(1)

    return result


def poll_status(api_key: str, status_url: str) -> str:
    """Poll job status until COMPLETED or FAILED. Returns final status.

    Uses the status_url returned by fal.ai's submit response — this is the
    canonical URL for checking status. MUST use GET, not POST (POST to fal.ai
    queue endpoints creates new jobs).
    """
    headers = {"Authorization": f"Key {api_key}"}

    start = time.time()
    last_status = ""

    while True:
        elapsed = time.time() - start
        if elapsed > MAX_WAIT_SECONDS:
            print(f"\n  ERROR: Timed out after {MAX_WAIT_SECONDS}s", file=sys.stderr)
            sys.exit(1)

        resp = requests.get(status_url, headers=headers, timeout=30)

        if resp.status_code not in (200, 202):
            print(f"  ERROR: Status check failed — {resp.status_code} — {resp.text[:300]}", file=sys.stderr)
            sys.exit(1)

        data = resp.json()
        status = data.get("status", "UNKNOWN")

        if status != last_status:
            print(f"  Status: {status} ({elapsed:.0f}s)")
            last_status = status

        if status == "COMPLETED":
            return status

        if status == "FAILED":
            error = data.get("error", "Unknown error")
            print(f"  ERROR: Job failed — {error}", file=sys.stderr)
            sys.exit(1)

        time.sleep(POLL_INTERVAL_SECONDS)


def fetch_result(api_key: str, response_url: str) -> dict:
    """Fetch the completed job result.

    Uses the response_url returned by fal.ai's submit response. MUST use GET.
    """
    headers = {"Authorization": f"Key {api_key}"}

    resp = requests.get(response_url, headers=headers, timeout=30)

    if resp.status_code != 200:
        print(f"  ERROR: Result fetch failed — {resp.status_code} — {resp.text[:300]}", file=sys.stderr)
        sys.exit(1)

    return resp.json()


def download_video(url: str, output_path: Path):
    """Download video from URL with streaming."""
    resp = requests.get(url, stream=True, timeout=120)

    if resp.status_code != 200:
        print(f"  ERROR: Download failed — {resp.status_code}", file=sys.stderr)
        sys.exit(1)

    total_bytes = 0
    with open(output_path, "wb") as f:
        for chunk in resp.iter_content(chunk_size=DOWNLOAD_CHUNK_SIZE):
            if chunk:
                f.write(chunk)
                total_bytes += len(chunk)

    size_mb = total_bytes / (1024 * 1024)
    print(f"  Downloaded: {size_mb:.1f}MB")


def apply_watermark(video_path: Path, logo_path: Path):
    """Overlay logo watermark on video using FFmpeg.

    Scales logo to ~8% of video width, 30% opacity, bottom-right with 20px padding.
    Replaces the input file in-place.
    """
    import subprocess

    if not logo_path.exists():
        print(f"  WARNING: Logo not found at {logo_path}, skipping watermark")
        return False

    temp_path = video_path.with_suffix(".watermarked.mp4")

    cmd = [
        "ffmpeg", "-y",
        "-i", str(video_path),
        "-i", str(logo_path),
        "-filter_complex",
        "[1:v]scale=iw*0.20:-1,format=rgba,colorchannelmixer=aa=0.3[logo];"
        "[0:v][logo]overlay=W-w-20:H-h-20:format=auto",
        "-c:a", "copy",
        "-shortest",
        str(temp_path),
    ]

    result = subprocess.run(cmd, capture_output=True, text=True, timeout=60)

    if result.returncode != 0:
        print(f"  WARNING: FFmpeg watermark failed — {result.stderr[:200]}")
        temp_path.unlink(missing_ok=True)
        return False

    # Replace original with watermarked version
    temp_path.replace(video_path)
    print(f"  Watermark applied (logo, bottom-right, 30% opacity)")
    return True


def append_end_card(video_path: Path, end_card_path: Path, duration: int = 3):
    """Append a static end card image as a video segment to the main video.

    Creates a short video clip from the end card image, then concatenates it
    to the main video. The end card gets a 0.5s fade-in from black.
    """
    import subprocess
    import tempfile

    if not end_card_path.exists():
        print(f"  WARNING: End card not found at {end_card_path}, skipping")
        return False

    with tempfile.TemporaryDirectory() as tmpdir:
        tmp = Path(tmpdir)
        end_card_video = tmp / "endcard.mp4"
        concat_list = tmp / "concat.txt"
        output = tmp / "final.mp4"

        # Get input video properties (resolution, fps) to match
        probe_cmd = [
            "ffprobe", "-v", "error",
            "-select_streams", "v:0",
            "-show_entries", "stream=width,height,r_frame_rate",
            "-of", "csv=p=0",
            str(video_path),
        ]
        probe = subprocess.run(probe_cmd, capture_output=True, text=True, timeout=10)
        if probe.returncode != 0:
            print(f"  WARNING: ffprobe failed, skipping end card")
            return False

        parts = probe.stdout.strip().split(",")
        width, height = int(parts[0]), int(parts[1])
        fps = parts[2]  # e.g., "30/1"

        # Create end card video from static image with fade-in
        ec_cmd = [
            "ffmpeg", "-y",
            "-loop", "1",
            "-i", str(end_card_path),
            "-f", "lavfi", "-i", f"anullsrc=r=44100:cl=stereo",
            "-vf", f"scale={width}:{height},format=yuv420p,fade=in:0:d=0.5",
            "-c:v", "libx264", "-preset", "fast", "-crf", "18",
            "-c:a", "aac", "-b:a", "128k",
            "-t", str(duration),
            "-r", fps,
            "-shortest",
            str(end_card_video),
        ]
        result = subprocess.run(ec_cmd, capture_output=True, text=True, timeout=30)
        if result.returncode != 0:
            print(f"  WARNING: End card video creation failed — {result.stderr[:200]}")
            return False

        # Re-encode main video to ensure compatible streams for concat
        main_reencoded = tmp / "main.mp4"
        reencode_cmd = [
            "ffmpeg", "-y",
            "-i", str(video_path),
            "-c:v", "libx264", "-preset", "fast", "-crf", "18",
            "-c:a", "aac", "-b:a", "128k",
            "-r", fps,
            str(main_reencoded),
        ]
        result = subprocess.run(reencode_cmd, capture_output=True, text=True, timeout=60)
        if result.returncode != 0:
            print(f"  WARNING: Main video re-encode failed — {result.stderr[:200]}")
            return False

        # Concat
        concat_list.write_text(f"file '{main_reencoded}'\nfile '{end_card_video}'\n")
        concat_cmd = [
            "ffmpeg", "-y",
            "-f", "concat", "-safe", "0",
            "-i", str(concat_list),
            "-c", "copy",
            str(output),
        ]
        result = subprocess.run(concat_cmd, capture_output=True, text=True, timeout=30)
        if result.returncode != 0:
            print(f"  WARNING: Concat failed — {result.stderr[:200]}")
            return False

        # Replace original
        output.replace(video_path)

    print(f"  End card appended ({duration}s fade-in)")
    return True


# ─── Veo Chaining ────────────────────────────────────────────────────────────

def plan_veo_chain(total_duration: int) -> list[int]:
    """Plan clip durations for Veo 3.1 chaining.

    First clip uses text-to-video (max 8s, must be 4/6/8).
    Subsequent clips use extend-video or image-to-video (flexible duration for
    extend, 4/6/8 for lite image-to-video).
    Returns list of durations, e.g. [8, 8] for 16s total.
    """
    if total_duration <= 8:
        # Single clip — snap to nearest valid duration
        for d in VEO_CLIP_DURATIONS:
            if total_duration <= d:
                return [d]
        return [8]

    clips = [8]  # First clip always 8s (max single-clip)
    remaining = total_duration - 8

    while remaining > 0:
        ext = min(8, remaining)
        # Snap to valid clip duration for lite (image-to-video also requires 4/6/8)
        if ext not in VEO_CLIP_DURATIONS:
            for d in VEO_CLIP_DURATIONS:
                if ext <= d:
                    ext = d
                    break
        clips.append(ext)
        remaining -= ext

    return clips


def extract_last_frame(video_path: Path, output_path: Path) -> bool:
    """Extract the last frame of a video as a PNG for chaining.

    Uses ffprobe to get duration, then seeks to near the end.
    Falls back to -sseof if ffprobe fails.
    """
    import subprocess

    # Get video duration via ffprobe
    probe_cmd = [
        "ffprobe", "-v", "error",
        "-show_entries", "format=duration",
        "-of", "csv=p=0",
        str(video_path),
    ]
    probe = subprocess.run(probe_cmd, capture_output=True, text=True, timeout=10)

    if probe.returncode == 0 and probe.stdout.strip():
        duration = float(probe.stdout.strip())
        seek_time = max(0, duration - 0.1)
        cmd = [
            "ffmpeg", "-y",
            "-ss", str(seek_time),
            "-i", str(video_path),
            "-frames:v", "1",
            "-q:v", "2",
            str(output_path),
        ]
    else:
        # Fallback: seek from end
        cmd = [
            "ffmpeg", "-y",
            "-sseof", "-0.1",
            "-i", str(video_path),
            "-frames:v", "1",
            "-q:v", "2",
            str(output_path),
        ]

    result = subprocess.run(cmd, capture_output=True, text=True, timeout=10)

    if result.returncode != 0:
        print(f"  ERROR: Frame extraction failed — {result.stderr[:200]}", file=sys.stderr)
        return False

    if not output_path.exists() or output_path.stat().st_size == 0:
        print(f"  ERROR: Frame extraction produced no output", file=sys.stderr)
        return False

    size_kb = output_path.stat().st_size / 1024
    print(f"  Extracted last frame: {output_path.name} ({size_kb:.0f}KB)")
    return True


def concat_clips(clip_paths: list, output_path: Path, fps: str = "24") -> bool:
    """Concatenate multiple video clips into a single video using ffmpeg."""
    import subprocess
    import tempfile

    with tempfile.TemporaryDirectory() as tmpdir:
        tmp = Path(tmpdir)

        # Re-encode all clips to ensure compatible streams
        reencoded = []
        for i, clip in enumerate(clip_paths):
            out = tmp / f"clip_{i}.mp4"
            cmd = [
                "ffmpeg", "-y",
                "-i", str(clip),
                "-c:v", "libx264", "-preset", "fast", "-crf", "18",
                "-c:a", "aac", "-b:a", "128k",
                "-r", fps,
                str(out),
            ]
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
            if result.returncode != 0:
                print(f"  ERROR: Re-encode clip {i} failed — {result.stderr[:200]}", file=sys.stderr)
                return False
            reencoded.append(out)

        # Build concat list
        concat_list = tmp / "concat.txt"
        concat_list.write_text("\n".join(f"file '{p}'" for p in reencoded) + "\n")

        # Concat
        cmd = [
            "ffmpeg", "-y",
            "-f", "concat", "-safe", "0",
            "-i", str(concat_list),
            "-c", "copy",
            str(output_path),
        ]
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
        if result.returncode != 0:
            print(f"  ERROR: Concat failed — {result.stderr[:200]}", file=sys.stderr)
            return False

    print(f"  Concatenated {len(clip_paths)} clips")
    return True


def generate_and_get_url(api_key: str, model_id: str, input_payload: dict,
                         label: str = "") -> str:
    """Submit a generation job, poll until done, return the fal.ai video URL.

    Does NOT download the video — returns the URL for chaining or final download.
    """
    prefix = f"  [{label}] " if label else "  "

    print(f"\n{prefix}Submitting to fal.ai ({model_id.split('/')[-1]})...")
    submit_result = submit_job(api_key, model_id, input_payload)
    request_id = submit_result["request_id"]
    status_url = submit_result.get("status_url")
    response_url = submit_result.get("response_url")
    print(f"{prefix}Request ID: {request_id}")

    if not status_url or not response_url:
        print(f"{prefix}ERROR: Missing status_url or response_url", file=sys.stderr)
        sys.exit(1)

    print(f"{prefix}Waiting for generation (max {MAX_WAIT_SECONDS}s)...")
    poll_status(api_key, status_url)

    print(f"{prefix}Fetching result...")
    result = fetch_result(api_key, response_url)

    video_url = None
    video_data = result.get("video")
    if isinstance(video_data, dict):
        video_url = video_data.get("url")
    elif isinstance(video_data, str):
        video_url = video_data

    if not video_url:
        print(f"{prefix}ERROR: No video URL in result", file=sys.stderr)
        print(f"{prefix}Result keys: {list(result.keys())}", file=sys.stderr)
        sys.exit(1)

    print(f"{prefix}Video URL: {video_url[:80]}...")
    return video_url


# ─── Scene Prompts ───────────────────────────────────────────────────────────

def load_scenes_file(path: Path) -> dict:
    """Load a scenes JSON file for per-clip prompts.

    Expected format:
    {
        "preamble": "STYLE: ... CHARACTER: ...",
        "scenes": [
            "SCENE 1: environment, action, dialogue...",
            "SCENE 2: environment, action, dialogue..."
        ]
    }

    Each clip gets: preamble + "\\n\\n" + scenes[i]
    """
    import json

    if not path.exists():
        print(f"Error: Scenes file not found: {path}", file=sys.stderr)
        sys.exit(1)

    with open(path) as f:
        data = json.load(f)

    if "preamble" not in data or "scenes" not in data:
        print("Error: Scenes file must contain 'preamble' and 'scenes' keys", file=sys.stderr)
        sys.exit(1)

    if not isinstance(data["scenes"], list) or len(data["scenes"]) == 0:
        print("Error: 'scenes' must be a non-empty array", file=sys.stderr)
        sys.exit(1)

    return data


def get_clip_prompt(scenes_data: dict, clip_index: int) -> str:
    """Get the prompt for a specific clip from scenes data.

    Returns preamble + scene[clip_index]. If clip_index exceeds the number
    of scenes, uses the last scene (for safety).
    """
    preamble = scenes_data["preamble"]
    scenes = scenes_data["scenes"]
    scene_idx = min(clip_index, len(scenes) - 1)
    return f"{preamble}\n\n{scenes[scene_idx]}"


# ─── Main ─────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description="Generate video creatives via fal.ai (Kling 3.0 / Veo 3.1)")
    parser.add_argument("--prompt", default=None, help="Scene description prompt (single prompt for all clips)")
    parser.add_argument("--scenes-file", default=None,
                        help="JSON file with per-scene prompts for chaining. Format: {preamble, scenes[]}. "
                             "Each clip gets preamble + its scene prompt. Overrides --prompt for chained videos.")
    parser.add_argument("--aspect", required=True, choices=sorted(VALID_ASPECTS),
                        help="Aspect ratio")
    parser.add_argument("--output", required=True, help="Output file path")
    parser.add_argument("--model", default="veo", choices=["kling", "veo", "heygen"],
                        help="Model to use (default: veo)")
    parser.add_argument("--tier", default="lite", choices=["standard", "fast", "lite"],
                        help="Veo 3.1 quality tier (default: lite). 720p+audio costs: lite $0.05/s, fast $0.15/s, standard $0.40/s")
    parser.add_argument("--avatar", default=None,
                        help="HeyGen avatar name (optional, e.g., 'Marcus Suit Front')")
    parser.add_argument("--image", help="Reference image path for Kling image-to-video (optional)")
    parser.add_argument("--duration", type=int, default=8,
                        help="Video duration in seconds (default: 8). Veo: 4-32s, auto-chains if >8s.")
    parser.add_argument("--no-watermark", action="store_true",
                        help="Skip logo watermark overlay")
    parser.add_argument("--end-card", default=None,
                        help="Path to end card image (PNG) to append as 3s outro")
    parser.add_argument("--end-card-duration", type=int, default=3,
                        help="End card duration in seconds (default: 3)")
    args = parser.parse_args()

    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    # Validate prompt args — need either --prompt or --scenes-file
    scenes_data = None
    if args.scenes_file:
        scenes_data = load_scenes_file(Path(args.scenes_file))
        # Use preamble + first scene as the base prompt (for single-clip or non-chained)
        if not args.prompt:
            args.prompt = get_clip_prompt(scenes_data, 0)
        print(f"  Scenes file: {args.scenes_file} ({len(scenes_data['scenes'])} scenes)")
    elif not args.prompt:
        print("Error: Either --prompt or --scenes-file is required", file=sys.stderr)
        sys.exit(1)

    # Validate image arg
    if args.image and args.model != "kling":
        print("Error: --image is only supported with --model kling", file=sys.stderr)
        sys.exit(1)

    if args.tier != "standard" and args.model != "veo":
        print("Error: --tier is only supported with --model veo", file=sys.stderr)
        sys.exit(1)

    if args.image:
        image_path = Path(args.image)
        if not image_path.exists():
            print(f"Error: Image not found: {args.image}", file=sys.stderr)
            sys.exit(1)
        if image_path.suffix.lower() not in IMAGE_EXTENSIONS:
            print(f"Error: Unsupported image format: {image_path.suffix}", file=sys.stderr)
            sys.exit(1)

    # Validate duration by model
    if args.model == "veo":
        if args.duration < 4 or args.duration > VEO_MAX_DURATION:
            print(f"Error: Veo duration must be 4-{VEO_MAX_DURATION}s, got {args.duration}s", file=sys.stderr)
            sys.exit(1)
    elif args.model in ("kling", "heygen"):
        if args.duration not in KLING_HEYGEN_DURATIONS:
            print(f"Error: {args.model} duration must be one of {sorted(KLING_HEYGEN_DURATIONS)}, got {args.duration}s", file=sys.stderr)
            sys.exit(1)

    # Load API key
    api_key = load_env()

    # ── Determine model ID ──

    if args.model == "kling" and args.image:
        model_key = "kling-i2v"
    elif args.model == "kling":
        model_key = "kling-t2v"
    elif args.model == "heygen":
        model_key = "heygen"
    else:
        veo_model_keys = {"standard": "veo", "fast": "veo-fast", "lite": "veo-lite"}
        model_key = veo_model_keys[args.tier]

    model_id = MODEL_IDS[model_key]
    is_veo = args.model == "veo"
    use_chain = is_veo and args.duration > 8

    tier_label = args.tier
    veo_cost = {"standard": 0.40, "fast": 0.15, "lite": 0.05}
    print(f"Model: {model_key} ({model_id})")
    print(f"Aspect: {args.aspect}")
    print(f"Duration: {args.duration}s")
    if use_chain:
        chain = plan_veo_chain(args.duration)
        est_cost = sum(d * veo_cost[args.tier] for d in chain)
        chain_method = "image-to-video" if args.tier == "lite" else "extend-video"
        print(f"  Chain plan: {' + '.join(f'{d}s' for d in chain)} ({tier_label}, {chain_method}, ~${est_cost:.2f})")
    elif is_veo:
        est_cost = args.duration * veo_cost[args.tier]
        print(f"  Single clip ({tier_label}, ~${est_cost:.2f})")
    print(f"Output: {output_path}")

    # ── Veo 3.1 with auto-chaining ──

    if is_veo:
        chain = plan_veo_chain(args.duration)
        print(f"  Audio: enabled | Resolution: 720p")

        if args.tier == "lite" and len(chain) > 1:
            # ── Lite chaining: text-to-video → (extract last frame → image-to-video) × N ──
            import tempfile

            with tempfile.TemporaryDirectory() as tmpdir:
                tmp = Path(tmpdir)
                clip_paths = []

                # Clip 1: text-to-video
                clip1_prompt = get_clip_prompt(scenes_data, 0) if scenes_data else args.prompt
                initial_payload = {
                    "prompt": clip1_prompt,
                    "duration": f"{chain[0]}s",
                    "aspect_ratio": args.aspect,
                    "generate_audio": True,
                    "resolution": "720p",
                }
                video_url = generate_and_get_url(
                    api_key, model_id, initial_payload,
                    label=f"Clip 1/{len(chain)} ({chain[0]}s, text-to-video)"
                )

                clip1_path = tmp / "clip_1.mp4"
                print(f"\n  Downloading clip 1...")
                download_video(video_url, clip1_path)
                clip_paths.append(clip1_path)

                # Clips 2+: extract last frame → image-to-video
                lite_i2v_model = MODEL_IDS["veo-lite-i2v"]
                for i, ext_duration in enumerate(chain[1:], start=2):
                    prev_clip = clip_paths[-1]

                    # Extract last frame
                    frame_path = tmp / f"frame_{i-1}.png"
                    if not extract_last_frame(prev_clip, frame_path):
                        print(f"  ERROR: Failed to extract frame from clip {i-1}", file=sys.stderr)
                        sys.exit(1)

                    # Convert frame to data URL
                    frame_data_url = image_to_data_url(frame_path)

                    # Generate next clip via image-to-video (per-scene prompt)
                    clip_prompt = get_clip_prompt(scenes_data, i - 1) if scenes_data else args.prompt
                    i2v_payload = {
                        "prompt": clip_prompt,
                        "image_url": frame_data_url,
                        "duration": f"{ext_duration}s",
                        "aspect_ratio": args.aspect,
                        "generate_audio": True,
                        "resolution": "720p",
                    }
                    video_url = generate_and_get_url(
                        api_key, lite_i2v_model, i2v_payload,
                        label=f"Clip {i}/{len(chain)} ({ext_duration}s, image-to-video)"
                    )

                    clip_path = tmp / f"clip_{i}.mp4"
                    print(f"\n  Downloading clip {i}...")
                    download_video(video_url, clip_path)
                    clip_paths.append(clip_path)

                # Stitch all clips
                print(f"\nStitching {len(clip_paths)} clips...")
                if not concat_clips(clip_paths, output_path):
                    print("  ERROR: Failed to concatenate clips", file=sys.stderr)
                    sys.exit(1)

        else:
            # ── Standard/Fast chaining via extend-video, or single clip ──
            initial_payload = {
                "prompt": args.prompt,
                "duration": f"{chain[0]}s",
                "aspect_ratio": args.aspect,
                "generate_audio": True,
                "resolution": "720p",
            }
            video_url = generate_and_get_url(
                api_key, model_id, initial_payload,
                label=f"Clip 1/{len(chain)} ({chain[0]}s)"
            )

            if len(chain) > 1:
                extend_model_keys = {"standard": "veo-extend", "fast": "veo-extend-fast"}
                extend_model_key = extend_model_keys.get(args.tier, "veo-extend")

                for i, ext_duration in enumerate(chain[1:], start=2):
                    extend_payload = {
                        "prompt": args.prompt,
                        "video_url": video_url,
                        "duration": f"{ext_duration}s",
                        "aspect_ratio": args.aspect,
                        "generate_audio": True,
                        "resolution": "720p",
                    }
                    extend_model_id = MODEL_IDS[extend_model_key]
                    video_url = generate_and_get_url(
                        api_key, extend_model_id, extend_payload,
                        label=f"Clip {i}/{len(chain)} (extend +{ext_duration}s)"
                    )

            # Download final video
            print(f"\nDownloading final video...")
            download_video(video_url, output_path)

    # ── Kling / HeyGen (non-chained) ──

    else:
        if model_key == "kling-i2v":
            image_data_url = image_to_data_url(Path(args.image))
            input_payload = {
                "prompt": args.prompt,
                "image_url": image_data_url,
                "duration": str(args.duration),
                "aspect_ratio": args.aspect,
            }
            print(f"  Reference image: {args.image}")
        elif model_key == "kling-t2v":
            input_payload = {
                "prompt": args.prompt,
                "duration": str(args.duration),
                "aspect_ratio": args.aspect,
            }
        elif model_key == "heygen":
            orientation = "portrait" if args.aspect == "9:16" else "landscape"
            input_payload = {
                "prompt": args.prompt,
                "config": {
                    "orientation": orientation,
                    "duration": args.duration,
                },
            }
            if args.avatar:
                input_payload["config"]["avatar"] = args.avatar
            print(f"  Orientation: {orientation}")
            if args.avatar:
                print(f"  Avatar: {args.avatar}")

        print(f"\nSubmitting to fal.ai...")
        submit_result = submit_job(api_key, model_id, input_payload)
        request_id = submit_result["request_id"]
        status_url = submit_result.get("status_url")
        response_url = submit_result.get("response_url")
        print(f"  Request ID: {request_id}")
        print(f"  Status URL: {status_url}")
        print(f"  Response URL: {response_url}")

        if not status_url or not response_url:
            print(f"  ERROR: Missing status_url or response_url in submit response", file=sys.stderr)
            print(f"  Response: {submit_result}", file=sys.stderr)
            sys.exit(1)

        print(f"\nWaiting for generation (max {MAX_WAIT_SECONDS}s)...")
        poll_status(api_key, status_url)

        print(f"\nFetching result...")
        result = fetch_result(api_key, response_url)

        video_url = None
        video_data = result.get("video")
        if isinstance(video_data, dict):
            video_url = video_data.get("url")
        elif isinstance(video_data, str):
            video_url = video_data

        if not video_url:
            print(f"  ERROR: No video URL in result", file=sys.stderr)
            print(f"  Result keys: {list(result.keys())}", file=sys.stderr)
            print(f"  Full result: {str(result)[:500]}", file=sys.stderr)
            sys.exit(1)

        print(f"\nDownloading video...")
        download_video(video_url, output_path)

    # ── Apply watermark ──

    if not args.no_watermark:
        logo_path = PLUGIN_ROOT / "data" / "reference-images" / "apg-logo-light.png"
        print(f"\nApplying watermark...")
        apply_watermark(output_path, logo_path)

    # ── Append end card ──

    if args.end_card:
        end_card_path = Path(args.end_card)
        if not end_card_path.exists():
            print(f"  WARNING: End card not found at {args.end_card}")
        else:
            print(f"\nAppending end card ({args.end_card_duration}s)...")
            append_end_card(output_path, end_card_path, args.end_card_duration)

    print(f"\nGenerated: {output_path} ({args.duration}s, {args.model})")


if __name__ == "__main__":
    main()
