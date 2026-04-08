#!/bin/bash
# Auto-regenerate existing HTML deliverables when audit-data.json is updated.
# Only regenerates files that already exist in the client's deliverables/ folder.
# Called by Claude Code hook after audit-data.json write.

AUDIT_FILE="$1"
if [ -z "$AUDIT_FILE" ]; then
  echo "Usage: auto-regen-deliverables.sh <path-to-audit-data.json>"
  exit 1
fi

# Extract client slug from path: clients/{slug}/audit/audit-data.json
CLIENT_DIR=$(dirname "$(dirname "$AUDIT_FILE")")
CLIENT_SLUG=$(basename "$CLIENT_DIR")
DELIVERABLES_DIR="$CLIENT_DIR/deliverables"
SCRIPT_DIR="$(cd "$(dirname "$0")/../.claude/skills/bmad-apg-agent-generator/scripts" && pwd)"
GENERATE_PY="$SCRIPT_DIR/generate.py"

if [ ! -d "$DELIVERABLES_DIR" ]; then
  exit 0  # No deliverables folder yet, nothing to regenerate
fi

if [ ! -f "$GENERATE_PY" ]; then
  echo "Warning: generate.py not found at $GENERATE_PY"
  exit 1
fi

# Map deliverable filenames to generate.py output types
declare -A FILE_TO_OUTPUT
FILE_TO_OUTPUT["process-map.html"]="process-map"
FILE_TO_OUTPUT["client-website.html"]="client-website"
FILE_TO_OUTPUT["findings.html"]="findings"
FILE_TO_OUTPUT["waste.html"]="waste"
FILE_TO_OUTPUT["priority-matrix.html"]="priority-matrix"
FILE_TO_OUTPUT["transformation-blueprint.html"]="transformation-blueprint"
FILE_TO_OUTPUT["audit-report.html"]="audit-report"
FILE_TO_OUTPUT["costed-plans.html"]="costed-plans"
FILE_TO_OUTPUT["solutions-overview.html"]="solutions-overview"

REGENERATED=0
for FILE in "${!FILE_TO_OUTPUT[@]}"; do
  if [ -f "$DELIVERABLES_DIR/$FILE" ]; then
    OUTPUT_TYPE="${FILE_TO_OUTPUT[$FILE]}"
    python3 "$GENERATE_PY" --client-slug "$CLIENT_SLUG" --output "$OUTPUT_TYPE" 2>/dev/null
    if [ $? -eq 0 ]; then
      REGENERATED=$((REGENERATED + 1))
    fi
  fi
done

if [ $REGENERATED -gt 0 ]; then
  echo "Auto-regenerated $REGENERATED deliverable(s) for $CLIENT_SLUG"
fi
