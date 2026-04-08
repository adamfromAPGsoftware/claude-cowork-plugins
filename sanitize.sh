#!/usr/bin/env bash
# ═══════════════════════════════════════════════════════════════════════════════
# sanitize.sh — Sync private APG plugins → public sanitized plugins
# ═══════════════════════════════════════════════════════════════════════════════
#
# Usage:
#   bash sanitize.sh --source ~/Documents/Repositories/APG-AI-Operating-System \
#                    --target ~/staging/public-plugins
#
#   bash sanitize.sh --source <path> --target <path> --check-only
#
# Phases:
#   1. Copy plugin directories (excluding blacklisted paths)
#   2. Rename apg-{domain}-plugin → {domain}-plugin
#   3. Global find-and-replace from sanitize-rules.json
#   4. Template replacement for business-specific files
#   5. Sensitive pattern scan → SANITIZE_REPORT.txt
#   6. Diff against previous sync (if exists)
# ═══════════════════════════════════════════════════════════════════════════════

set -euo pipefail

# ─── Parse Arguments ──────────────────────────────────────────────────────────

SOURCE=""
TARGET=""
CHECK_ONLY=false
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
RULES_FILE="$SCRIPT_DIR/sanitize-rules.json"
TEMPLATES_DIR="$SCRIPT_DIR/_templates"

while [[ $# -gt 0 ]]; do
  case $1 in
    --source) SOURCE="$2"; shift 2 ;;
    --target) TARGET="$2"; shift 2 ;;
    --rules) RULES_FILE="$2"; shift 2 ;;
    --check-only) CHECK_ONLY=true; shift ;;
    -h|--help)
      echo "Usage: bash sanitize.sh --source <private-repo-path> --target <staging-dir>"
      echo ""
      echo "Options:"
      echo "  --source       Path to the private APG-AI-Operating-System repo"
      echo "  --target       Path to staging directory for sanitized output"
      echo "  --rules        Path to sanitize-rules.json (default: ./sanitize-rules.json)"
      echo "  --check-only   Dry run: only scan for sensitive patterns, don't copy"
      echo ""
      exit 0
      ;;
    *) echo "Unknown option: $1"; exit 1 ;;
  esac
done

if [[ -z "$SOURCE" || -z "$TARGET" ]]; then
  echo "ERROR: --source and --target are required"
  echo "Run: bash sanitize.sh --help"
  exit 1
fi

if [[ ! -d "$SOURCE" ]]; then
  echo "ERROR: Source directory does not exist: $SOURCE"
  exit 1
fi

if [[ ! -f "$RULES_FILE" ]]; then
  echo "ERROR: Rules file not found: $RULES_FILE"
  exit 1
fi

# Check for jq (required for parsing JSON rules)
if ! command -v jq &> /dev/null; then
  echo "ERROR: jq is required. Install with: brew install jq"
  exit 1
fi

REPORT_FILE="$SCRIPT_DIR/SANITIZE_REPORT.txt"
PLUGINS=("apg-sales-plugin" "apg-audit-plugin" "apg-content-plugin" "apg-marketing-plugin" "apg-video-plugin" "apg-finance-plugin" "apg-social-plugin")

echo "═══════════════════════════════════════════════════════════════"
echo "  Sanitize: Private → Public Plugin Sync"
echo "═══════════════════════════════════════════════════════════════"
echo "  Source:    $SOURCE"
echo "  Target:    $TARGET"
echo "  Rules:     $RULES_FILE"
echo "  Templates: $TEMPLATES_DIR"
echo "  Mode:      $(if $CHECK_ONLY; then echo 'CHECK ONLY'; else echo 'FULL SYNC'; fi)"
echo "═══════════════════════════════════════════════════════════════"
echo ""

# ─── Phase 1: Copy ────────────────────────────────────────────────────────────

if ! $CHECK_ONLY; then
  echo "Phase 1/6: Copying plugin directories..."

  # Clean staging target
  rm -rf "$TARGET"
  mkdir -p "$TARGET"

  for plugin in "${PLUGINS[@]}"; do
    if [[ ! -d "$SOURCE/$plugin" ]]; then
      echo "  WARNING: Plugin directory not found: $SOURCE/$plugin"
      continue
    fi

    echo "  Copying $plugin..."
    rsync -a \
      --exclude='.env' \
      --exclude='.gmail-token.json' \
      --exclude='ga4-service-account.json' \
      --exclude='data/marketing-data.json' \
      --exclude='data/finance-data.json' \
      --exclude='data/social-data.json' \
      --exclude='data/adamgoodyer/' \
      --exclude='data/apgsoftware/' \
      --exclude='accounts/adamgoodyer/' \
      --exclude='debug/' \
      --exclude='.browser-data/' \
      --exclude='*-sidecar/' \
      --exclude='*.mp4' \
      --exclude='*.mov' \
      --exclude='*.mp4.part' \
      --exclude='*.mp4.ytdl' \
      --exclude='*.m4a' \
      --exclude='*.wav' \
      --exclude='*.mp3' \
      --exclude='__pycache__/' \
      --exclude='*.pyc' \
      --exclude='.DS_Store' \
      --exclude='node_modules/' \
      "$SOURCE/$plugin/" "$TARGET/$plugin/"
  done

  # Remove client-specific follow-up emails if they exist
  find "$TARGET" -name "james-*" -delete 2>/dev/null || true
  find "$TARGET" -name "dale-*" -delete 2>/dev/null || true

  # For social plugin: rename apgsoftware account to example-account
  if [[ -d "$TARGET/apg-social-plugin/accounts/apgsoftware" ]]; then
    mv "$TARGET/apg-social-plugin/accounts/apgsoftware" "$TARGET/apg-social-plugin/accounts/example-account"
    echo "  Renamed social account: apgsoftware → example-account"
  fi

  # Rename any files containing "adamgoodyer" or "apgsoftware" in their names
  find "$TARGET" -type f -name "*adamgoodyer*" 2>/dev/null | while read -r file; do
    dir=$(dirname "$file")
    base=$(basename "$file")
    newbase=$(echo "$base" | sed 's/adamgoodyer/example-account/g')
    mv "$file" "$dir/$newbase"
    echo "  Renamed file: $base → $newbase"
  done
  find "$TARGET" -type f -name "*apgsoftware*" 2>/dev/null | while read -r file; do
    dir=$(dirname "$file")
    base=$(basename "$file")
    newbase=$(echo "$base" | sed 's/apgsoftware/example-account-2/g')
    mv "$file" "$dir/$newbase"
    echo "  Renamed file: $base → $newbase"
  done

  echo "  Done."
  echo ""

  # ─── Phase 2: Rename ──────────────────────────────────────────────────────────

  echo "Phase 2/6: Renaming plugin directories..."

  # Read renames from rules
  jq -r '.directory_renames | to_entries[] | "\(.key)\t\(.value)"' "$RULES_FILE" | while IFS=$'\t' read -r old_name new_name; do
    if [[ -d "$TARGET/$old_name" ]]; then
      mv "$TARGET/$old_name" "$TARGET/$new_name"
      echo "  $old_name → $new_name"
    fi
  done

  echo "  Done."
  echo ""

  # ─── Phase 3: Global Find-and-Replace ──────────────────────────────────────────

  echo "Phase 3/6: Applying global find-and-replace rules..."

  REPLACEMENT_COUNT=$(jq '.global_replacements | length' "$RULES_FILE")
  echo "  Applying $REPLACEMENT_COUNT replacement rules..."

  # Use Python for reliable find-and-replace (handles special chars, @, $, etc.)
  python3 - "$RULES_FILE" "$TARGET" <<'PYEOF'
import json, sys, os, glob

rules_file = sys.argv[1]
target_dir = sys.argv[2]

with open(rules_file) as f:
    rules = json.load(f)

replacements = [(r["find"], r["replace"]) for r in rules["global_replacements"]]

TEXT_EXTENSIONS = {
    ".md", ".json", ".py", ".sh", ".html", ".txt",
    ".yaml", ".yml", ".css", ".js", ".toml", ".csv"
}

file_count = 0
for root, dirs, files in os.walk(target_dir):
    for fname in files:
        ext = os.path.splitext(fname)[1].lower()
        if ext not in TEXT_EXTENSIONS:
            continue
        fpath = os.path.join(root, fname)
        try:
            with open(fpath, "r", encoding="utf-8", errors="replace") as f:
                content = f.read()
        except Exception:
            continue

        original = content
        for find_str, replace_str in replacements:
            content = content.replace(find_str, replace_str)

        if content != original:
            with open(fpath, "w", encoding="utf-8") as f:
                f.write(content)
            file_count += 1

print(f"  Modified {file_count} files.")
PYEOF

  echo "  Done."
  echo ""

  # ─── Phase 4: Template Replacement ────────────────────────────────────────────

  echo "Phase 4/6: Replacing business-specific files with templates..."

  jq -r '.file_replacements[] | "\(.source)\t\(.template)"' "$RULES_FILE" | while IFS=$'\t' read -r source_path template_path; do
    # Map the source path to the renamed directory
    # e.g., apg-audit-plugin/references/apg-pricing.md → audit-plugin/references/apg-pricing.md
    renamed_path=$(echo "$source_path" | sed 's/^apg-\([a-z]*\)-plugin/\1-plugin/')
    target_file="$TARGET/$renamed_path"
    template_file="$SCRIPT_DIR/$template_path"

    if [[ -f "$template_file" ]]; then
      if [[ -f "$target_file" ]]; then
        cp "$template_file" "$target_file"
        echo "  Replaced: $renamed_path"
      else
        # The file might have been renamed by global replacements or the path changed
        # Try to find it
        base_name=$(basename "$source_path")
        found=$(find "$TARGET" -name "$base_name" -type f 2>/dev/null | head -1)
        if [[ -n "$found" ]]; then
          cp "$template_file" "$found"
          echo "  Replaced: $found (found by name)"
        else
          echo "  SKIP: $renamed_path (not found in staging)"
        fi
      fi
    else
      echo "  WARNING: Template not found: $template_path"
    fi
  done

  echo "  Done."
  echo ""
fi

# ─── Phase 5: Sensitive Pattern Scan ──────────────────────────────────────────

SCAN_DIR="$TARGET"
if $CHECK_ONLY; then
  SCAN_DIR="$SOURCE"
  echo "Phase 5/6: Scanning source for sensitive patterns (check-only mode)..."
else
  echo "Phase 5/6: Scanning staging for remaining sensitive patterns..."
fi

echo "" > "$REPORT_FILE"
echo "═══════════════════════════════════════════════════════════" >> "$REPORT_FILE"
echo "  SANITIZE REPORT — $(date '+%Y-%m-%d %H:%M:%S')" >> "$REPORT_FILE"
echo "  Scanned: $SCAN_DIR" >> "$REPORT_FILE"
echo "═══════════════════════════════════════════════════════════" >> "$REPORT_FILE"
echo "" >> "$REPORT_FILE"

TOTAL_MATCHES=0

# Read sensitive patterns from rules
jq -r '.sensitive_patterns[]' "$RULES_FILE" | while IFS= read -r pattern; do
  # Search for pattern in all text files
  matches=$(grep -rn --include="*.md" --include="*.json" --include="*.py" \
    --include="*.sh" --include="*.html" --include="*.txt" --include="*.yaml" \
    --include="*.yml" --include="*.js" --include="*.css" --include="*.toml" \
    --exclude="SANITIZE_REPORT.txt" --exclude="SANITIZE_DIFF.txt" \
    --exclude="sanitize-rules.json" --exclude="sanitize.sh" \
    -E "$pattern" "$SCAN_DIR" 2>/dev/null || true)

  if [[ -n "$matches" ]]; then
    count=$(echo "$matches" | wc -l | tr -d ' ')
    echo "FOUND [$count matches]: $pattern" >> "$REPORT_FILE"
    echo "$matches" | head -20 >> "$REPORT_FILE"
    if [[ $count -gt 20 ]]; then
      echo "  ... and $((count - 20)) more matches" >> "$REPORT_FILE"
    fi
    echo "" >> "$REPORT_FILE"
    TOTAL_MATCHES=$((TOTAL_MATCHES + count))
  fi
done

# Count total matches from report
MATCH_LINES=$(grep -c "^FOUND" "$REPORT_FILE" 2>/dev/null || echo "0")

if [[ "$MATCH_LINES" -gt 0 ]]; then
  echo "  WARNING: Found $MATCH_LINES sensitive pattern categories with matches!"
  echo "  Review: $REPORT_FILE"
else
  echo "  CLEAN: No sensitive patterns detected."
fi

echo "" >> "$REPORT_FILE"
echo "═══════════════════════════════════════════════════════════" >> "$REPORT_FILE"
echo "  Pattern categories with matches: $MATCH_LINES" >> "$REPORT_FILE"
echo "═══════════════════════════════════════════════════════════" >> "$REPORT_FILE"

echo "  Report saved to: $REPORT_FILE"
echo ""

# ─── Phase 6: Diff ───────────────────────────────────────────────────────────

if ! $CHECK_ONLY; then
  # Check if the public repo already has plugin directories
  PUBLIC_REPO="$SCRIPT_DIR"
  HAS_EXISTING=false

  for plugin_dir in sales-plugin audit-plugin content-plugin marketing-plugin video-plugin finance-plugin social-plugin; do
    if [[ -d "$PUBLIC_REPO/$plugin_dir" ]]; then
      HAS_EXISTING=true
      break
    fi
  done

  if $HAS_EXISTING; then
    echo "Phase 6/6: Generating diff against existing public repo..."
    DIFF_FILE="$SCRIPT_DIR/SANITIZE_DIFF.txt"

    diff -r --brief "$TARGET" "$PUBLIC_REPO" \
      --exclude='.git' \
      --exclude='_templates' \
      --exclude='sanitize*' \
      --exclude='SANITIZE_*' \
      --exclude='staging' \
      --exclude='.gitignore' \
      --exclude='LICENSE' \
      --exclude='README.md' \
      --exclude='SETUP.md' \
      --exclude='config.example.json' \
      --exclude='.env.example' \
      > "$DIFF_FILE" 2>/dev/null || true

    if [[ -s "$DIFF_FILE" ]]; then
      DIFF_LINES=$(wc -l < "$DIFF_FILE" | tr -d ' ')
      echo "  Found $DIFF_LINES differences. Review: $DIFF_FILE"
    else
      echo "  No differences found."
      rm -f "$DIFF_FILE"
    fi
  else
    echo "Phase 6/6: No existing plugins in public repo — skipping diff."
  fi

  echo ""
fi

# ─── Summary ──────────────────────────────────────────────────────────────────

echo "═══════════════════════════════════════════════════════════"
if $CHECK_ONLY; then
  echo "  Check complete. Review: $REPORT_FILE"
else
  echo "  Sync complete!"
  echo ""
  echo "  Staging directory: $TARGET"
  echo "  Report: $REPORT_FILE"
  echo ""
  echo "  Next steps:"
  echo "    1. Review SANITIZE_REPORT.txt for any remaining sensitive data"
  echo "    2. Spot-check a few SKILL.md and .mcp.json files"
  echo "    3. Copy staging to public repo:"
  echo "       cp -r $TARGET/* $SCRIPT_DIR/"
  echo "    4. Review, commit, and push"
fi
echo "═══════════════════════════════════════════════════════════"
