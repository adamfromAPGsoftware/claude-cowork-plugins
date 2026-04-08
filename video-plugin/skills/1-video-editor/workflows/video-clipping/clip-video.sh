#!/bin/bash
# Full deterministic video clipping pipeline
#
# Usage:
#   ./clip-video.sh --video <path> --type intro|main|short [--transcript <path>] [--execute] [--no-denoise]
#
# This script chains:
#   1. Audio analysis (denoised) → audio-analysis.json
#   2. Clip plan generation → clip-plan.md + FFmpeg commands
#   3. Optional: FFmpeg execution → cleaned video

set -e

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
ANALYSIS_DIR="$(dirname "$SCRIPT_DIR")/audio-analysis"

# Parse arguments
VIDEO=""
CONTENT_TYPE="main"
TRANSCRIPT=""
EXECUTE=""
DENOISE_FLAG=""
AUDIO_ENHANCE_FLAG=""
OUTPUT_DIR=""

while [[ $# -gt 0 ]]; do
  case $1 in
    --video) VIDEO="$2"; shift 2 ;;
    --type) CONTENT_TYPE="$2"; shift 2 ;;
    --transcript) TRANSCRIPT="--transcript $2"; shift 2 ;;
    --execute) EXECUTE="--execute"; shift ;;
    --no-denoise) DENOISE_FLAG="--no-denoise"; shift ;;
    --no-audio-enhance) AUDIO_ENHANCE_FLAG="--no-audio-enhance"; shift ;;
    --output-dir) OUTPUT_DIR="$2"; shift 2 ;;
    *) echo "Unknown option: $1"; exit 1 ;;
  esac
done

if [ -z "$VIDEO" ]; then
  echo "Usage: ./clip-video.sh --video <path> --type intro|main [options]"
  echo ""
  echo "Options:"
  echo "  --video <path>        Path to video file (required)"
  echo "  --type intro|main|short Content type (default: main)"
  echo "  --transcript <path>   Path to Deepgram transcript (optional, enables filler word detection)"
  echo "  --execute             Execute FFmpeg command after generating clip plan"
  echo "  --no-denoise          Skip audio denoising (not recommended)"
  echo "  --no-audio-enhance   Skip studio audio enhancement (gate + compressor + loudnorm)"
  echo "  --output-dir <path>   Output directory (default: same as video)"
  exit 1
fi

if [ ! -f "$VIDEO" ]; then
  echo "Error: Video file not found: $VIDEO"
  exit 1
fi

# Determine output directory
if [ -z "$OUTPUT_DIR" ]; then
  OUTPUT_DIR="$(dirname "$VIDEO")"
fi
mkdir -p "$OUTPUT_DIR"

VIDEO_NAME="$(basename "$VIDEO" | sed 's/\.[^.]*$//')"
ANALYSIS_OUTPUT="$OUTPUT_DIR/${VIDEO_NAME}-audio-analysis.md"
ANALYSIS_JSON="$OUTPUT_DIR/${VIDEO_NAME}-audio-analysis.json"
CLIP_PLAN="$OUTPUT_DIR/${VIDEO_NAME}-clip-plan.md"

echo "============================================"
echo " Video Clipping Pipeline"
echo "============================================"
echo "Video:        $VIDEO"
echo "Content type: $CONTENT_TYPE"
echo "Output dir:   $OUTPUT_DIR"
echo "Denoising:    $([ -z "$DENOISE_FLAG" ] && echo 'enabled' || echo 'disabled')"
echo "Audio enhance: $([ -z "$AUDIO_ENHANCE_FLAG" ] && echo 'enabled (gate + compressor + loudnorm)' || echo 'disabled')"
echo ""

# Step 1: Audio Analysis
echo "--- Step 1: Audio Analysis ---"
cd "$ANALYSIS_DIR"

# Ensure dependencies
if [ ! -d "node_modules" ]; then
  echo "Installing npm dependencies..."
  npm install --silent
fi

npx tsx analyze-audio.ts \
  --video "$VIDEO" \
  --output "$ANALYSIS_OUTPUT" \
  --content-type "$CONTENT_TYPE" \
  $DENOISE_FLAG \
  $TRANSCRIPT

echo ""

# Verify JSON was created
if [ ! -f "$ANALYSIS_JSON" ]; then
  echo "Error: audio-analysis.json was not created"
  exit 1
fi

# Step 2: Generate Clip Plan
echo "--- Step 2: Generate Clip Plan ---"
cd "$SCRIPT_DIR"

# Ensure dependencies
if [ ! -d "node_modules" ]; then
  if [ -f "package.json" ]; then
    npm install --silent
  fi
fi

npx tsx generate-clip-plan.ts \
  --analysis "$ANALYSIS_JSON" \
  --video "$VIDEO" \
  --type "$CONTENT_TYPE" \
  --output "$CLIP_PLAN" \
  $AUDIO_ENHANCE_FLAG \
  $EXECUTE

echo ""
echo "============================================"
echo " Pipeline Complete"
echo "============================================"
echo "Analysis:   $ANALYSIS_JSON"
echo "Clip Plan:  $CLIP_PLAN"
if [ -n "$EXECUTE" ]; then
  echo "Output:     $OUTPUT_DIR/${VIDEO_NAME}-cleaned.*"
fi
