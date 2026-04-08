#!/usr/bin/env python3
"""
generate-ad-image.py — Generate ad creative images via Nano Banana Pro (OpenRouter).

Generates high-quality ad images for Meta campaigns using Gemini Flash Image
through OpenRouter. Supports reference photos and inspiration images as input.

Usage:
    python3 marketing-plugin/scripts/generate-ad-image.py \
        --prompt "Bold ad creative: entrepreneur pointing at camera..." \
        --aspect 1:1 \
        --output /path/to/output.png

    # With reference photos and inspiration
    python3 marketing-plugin/scripts/generate-ad-image.py \
        --ref-dir /path/to/reference-photos \
        --inspo-dir /path/to/inspiration-images \
        --aspect 9:16 \
        --output /path/to/output.png \
        --prompt "Story ad: ..."

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

try:
    from PIL import Image
except ImportError:
    Image = None  # Only needed for 1.91:1 crop


# ─── Configuration ────────────────────────────────────────────────────────────

PLUGIN_ROOT = Path(__file__).parent.parent  # marketing-plugin/

OPENROUTER_URL = "https://openrouter.ai/api/v1/chat/completions"
MODEL = "google/gemini-3-pro-image-preview"

VALID_ASPECTS = {"1:1", "9:16", "16:9", "1.91:1"}
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

    api_key = os.environ.get("OPENROUTER_API_KEY")

    if not api_key:
        print("Error: OPENROUTER_API_KEY not set.", file=sys.stderr)
        print("  1. Add OPENROUTER_API_KEY to .env in the plugin or repo root directory", file=sys.stderr)
        print("  2. Get a key from: https://openrouter.ai/keys", file=sys.stderr)
        sys.exit(1)

    return api_key


def image_to_base64_part(path: Path) -> dict:
    """Convert an image file to an OpenAI-compatible base64 image_url part."""
    data = path.read_bytes()
    b64 = base64.b64encode(data).decode()
    ext = path.suffix.lower().lstrip(".")
    mime = {"png": "image/png", "jpg": "image/jpeg", "jpeg": "image/jpeg",
            "webp": "image/webp"}.get(ext, "image/png")
    return {"type": "image_url", "image_url": {"url": f"data:{mime};base64,{b64}"}}


def crop_to_191_aspect(path: Path):
    """Crop a 16:9 image to 1.91:1 by trimming height from center."""
    img = Image.open(path)
    w, h = img.size
    target_h = round(w / 1.91)
    if target_h >= h:
        return  # Already wider than 1.91:1, no crop needed
    top = (h - target_h) // 2
    cropped = img.crop((0, top, w, top + target_h))
    cropped.save(path)
    print(f"  Cropped to 1.91:1: {w}x{target_h} (from {w}x{h})")


def load_images_from_dir(dir_path: Path, label: str) -> list:
    """Load all supported images from a directory, sorted by name."""
    parts = []
    if not dir_path.exists():
        print(f"  WARNING: {label} directory not found: {dir_path}", file=sys.stderr)
        return parts

    for p in sorted(dir_path.iterdir()):
        if p.suffix.lower() in IMAGE_EXTENSIONS:
            parts.append(image_to_base64_part(p))
            print(f"  Loaded {label}: {p.name}")

    return parts


# ─── Main ─────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description="Generate ad creative images via Nano Banana Pro (OpenRouter)")
    parser.add_argument("--prompt", required=True, help="Full text prompt for image generation")
    parser.add_argument("--aspect", required=True, choices=sorted(VALID_ASPECTS),
                        help="Aspect ratio (1.91:1 generates at 16:9 then crops)")
    parser.add_argument("--output", required=True, help="Output file path")
    parser.add_argument("--ref-dir", help="Directory of reference photos to include as input (optional)")
    parser.add_argument("--inspo-dir", help="Directory of inspiration images (optional)")
    args = parser.parse_args()

    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    # 1.91:1 requires Pillow for post-generation crop
    requested_aspect = args.aspect
    crop_to_191 = requested_aspect == "1.91:1"

    if crop_to_191:
        if Image is None:
            print("Error: Pillow is required for 1.91:1 aspect ratio. Run: pip install Pillow", file=sys.stderr)
            sys.exit(1)
        # Generate at 16:9 (model-supported), then crop to 1.91:1
        args.aspect = "16:9"

    # Load API key
    api_key = load_env()

    # ── Build content parts ──

    content_parts = []

    # 1. Reference images
    if args.ref_dir:
        ref_parts = load_images_from_dir(Path(args.ref_dir), "ref")
        content_parts.extend(ref_parts)
        print(f"  Reference photos: {len(ref_parts)}")

    # 2. Inspiration images
    if args.inspo_dir:
        inspo_parts = load_images_from_dir(Path(args.inspo_dir), "inspo")
        content_parts.extend(inspo_parts)
        print(f"  Inspiration images: {len(inspo_parts)}")

    # 3. Text prompt (always last)
    content_parts.append({"type": "text", "text": args.prompt})

    print(f"\nAspect: {requested_aspect}" + (" (generating at 16:9, will crop)" if crop_to_191 else ""))
    print(f"Output: {output_path}")

    # ── API request ──

    payload = {
        "model": MODEL,
        "messages": [{"role": "user", "content": content_parts}],
        "modalities": ["image", "text"],
        "image_config": {
            "aspect_ratio": args.aspect,
            "image_size": "2K",
        },
    }

    print(f"\nGenerating ad image via OpenRouter ({MODEL})...")
    try:
        t0 = time.time()
        resp = requests.post(
            OPENROUTER_URL,
            headers={
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json",
            },
            json=payload,
            timeout=120,
        )
        elapsed = time.time() - t0
        print(f"  API response in {elapsed:.1f}s (status {resp.status_code})")

        if resp.status_code != 200:
            print(f"  ERROR: {resp.status_code} — {resp.text[:500]}", file=sys.stderr)
            sys.exit(1)

        result = resp.json()

        if "error" in result:
            print(f"  ERROR: {result['error']}", file=sys.stderr)
            sys.exit(1)

        message = result["choices"][0]["message"]

        if message.get("content"):
            print(f"  Model text: {message['content'][:200]}")

        images = message.get("images", [])
        if not images:
            print("  ERROR: No image in response", file=sys.stderr)
            print(f"  Full response: {str(result)[:500]}", file=sys.stderr)
            sys.exit(1)

        # Extract first image (may be string or dict)
        img_data_url = images[0]
        if isinstance(img_data_url, dict):
            data_url = img_data_url.get("image_url", {}).get("url", "")
        else:
            data_url = str(img_data_url)

        if "base64," in data_url:
            b64_data = data_url.split("base64,", 1)[1]
        else:
            b64_data = data_url

        img_bytes = base64.b64decode(b64_data)
        output_path.write_bytes(img_bytes)
        size_kb = len(img_bytes) / 1024
        print(f"\nGenerated: {output_path} ({size_kb:.0f}KB)")

        # Crop to 1.91:1 if requested
        if crop_to_191:
            crop_to_191_aspect(output_path)

        # Only use the first image — skip additional variants
        if len(images) > 1:
            print(f"  ({len(images)} variants returned, using first only)")

    except requests.exceptions.Timeout:
        print("  ERROR: Request timed out (120s)", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"  ERROR: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
