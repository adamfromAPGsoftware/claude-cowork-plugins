#!/usr/bin/env bash
# Download long-form inspiration videos for production analysis
# Usage: bash download-videos.sh [--video-id ID] [--full]
#
# Downloads into per-creator folders:
#   - Video clips for visual analysis (full for all, 720p for long courses)
#   - Full audio (m4a) for all videos (transcript extraction)
#
# --full: Download complete videos for long courses (needed for MG body sample analysis)
#         Without --full, long courses only get 10-min clips
#
# Requires: yt-dlp (brew install yt-dlp)
# Compatible with bash 3.2+ (macOS default)

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

YT_DLP="${YT_DLP:-/opt/homebrew/bin/yt-dlp}"

if ! command -v "$YT_DLP" &>/dev/null; then
  echo "ERROR: yt-dlp not found at $YT_DLP"
  echo "Install: brew install yt-dlp"
  exit 1
fi

# Video manifest — plain arrays (bash 3 compatible)
# Format: "id|folder|visual_minutes|is_long_course"
VIDEOS=(
  "Ey18PDiaAYI|nate-herk-n8n-agents-course|5|true"
  "QoQBzR1NIqI|nick-saraev-claude-code-course|5|true"
  "EH5jx5qPabU|futurepedia-first-ai-agent|26|false"
  "OpUGl4gBHAU|varun-mayya-automate-with-ai|29|false"
  "dpoMEcXjVH8|kevin-stratvert-n8n-beginners|23|false"
)

# Parse args
SINGLE_ID=""
FULL_MODE=false
while [[ $# -gt 0 ]]; do
  case $1 in
    --video-id) SINGLE_ID="$2"; shift 2 ;;
    --full) FULL_MODE=true; shift ;;
    *) echo "Unknown arg: $1"; exit 1 ;;
  esac
done

download_video() {
  local id="$1"
  local folder="$2"
  local visual_min="$3"
  local is_long="$4"
  local url="https://www.youtube.com/watch?v=${id}"

  echo ""
  echo "=========================================="
  echo "Processing: $folder ($id)"
  echo "=========================================="

  mkdir -p "$folder"

  # 1. Download video for visual analysis
  if [[ -f "${folder}/video.mp4" ]]; then
    echo "  SKIP: ${folder}/video.mp4 already exists"
  else
    if [[ "$is_long" == "true" && "$FULL_MODE" == "false" ]]; then
      echo "  Downloading first ${visual_min} min clip (long course, use --full for complete video)..."
      "$YT_DLP" \
        -f "bestvideo[height<=1080]+bestaudio/best[height<=1080]" \
        --download-sections "*0-$((visual_min * 60))" \
        --merge-output-format mp4 \
        -o "${folder}/video.mp4" \
        "$url"
    elif [[ "$is_long" == "true" && "$FULL_MODE" == "true" ]]; then
      echo "  Downloading FULL video at 720p (long course, --full mode)..."
      "$YT_DLP" \
        -f "bestvideo[height<=720]+bestaudio/best[height<=720]" \
        --merge-output-format mp4 \
        -o "${folder}/video.mp4" \
        "$url"
    else
      echo "  Downloading full video at 1080p (${visual_min} min)..."
      "$YT_DLP" \
        -f "bestvideo[height<=1080]+bestaudio/best[height<=1080]" \
        --merge-output-format mp4 \
        -o "${folder}/video.mp4" \
        "$url"
    fi
    echo "  OK: ${folder}/video.mp4"
  fi

  # 2. Download full audio for transcription
  if [[ -f "${folder}/full-audio.m4a" ]]; then
    echo "  SKIP: ${folder}/full-audio.m4a already exists"
  else
    echo "  Downloading full audio..."
    "$YT_DLP" \
      --extract-audio \
      --audio-format m4a \
      --audio-quality 0 \
      -o "${folder}/full-audio.%(ext)s" \
      "$url"
    echo "  OK: ${folder}/full-audio.m4a"
  fi

  echo "  DONE: $folder"
}

# Find video entry by ID, returns "id|folder|min|long" or empty
find_video() {
  local search_id="$1"
  for entry in "${VIDEOS[@]}"; do
    local entry_id="${entry%%|*}"
    if [[ "$entry_id" == "$search_id" ]]; then
      echo "$entry"
      return 0
    fi
  done
  return 1
}

# Execute
if [[ -n "$SINGLE_ID" ]]; then
  entry=$(find_video "$SINGLE_ID") || {
    echo "ERROR: Unknown video ID: $SINGLE_ID"
    echo "Valid IDs:"
    for v in "${VIDEOS[@]}"; do echo "  ${v%%|*}"; done
    exit 1
  }
  IFS='|' read -r id folder visual_min is_long <<< "$entry"
  download_video "$id" "$folder" "$visual_min" "$is_long"
else
  echo "Downloading all 5 inspiration videos..."
  for entry in "${VIDEOS[@]}"; do
    IFS='|' read -r id folder visual_min is_long <<< "$entry"
    download_video "$id" "$folder" "$visual_min" "$is_long"
  done
fi

echo ""
echo "=========================================="
echo "Download complete!"
echo "=========================================="
for d in */; do
  ls -lh "${d}"video.mp4 "${d}"full-audio.m4a 2>/dev/null
done
