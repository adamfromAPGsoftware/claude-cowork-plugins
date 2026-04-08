#!/bin/bash
# Setup script for audio analysis dependencies
# Run this once before using analyze-audio.ts

set -e

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
MODEL_DIR="$SCRIPT_DIR/models"
MODEL_FILE="$MODEL_DIR/std.rnnn"
MODEL_URL="https://github.com/richardpl/arnndn-models/raw/master/std.rnnn"

echo "=== Audio Analysis Setup ==="
echo ""

# Check ffmpeg
echo -n "Checking ffmpeg... "
if command -v ffmpeg &>/dev/null; then
  echo "OK ($(ffmpeg -version 2>&1 | head -1 | cut -d' ' -f3))"
  # Check arnndn filter support
  if ffmpeg -filters 2>/dev/null | grep -q arnndn; then
    echo "  arnndn filter: supported"
  else
    echo "  WARNING: arnndn filter not available. Denoising will be skipped."
    echo "  Install a full ffmpeg build: brew install ffmpeg"
  fi
else
  echo "MISSING"
  echo "  Install: brew install ffmpeg (macOS) or apt install ffmpeg (Linux)"
fi

# Check python3
echo -n "Checking python3... "
if command -v python3 &>/dev/null; then
  echo "OK ($(python3 --version 2>&1))"
else
  echo "MISSING"
  echo "  Install: https://python.org"
fi

# Check silero-vad
echo -n "Checking silero-vad... "
if python3 -c "from silero_vad import load_silero_vad; print('OK')" 2>/dev/null; then
  :
else
  echo "MISSING"
  echo "  Install: pip3 install silero-vad"
fi

# Check Node.js / npx / tsx
echo -n "Checking npx/tsx... "
if command -v npx &>/dev/null; then
  echo "OK (npx $(npx --version 2>&1))"
else
  echo "MISSING"
  echo "  Install Node.js, then: npm install -g tsx"
fi

# Check curl
echo -n "Checking curl... "
if command -v curl &>/dev/null; then
  echo "OK"
else
  echo "MISSING"
  echo "  Install: should be pre-installed on macOS/Linux"
fi

# Download RNNoise model
echo ""
echo -n "Checking RNNoise model... "
if [ -f "$MODEL_FILE" ]; then
  echo "OK ($(wc -c < "$MODEL_FILE" | tr -d ' ') bytes)"
else
  echo "downloading..."
  mkdir -p "$MODEL_DIR"
  curl -sL "$MODEL_URL" -o "$MODEL_FILE"
  echo "  Downloaded to: $MODEL_FILE ($(wc -c < "$MODEL_FILE" | tr -d ' ') bytes)"
fi

# Install npm dependencies
echo ""
echo -n "Checking node_modules... "
if [ -d "$SCRIPT_DIR/node_modules" ]; then
  echo "OK"
else
  echo "installing..."
  cd "$SCRIPT_DIR" && npm install
fi

echo ""
echo "=== Setup Complete ==="
echo ""
echo "Usage:"
echo "  npx tsx analyze-audio.ts --video <path> --content-type intro|main [--transcript <path>]"
