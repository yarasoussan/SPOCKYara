#!/usr/bin/env bash
# Log MCP tool usage to JSONL for analysis.
# Called by Claude Code hooks on PostToolUse and PostToolUseFailure events.
# Receives hook event JSON on stdin.
#
# Output: appends one JSON line per event to usage/multiomics-kg-usage.jsonl
# INSIDE THE REPO (un-ignored — see .gitignore). Testers commit usage/ alongside
# their per-milestone analysis commits, so logs ride along on every push and the
# maintainer aggregates by pulling forks (design spec §9).
#
# Fields: timestamp, template_version, event, session_id, tool_name, tool_input,
#          response_keys, truncated, total_matching, returned, error (if failure)
#
# The template version is stamped per line (read from VERSION). The explorer +
# KG versions complete the "version triple" and are recorded once per run by
# scripts/preflight.sh (it has a live KG connection; this hook does not).

set -euo pipefail

# jq is required to shape the event JSON (README prerequisites; preflight goes RED
# without it). If it is missing anyway, skip logging rather than failing the hook
# on every KG call — a broken hook must not block analysis.
command -v jq >/dev/null 2>&1 || exit 0

# ${CLAUDE_PROJECT_DIR} is set by Claude Code to the repo root. Fall back to the
# script's own parent dir so the hook still works if launched out of band.
PROJECT_DIR="${CLAUDE_PROJECT_DIR:-$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)}"

LOG_DIR="${PROJECT_DIR}/usage"
LOG_FILE="${LOG_DIR}/multiomics-kg-usage.jsonl"
mkdir -p "$LOG_DIR"

# Template version (best-effort): VERSION file, else `git describe`, else "unknown".
TEMPLATE_VERSION="unknown"
if [[ -f "${PROJECT_DIR}/VERSION" ]]; then
  TEMPLATE_VERSION="$(tr -d '[:space:]' < "${PROJECT_DIR}/VERSION")"
elif command -v git >/dev/null 2>&1; then
  TEMPLATE_VERSION="$(git -C "$PROJECT_DIR" describe --tags --always 2>/dev/null || echo unknown)"
fi

# Read full stdin (hook event JSON)
INPUT=$(cat)

# Extract fields with jq, adding timestamp + template_version.
# tool_response arrives as a JSON string, so parse it first.
echo "$INPUT" | jq -c --arg tv "$TEMPLATE_VERSION" '{
  timestamp: (now | todate),
  template_version: $tv,
  event: .hook_event_name,
  session_id: .session_id,
  tool_name: .tool_name,
  tool_input: .tool_input,
} + (.tool_response | fromjson? // {} |
  # Only an object response carries these keys; an array or scalar must not crash
  # the hook. Read fields directly (missing → null) — `// null` would turn false into null.
  if type == "object" then
    {response_keys: keys, truncated: .truncated, total_matching: .total_matching, returned: .returned}
  else
    {response_keys: null, truncated: null, total_matching: null, returned: null}
  end) + {
  error: (.error // null)
}' | tr -d '\015' >> "$LOG_FILE"   # jq on Windows ends lines with CRLF; keep the log LF-only

# Exit 0 = success, non-blocking
exit 0
