#!/usr/bin/env bash
# run-tests.sh — Run all script tests for bmad-apg-agent-close
# Usage: bash scripts/run-tests.sh

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
TESTS_DIR="$SCRIPT_DIR/tests"
PASS=0
FAIL=0

run_test() {
  local name="$1"
  local file="$2"
  echo "Running: $name"
  if python3 "$file"; then
    PASS=$((PASS + 1))
  else
    FAIL=$((FAIL + 1))
    echo "FAILED: $name"
  fi
  echo "---"
}

run_test "waste-calculator" "$TESTS_DIR/test_waste_calculator.py"
run_test "payback-gate" "$TESTS_DIR/test_payback_gate.py"
run_test "validate-audit-data-lite" "$TESTS_DIR/test_validate_audit_data_lite.py"

echo ""
echo "Results: $PASS passed, $FAIL failed"

if [ "$FAIL" -gt 0 ]; then
  exit 1
fi
