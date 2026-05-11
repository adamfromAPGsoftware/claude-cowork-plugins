#!/usr/bin/env python3
"""
analyse-competitor-creatives.py — Analyse competitor ad creatives using Claude vision (Anthropic API).

Reads competitor-data.json, finds ads with local_path but no analysis,
sends images and video frames to Claude for detailed creative analysis
(visual composition, person description, hooks, copy strategy, etc.),
and stores structured results back.

Videos are analysed via multi-frame extraction (ffmpeg required for videos).

Default model is claude-haiku-4-5 (fast/cheap). Use --quality high for claude-sonnet-4-6.

Usage:
  python3 marketing-plugin/scripts/analyse-competitor-creatives.py --campaign-id marketing-plugin
  python3 marketing-plugin/scripts/analyse-competitor-creatives.py --campaign-id marketing-plugin --limit 10
  python3 marketing-plugin/scripts/analyse-competitor-creatives.py --campaign-id marketing-plugin --competitor 12345678
  python3 marketing-plugin/scripts/analyse-competitor-creatives.py --campaign-id marketing-plugin --quality high
  python3 marketing-plugin/scripts/analyse-competitor-creatives.py --campaign-id marketing-plugin --skip-videos

Requires:
  pip install requests python-dotenv
  ANTHROPIC_API_KEY in .env (or environment)
"""

import argparse
import base64
import json
import os
import shutil
import subprocess
import sys
import time
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path

# ─── Startup checks ─────────────────────────────────────────────────────────

FFMPEG_AVAILABLE = shutil.which("ffmpeg") is not None

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
REPO_ROOT = PLUGIN_ROOT.parent
COMPETITOR_DATA_PATH: Path = None  # Set in main() after --campaign-id is parsed

ANTHROPIC_API_URL = "https://api.anthropic.com/v1/messages"
ANTHROPIC_VERSION = "2023-06-01"
MODEL_FLASH = "claude-haiku-4-5-20251001"
MODEL_PRO = "claude-sonnet-4-6"
MODEL = MODEL_FLASH

API_DELAY_SECONDS = 2
API_TIMEOUT = 180  # Increased for video analysis

IMAGE_EXTENSIONS = {".jpg", ".jpeg", ".png", ".webp", ".gif"}
VIDEO_EXTENSIONS = {".mp4", ".mov", ".webm"}

# Max video file size for native upload (base64 doubles the size in the request)
MAX_VIDEO_SIZE_MB = 50

# ─── Prompt ──────────────────────────────────────────────────────────────────

ANALYSIS_PROMPT_IMAGE = """You are analysing a competitor's Meta ad creative image for competitive intelligence. Study the visual AND the ad copy below in extreme detail. Your analysis must be descriptive enough that a designer could recreate this creative without seeing the original.

This ad has been running for {days_running} days ({longevity_tier}). Longevity on Meta = the advertiser is paying real money to keep it live, so longer-running ads are likely profitable.

Return a JSON object with ALL of these fields:

CREATIVE STRATEGY:
- hook_type: one of (question|statistic|story|pain_point|testimonial|curiosity|shock|bold_claim|comparison|how_to)
- hook_text: the exact opening hook text visible in the first 1-2 lines (what stops the scroll)
- angle: the core persuasion angle in one sentence
- offer_type: one of (free_trial|demo|lead_magnet|webinar|consultation|discount|waitlist|content|direct_purchase)
- offer_description: what specifically is being offered or promoted
- funnel_stage: one of (cold_awareness|warm_consideration|hot_conversion|retargeting)

VISUAL ANALYSIS:
- visual_style: one of (UGC|polished_brand|text_heavy_overlay|lifestyle|before_after|talking_head|animation|screen_recording|meme|testimonial_card)
- dominant_colours: array of 2-3 dominant hex colours in the creative
- text_on_image: boolean — does the image contain significant text overlay?
- text_on_image_content: the text visible on the image (or null)
- faces_visible: boolean — are human faces prominent?
- production_quality: one of (low_budget|mid|high_production)
- format_type: one of (single_image|carousel|video|story|reel)
- aspect_ratio_guess: one of (1:1|4:5|9:16|16:9)

VISUAL DESCRIPTION (be extremely detailed — a designer must be able to recreate this):
- scene_description: 3-4 sentence detailed description of EVERYTHING visible — objects, layout, mood, lighting, overall composition. Describe it as if the reader cannot see the image.
- person_description: If people are visible, describe EACH person: gender, approximate age range (20s/30s/40s/50s+), appearance style (professional/casual/sporty/nerdy/creative/corporate), what they are doing (talking to camera/typing/pointing/gesturing/posing/smiling), facial expression (confident/friendly/serious/excited/thoughtful), clothing (business shirt/suit/casual tee/hoodie/polo), hair style, and overall vibe/energy. If no people, return null.
- background_treatment: detailed background description — solid colour with hex, gradient direction and colours, office/desk setup, outdoor scene, abstract shapes, blurred real environment, green screen with UI overlay, studio lighting, etc.
- layout_composition: precise spatial description — "Large bold headline top-left occupying 40% of frame, product screenshot center-right, small logo bottom-left corner, CTA button bottom-center". Describe the visual hierarchy and whitespace usage.
- typography_style: font description — sans-serif/serif/display/handwritten, bold/regular/light weight, large headline vs small body text, text colour against background, any text effects (shadow, outline, glow)
- cta_placement: exactly where the CTA sits and how it's styled — "Rounded orange button bottom-center reading 'Start Free Trial' in white bold text, high contrast against dark background" or null if no CTA visible in image
- branding_elements: logo position (top-left/bottom-right/etc), logo size (small/medium/large), brand colour usage throughout, any brand marks, mascots, or icons
- decorative_elements: borders, badges (e.g. "FREE", "Limited Time"), icons, patterns, gradients, drop shadows, divider lines, or "none — clean minimal design"

COPY ANALYSIS:
- copy_length: one of (short|medium|long) — short=1-2 lines, medium=3-5, long=6+
- copy_tone: one of (casual|professional|urgent|empathetic|authoritative|provocative|educational)
- copy_structure: one of (problem_solution|story_arc|list_benefits|social_proof_led|direct_offer|question_led)
- primary_benefit: the #1 benefit communicated
- secondary_benefits: array of other benefits mentioned
- social_proof_elements: array of proof points (e.g. "200,000+ coaches", "trusted by X") or empty array
- cta_text: the CTA button text or visible CTA (or null)
- cta_type: one of (learn_more|sign_up|get_started|book_now|download|shop_now|watch_more|send_message|other)

TARGETING & POSITIONING:
- target_audience: who this ad is specifically targeting (be specific — industry, role, company size)
- pain_point_addressed: the specific pain point this ad speaks to
- objection_handled: what buying objection this ad preemptively addresses (or null)
- competitive_positioning: how they position against alternatives (or null)
- emotional_trigger: one of (fear_of_missing_out|aspiration|frustration|curiosity|urgency|social_proof|authority|belonging)
- awareness_level: one of (unaware|problem_aware|solution_aware|product_aware|most_aware)

COMPETITIVE INTEL:
- what_works: 2-3 sentence assessment of what makes this ad effective (or ineffective)
- replicable_elements: array of specific elements could adapt for our own ads
- unique_differentiator: what makes this ad stand out from typical B2B software ads (or null)
- creative_brief: 2-3 sentence brief that a designer could use to recreate this creative from scratch. Include dimensions, background, text content, layout, colours, and style. Example: "Create a 1:1 square with warm beige (#F8EFEB) background. Large bold dark brown sans-serif text centered reading 'Say hello to smooth processes for all'. Clean minimal style, no people, small logo bottom-right corner."
- confidence: 0.0-1.0 float for overall analysis confidence

Ad copy text: "{ad_copy}"
Headline: "{headline}"
Advertiser: {page_name}
Days running: {days_running} ({longevity_tier})

Return ONLY the JSON object, no markdown fences or explanation."""


ANALYSIS_PROMPT_VIDEO = """You are analysing a competitor's Meta ad VIDEO for competitive intelligence. Watch the ENTIRE video carefully — analyse the full narrative, every scene, transitions, people, audio, and pacing. Your analysis must be descriptive enough that a video editor could recreate this ad without seeing the original.

This ad has been running for {days_running} days ({longevity_tier}). Longevity on Meta = the advertiser is paying real money to keep it live, so longer-running ads are likely profitable.

Return a JSON object with ALL of these fields:

CREATIVE STRATEGY:
- hook_type: one of (question|statistic|story|pain_point|testimonial|curiosity|shock|bold_claim|comparison|how_to)
- hook_text: the exact opening hook text visible or spoken in the first 1-2 seconds (what stops the scroll)
- angle: the core persuasion angle in one sentence
- offer_type: one of (free_trial|demo|lead_magnet|webinar|consultation|discount|waitlist|content|direct_purchase)
- offer_description: what specifically is being offered or promoted
- funnel_stage: one of (cold_awareness|warm_consideration|hot_conversion|retargeting)

VISUAL ANALYSIS:
- visual_style: one of (UGC|polished_brand|text_heavy_overlay|lifestyle|before_after|talking_head|animation|screen_recording|meme|testimonial_card)
- dominant_colours: array of 2-3 dominant hex colours across the video
- text_on_image: boolean — does the video contain significant text overlays?
- text_on_image_content: key text visible on screen throughout the video (or null)
- faces_visible: boolean — are human faces prominent?
- production_quality: one of (low_budget|mid|high_production)
- format_type: one of (single_image|carousel|video|story|reel)
- aspect_ratio_guess: one of (1:1|4:5|9:16|16:9)

VISUAL DESCRIPTION (be extremely detailed):
- scene_description: 3-4 sentence overview of the entire video — setting, mood, lighting, overall feel
- person_description: For EACH person who appears: gender, approximate age range (20s/30s/40s/50s+), appearance style (professional/casual/sporty/nerdy/creative/corporate), what they are doing (talking to camera/demonstrating product/typing/walking/gesturing), facial expression and energy (confident/friendly/serious/excited/passionate/calm), clothing (business shirt/suit/casual tee/hoodie/polo), hair style. Describe their vibe — are they a relatable founder type, a polished corporate presenter, a casual tech bro? If no people, return null.
- background_treatment: what environments/settings appear — home office, professional studio, co-working space, outdoor, abstract animated background, screen recordings, etc.
- layout_composition: how the frame is composed — where the person sits, where text overlays appear, lower thirds, logo placement throughout
- typography_style: any on-screen text styling — font type, size, animation (fade in, slide, pop), colour
- cta_placement: where and when the CTA appears — "End card with blue button reading 'Book a Demo' centered, white text on blue (#2B6BFB) background" or null
- branding_elements: logo appearances (intro/outro/watermark), brand colours used, any brand sounds or jingles
- decorative_elements: transitions, motion graphics, animated icons, progress bars, captions style, or "minimal — straight cuts only"

VIDEO NARRATIVE (watch the full video):
- video_narrative: detailed scene-by-scene description of what happens from start to finish. Example: "Opens with animated text 'Tired of manual work?' on dark background (0-2s). Cuts to talking head of man in his 30s at a desk explaining the problem (2-8s). Screen recording showing the product dashboard with cursor clicking through features (8-15s). Returns to talking head summarising benefits (15-20s). End card with logo and CTA button (20-22s)."
- video_pacing: one of (fast_cuts|moderate|slow_and_steady|single_shot)
- video_duration_estimate: estimated duration in seconds
- opening_hook_visual: exactly what the first 1-2 seconds look like — this is what stops the scroll
- scene_count: number of distinct scenes or cuts
- audio_description: describe the audio — is there a voiceover (male/female, tone), background music (upbeat/calm/corporate/none), sound effects, silence? What language and accent if detectable?
- caption_style: are there captions/subtitles? What style — burned in, auto-generated, styled with background bars?

COPY ANALYSIS:
- copy_length: one of (short|medium|long) — short=1-2 lines, medium=3-5, long=6+
- copy_tone: one of (casual|professional|urgent|empathetic|authoritative|provocative|educational)
- copy_structure: one of (problem_solution|story_arc|list_benefits|social_proof_led|direct_offer|question_led)
- primary_benefit: the #1 benefit communicated
- secondary_benefits: array of other benefits mentioned
- social_proof_elements: array of proof points or empty array
- cta_text: the CTA button text or spoken CTA (or null)
- cta_type: one of (learn_more|sign_up|get_started|book_now|download|shop_now|watch_more|send_message|other)

TARGETING & POSITIONING:
- target_audience: who this ad is specifically targeting (be specific — industry, role, company size)
- pain_point_addressed: the specific pain point this ad speaks to
- objection_handled: what buying objection this ad preemptively addresses (or null)
- competitive_positioning: how they position against alternatives (or null)
- emotional_trigger: one of (fear_of_missing_out|aspiration|frustration|curiosity|urgency|social_proof|authority|belonging)
- awareness_level: one of (unaware|problem_aware|solution_aware|product_aware|most_aware)

COMPETITIVE INTEL:
- what_works: 2-3 sentence assessment of what makes this video ad effective (or ineffective)
- replicable_elements: array of specific elements could adapt for our own video ads
- unique_differentiator: what makes this video stand out from typical B2B software video ads (or null)
- creative_brief: 3-4 sentence brief that a video editor could use to recreate this ad. Include format, duration, scene sequence, talent description, audio approach, and end card. Example: "Create a 9:16 vertical video, ~20 seconds. Open with bold text animation on dark background asking a pain-point question. Cut to a casual male founder (30s, hoodie, home office) talking to camera explaining the solution. Show 5-second screen recording of the product. End with logo + 'Book Free Audit' CTA button. Background music: upbeat but subtle. Add burned-in captions."
- confidence: 0.0-1.0 float for overall analysis confidence

Ad copy text: "{ad_copy}"
Headline: "{headline}"
Advertiser: {page_name}
Days running: {days_running} ({longevity_tier})

Return ONLY the JSON object, no markdown fences or explanation."""


# ─── Helpers ──────────────────────────────────────────────────────────────────

def load_env():
    """Load environment variables from .env."""
    repo_env = REPO_ROOT / ".env"
    plugin_env = PLUGIN_ROOT / ".env"

    if plugin_env.exists():
        load_dotenv(plugin_env)
    if repo_env.exists():
        load_dotenv(repo_env, override=False)

    api_key = os.environ.get("ANTHROPIC_API_KEY")

    if not api_key:
        print("Error: ANTHROPIC_API_KEY not set.", file=sys.stderr)
        print("  Add ANTHROPIC_API_KEY to your .env file at the repo root.", file=sys.stderr)
        print("  Get a key from: https://console.anthropic.com/settings/keys", file=sys.stderr)
        sys.exit(1)

    return api_key


def load_competitor_data():
    """Load competitor-data.json."""
    if not COMPETITOR_DATA_PATH.exists():
        print("Error: competitor-data.json not found.", file=sys.stderr)
        sys.exit(1)
    with open(COMPETITOR_DATA_PATH) as f:
        return json.load(f)


def save_competitor_data(data):
    """Save competitor-data.json."""
    with open(COMPETITOR_DATA_PATH, "w") as f:
        json.dump(data, f, indent=2)


def image_to_base64_part(file_path):
    """Convert an image file to an Anthropic-compatible base64 image content block."""
    data = file_path.read_bytes()
    b64 = base64.b64encode(data).decode()
    ext = file_path.suffix.lower().lstrip(".")
    mime = {"png": "image/png", "jpg": "image/jpeg", "jpeg": "image/jpeg",
            "webp": "image/webp", "gif": "image/gif"}.get(ext, "image/png")
    return {"type": "image", "source": {"type": "base64", "media_type": mime, "data": b64}}


def extract_frames(video_path, count=4):
    """Extract multiple frames from a video using ffmpeg. Returns list of frame paths."""
    if not FFMPEG_AVAILABLE:
        return []

    frames = []
    # Get video duration first
    try:
        result = subprocess.run(
            ["ffprobe", "-v", "quiet", "-show_entries", "format=duration",
             "-of", "csv=p=0", str(video_path)],
            capture_output=True, text=True, timeout=15
        )
        duration = float(result.stdout.strip()) if result.returncode == 0 else 10.0
    except Exception:
        duration = 10.0

    for i in range(count):
        timestamp = (duration * i) / count
        frame_path = video_path.with_suffix(f".frame{i}.jpg")
        if frame_path.exists():
            frames.append(frame_path)
            continue
        try:
            result = subprocess.run(
                ["ffmpeg", "-y", "-ss", str(timestamp), "-i", str(video_path),
                 "-vframes", "1", "-q:v", "2", str(frame_path)],
                capture_output=True, timeout=30
            )
            if result.returncode == 0 and frame_path.exists():
                frames.append(frame_path)
        except Exception:
            pass
    return frames


# ─── Anthropic API ───────────────────────────────────────────────────────────

def analyse_creative(api_key, file_path, is_video=False,
                     ad_copy="", headline="", page_name="",
                     days_running=0, longevity_tier="unknown"):
    """Send an image (or video frames) to Anthropic Claude for creative analysis. Returns parsed JSON or None."""

    prompt_template = ANALYSIS_PROMPT_VIDEO if is_video else ANALYSIS_PROMPT_IMAGE
    prompt = prompt_template.format(
        ad_copy=ad_copy.replace('"', '\\"') if ad_copy else "",
        headline=headline.replace('"', '\\"') if headline else "",
        page_name=page_name,
        days_running=days_running,
        longevity_tier=longevity_tier,
    )

    # Build content parts — Anthropic does not support native video; extract frames for videos
    content_parts = []

    if is_video and file_path.suffix.lower() in VIDEO_EXTENSIONS:
        frames = extract_frames(file_path, count=4)
        if frames:
            for frame in frames:
                content_parts.append(image_to_base64_part(frame))
        else:
            print("    Warning: frame extraction failed (ffmpeg required for video analysis).")
            return None
    else:
        content_parts.append(image_to_base64_part(file_path))

    content_parts.append({"type": "text", "text": prompt})

    payload = {
        "model": MODEL,
        "max_tokens": 4096,
        "messages": [{"role": "user", "content": content_parts}],
    }

    try:
        resp = requests.post(
            ANTHROPIC_API_URL,
            headers={
                "x-api-key": api_key,
                "anthropic-version": ANTHROPIC_VERSION,
                "content-type": "application/json",
            },
            json=payload,
            timeout=API_TIMEOUT,
        )

        if resp.status_code != 200:
            print(f"    API error: {resp.status_code} — {resp.text[:300]}")
            return None

        result = resp.json()

        if "error" in result:
            print(f"    API error: {result['error']}")
            return None

        content = result["content"][0]["text"]

        # Strip markdown code fences if present
        content = content.strip()
        if content.startswith("```"):
            lines = content.split("\n")
            lines = [l for l in lines if not l.strip().startswith("```")]
            content = "\n".join(lines)

        analysis = json.loads(content)
        return analysis

    except json.JSONDecodeError as e:
        print(f"    Failed to parse JSON response: {e}")
        try:
            print(f"    Raw content: {content[:200]}")
        except UnboundLocalError:
            print(f"    Raw content: (unavailable — response body was not valid JSON)")
        return None

    except requests.exceptions.Timeout:
        print(f"    API request timed out ({API_TIMEOUT}s)")
        return None

    except Exception as e:
        print(f"    Analysis failed: {e}")
        return None


# ─── Main ─────────────────────────────────────────────────────────────────────

def get_field(d, key):
    """Get a field from flat or nested analysis JSON."""
    if key in d:
        return d[key]
    for section in d.values():
        if isinstance(section, dict) and key in section:
            return section[key]
    return "unknown"


def main():
    parser = argparse.ArgumentParser(description="Analyse competitor ad creatives via Gemini vision.")
    parser.add_argument("--campaign-id", type=str, required=True,
                        help="Campaign ID (e.g. marketing-plugin). Competitor data is scoped per campaign.")
    parser.add_argument("--competitor", type=str, default=None,
                        help="Filter by Page ID.")
    parser.add_argument("--limit", type=int, default=None,
                        help="Maximum number of creatives to analyse per run.")
    parser.add_argument("--quality", type=str, choices=["high"], default=None,
                        help="Use 'high' for claude-sonnet-4-6 (default uses claude-haiku-4-5).")
    parser.add_argument("--skip-videos", action="store_true",
                        help="Skip video files (analyse images only — saves cost).")
    args = parser.parse_args()

    global COMPETITOR_DATA_PATH, MODEL
    COMPETITOR_DATA_PATH = PLUGIN_ROOT / "data" / "campaigns" / args.campaign_id / "competitor-data.json"

    if args.quality == "high":
        MODEL = MODEL_PRO

    api_key = load_env()
    data = load_competitor_data()
    ads = data.get("ads", [])

    if not ads:
        print("No ads in competitor-data.json.")
        sys.exit(0)

    # Filter to ads needing analysis
    pending = []
    skipped_no_path = 0
    skipped_already = 0

    for i, ad in enumerate(ads):
        local_path = ad.get("local_path")
        analysis = ad.get("analysis")

        if not local_path:
            skipped_no_path += 1
            continue
        if analysis:
            skipped_already += 1
            continue
        if args.competitor and ad.get("page_id") != args.competitor:
            continue

        file_path = PLUGIN_ROOT / local_path
        if not file_path.exists():
            continue

        ext = file_path.suffix.lower()
        if args.skip_videos and ext in VIDEO_EXTENSIONS:
            continue

        if ext not in IMAGE_EXTENSIONS and ext not in VIDEO_EXTENSIONS:
            continue

        pending.append((i, ad, file_path))

    if not pending:
        print("No pending analyses.")
        print(f"  {skipped_no_path} ads have no local_path")
        print(f"  {skipped_already} ads already analysed")
        sys.exit(0)

    if args.limit and args.limit < len(pending):
        pending = pending[:args.limit]

    video_count = sum(1 for _, _, fp in pending if fp.suffix.lower() in VIDEO_EXTENSIONS)
    image_count = len(pending) - video_count

    print(f"Analysing {len(pending)} creatives ({image_count} images, {video_count} videos)...")
    if args.competitor:
        print(f"  Filtered to competitor: {args.competitor}")
    print(f"  Model: {MODEL}")
    if video_count > 0:
        print(f"  Videos: frame extraction via ffmpeg (4 frames per video)")

    analysed_count = 0
    failed_count = 0
    all_hook_types = []
    all_visual_styles = []
    all_triggers = []

    for idx, (ad_index, ad, file_path) in enumerate(pending, 1):
        ad_id = ad.get("ad_id", "unknown")
        page_name = ad.get("page_name", ad.get("page_id", "unknown"))
        ext = file_path.suffix.lower()
        is_video = ext in VIDEO_EXTENSIONS

        media_label = "video" if is_video else "image"
        file_size_mb = file_path.stat().st_size / (1024 * 1024)
        print(f"\n  [{idx}/{len(pending)}] {page_name} — {ad_id} ({media_label}, {file_size_mb:.1f}MB)")

        ad_copy = ad.get("ad_copy", "") or ""
        headline = ad.get("headline", "") or ""
        days_running = ad.get("days_running", 0) or 0
        longevity_tier = ad.get("longevity_tier", "unknown") or "unknown"

        analysis = analyse_creative(
            api_key, file_path, is_video=is_video,
            ad_copy=ad_copy, headline=headline, page_name=page_name,
            days_running=days_running, longevity_tier=longevity_tier
        )

        if analysis:
            today_str = datetime.now(timezone.utc).strftime("%Y-%m-%d")
            analysis["analysed_at"] = today_str
            analysis["media_type"] = media_label
            ads[ad_index]["analysis"] = analysis
            analysed_count += 1

            hook = get_field(analysis, "hook_type")
            style = get_field(analysis, "visual_style")
            trigger = get_field(analysis, "emotional_trigger")
            all_hook_types.append(hook)
            all_visual_styles.append(style)
            all_triggers.append(trigger)

            print(f"    Hook: {hook} | Style: {style} | Trigger: {trigger}")
            angle = get_field(analysis, "angle")
            if angle and angle != "unknown":
                print(f"    Angle: {str(angle)[:100]}")
            what_works = get_field(analysis, "what_works")
            if what_works and what_works != "unknown":
                print(f"    What works: {str(what_works)[:120]}")
            person = get_field(analysis, "person_description")
            if person and person != "unknown" and person is not None:
                print(f"    Person: {str(person)[:120]}")
        else:
            failed_count += 1

        if idx < len(pending):
            time.sleep(API_DELAY_SECONDS)

    # Save
    data["ads"] = ads
    save_competitor_data(data)

    # Summary
    print(f"\n{'─' * 50}")
    print("Done.")
    print(f"  Analysed:   {analysed_count}")
    print(f"  Failed:     {failed_count}")

    if all_hook_types:
        print(f"\n  Common patterns found:")
        for label, values in [("Hook types", all_hook_types), ("Visual styles", all_visual_styles), ("Triggers", all_triggers)]:
            counts = Counter(values).most_common(3)
            print(f"    {label + ':':<20} {', '.join(f'{h} ({c})' for h, c in counts)}")

    print(f"\n  Saved to: {COMPETITOR_DATA_PATH}")


if __name__ == "__main__":
    main()
