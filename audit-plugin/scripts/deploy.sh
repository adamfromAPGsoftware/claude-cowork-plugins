#!/usr/bin/env bash
set -euo pipefail

REPO_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
DEPLOY_DIR="$REPO_ROOT/deploy"
CONFIG="$REPO_ROOT/clients.json"

# Load .env into local variables (not exported, so wrangler uses its own auth)
if [ -f "$REPO_ROOT/.env" ]; then
  while IFS='=' read -r key value; do
    [[ -z "$key" || "$key" =~ ^# ]] && continue
    declare "$key=$value"
  done < "$REPO_ROOT/.env"
fi

if [ ! -f "$CONFIG" ]; then
  echo "ERROR: clients.json not found. Copy clients.example.json and configure it."
  exit 1
fi

# Security posture check
SECURITY_FILE="$REPO_ROOT/SECURITY.md"
if [ -f "$SECURITY_FILE" ]; then
  OPEN_CRITICAL=$(grep -c '| CRITICAL |.*| OPEN |' "$SECURITY_FILE" 2>/dev/null || true)
  OPEN_HIGH=$(grep -c '| HIGH |.*| OPEN |' "$SECURITY_FILE" 2>/dev/null || true)
  if [ "$OPEN_CRITICAL" -gt 0 ] || [ "$OPEN_HIGH" -gt 0 ]; then
    echo ""
    echo "⚠️  SECURITY WARNING: $OPEN_CRITICAL critical and $OPEN_HIGH high findings still OPEN"
    echo "   Review SECURITY.md before deploying to production."
    echo ""
  fi
fi

echo "==> Cleaning deploy directory"
rm -rf "$DEPLOY_DIR"
mkdir -p "$DEPLOY_DIR"

echo "==> Copying middleware and routes"
cp -r "$REPO_ROOT/functions" "$DEPLOY_DIR/functions"

echo "==> Generating stripped clients.json for deploy (slug + close_token only)"
python3 -c "
import json
with open('$CONFIG') as f:
    clients = json.load(f)
stripped = {}
for key, cfg in clients.items():
    entry = {'slug': cfg['slug']}
    if 'close_token' in cfg:
        entry['close_token'] = cfg['close_token']
    stripped[key] = entry
with open('$DEPLOY_DIR/clients.json', 'w') as f:
    json.dump(stripped, f)
"

echo "==> Copying client deliverables"
# Parse client slugs from clients.json using python (available on macOS)
python3 -c "
import json, sys
with open('$CONFIG') as f:
    clients = json.load(f)
for subdomain, cfg in clients.items():
    print(cfg['slug'])
" | while read -r slug; do
  SRC="$REPO_ROOT/clients/$slug/deliverables"
  DEST="$DEPLOY_DIR/$slug"

  if [ ! -d "$SRC" ]; then
    echo "WARNING: No deliverables found for $slug — skipping"
    continue
  fi

  mkdir -p "$DEST"
  cp "$SRC"/*.html "$DEST/" 2>/dev/null || true

  # Rename client-website.html to index.html (entry point)
  if [ -f "$DEST/client-website.html" ]; then
    cp "$DEST/client-website.html" "$DEST/index.html"
  fi

  echo "  Copied: $slug ($(ls "$DEST"/*.html 2>/dev/null | wc -l | tr -d ' ') files)"
done

echo "==> Copying close pages (token-protected)"
python3 -c "
import json, sys
with open('$CONFIG') as f:
    clients = json.load(f)
for subdomain, cfg in clients.items():
    print(subdomain + ' ' + cfg['slug'])
" | while read -r key slug; do
  SRC_CLOSE="$REPO_ROOT/clients/$slug/close-page"
  DEST_CLOSE="$DEPLOY_DIR/close/$key"

  if [ ! -d "$SRC_CLOSE" ]; then
    continue
  fi

  mkdir -p "$DEST_CLOSE"
  cp "$SRC_CLOSE"/*.html "$DEST_CLOSE/" 2>/dev/null || true
  echo "  Copied close page: /close/$key/ ($(ls "$DEST_CLOSE"/*.html 2>/dev/null | wc -l | tr -d ' ') files)"
done

echo "==> Copying robots.txt"
cp "$REPO_ROOT/robots.txt" "$DEPLOY_DIR/robots.txt"

echo "==> Deploying to Cloudflare Pages"
cd "$DEPLOY_DIR"
wrangler pages deploy . --project-name apg-audits

# Sync Cloudflare Access applications (email OTP auth per client)
# Pass credentials only to the sync script so wrangler keeps its own auth
if [ -n "${CLOUDFLARE_ACCOUNT_ID:-}" ] && [ -n "${CLOUDFLARE_API_TOKEN:-}" ]; then
  echo "==> Syncing Cloudflare Access policies"
  CLOUDFLARE_ACCOUNT_ID="$CLOUDFLARE_ACCOUNT_ID" CLOUDFLARE_API_TOKEN="$CLOUDFLARE_API_TOKEN" \
    python3 "$REPO_ROOT/scripts/sync_access.py"
else
  echo "==> Skipping Access sync (CLOUDFLARE_ACCOUNT_ID / CLOUDFLARE_API_TOKEN not set)"
fi

echo "==> Done"
