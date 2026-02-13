#!/usr/bin/env bash
set -euo pipefail
IFS=$'\n\t'

ROOT="$(pwd)"
TS="$(date -u +%Y%m%dT%H%M%SZ)"
LOG_DIR="${ROOT}/logs"
ARTIFACT_DIR="${ROOT}/artifacts"
mkdir -p "$LOG_DIR" "$ARTIFACT_DIR"

LOG_FILE="${LOG_DIR}/setup_and_run_${TS}.log"
# tee all output to log file (but still keep exit statuses)
exec > >(tee -a "$LOG_FILE") 2>&1

trap 'rc=$?; echo "Exiting with status ${rc}. Log: ${LOG_FILE}"; exit $rc' EXIT

usage() {
  cat <<EOF
Usage: $(basename "$0") [--no-bootstrap] [--no-run] [--venv PATH] [--dry-run]
Options:
  --no-bootstrap     Skip running bootstrap.py
  --no-run           Skip running run_immediate.py
  --venv PATH        Virtualenv directory to create/use (default: .venv)
  --dry-run          Print actions but do not execute major steps
EOF
  exit 1
}

# defaults
DO_BOOTSTRAP=1
DO_RUN=1
VENV_DIR=".venv"
DRY_RUN=0

while [[ $# -gt 0 ]]; do
  case "$1" in
    --no-bootstrap) DO_BOOTSTRAP=0; shift ;;
    --no-run) DO_RUN=0; shift ;;
    --venv) VENV_DIR="$2"; shift 2 ;;
    --dry-run) DRY_RUN=1; shift ;;
    -h|--help) usage ;;
    *) echo "Unknown arg: $1"; usage ;;
  esac
done

echo "--- Start Automated Julius Deployer Setup ---"
echo "ROOT=$ROOT"
echo "VENV_DIR=$VENV_DIR"
echo "Timestamp=$TS"
if [[ "$DRY_RUN" -eq 1 ]]; then
  echo "DRY RUN: no major actions will be executed"
fi

run_cmd() {
  if [[ "$DRY_RUN" -eq 1 ]]; then
    echo "[DRY] $*"
    return 0
  fi
  echo "+ $*"
  "$@"
}

# ensure python3 available
if ! command -v python3 >/dev/null 2>&1; then
  echo "ERROR: python3 is required but not found in PATH" >&2
  exit 2
fi

PYTHON_EXEC="$(command -v python3)"

# create venv if missing
if [[ ! -d "$VENV_DIR" ]]; then
  echo "Creating virtualenv at $VENV_DIR"
  if [[ "$DRY_RUN" -eq 0 ]]; then
    "$PYTHON_EXEC" -m venv "$VENV_DIR"
  fi
else
  echo "Using existing virtualenv at $VENV_DIR"
fi

VENV_PYTHON="${VENV_DIR}/bin/python"
if [[ ! -x "$VENV_PYTHON" ]]; then
  # on Windows or if not present fallback
  VENV_PYTHON="${VENV_DIR}/Scripts/python.exe"
fi

if [[ "$DRY_RUN" -eq 0 ]] && [[ -x "$VENV_PYTHON" ]]; then
  echo "Upgrading pip inside venv"
  "$VENV_PYTHON" -m pip install --upgrade pip setuptools wheel >/dev/null || true
  if [[ -f "python/requirements.txt" ]]; then
    echo "Installing Python requirements from python/requirements.txt"
    "$VENV_PYTHON" -m pip install -r python/requirements.txt
  fi
fi

# Run bootstrap.py if present and not skipped
if [[ "$DO_BOOTSTRAP" -eq 1 ]]; then
  if [[ -f "bootstrap.py" ]]; then
    echo "--- Running bootstrap.py ---"
    run_cmd "$VENV_PYTHON" "bootstrap.py" --project-path "$ROOT"
  else
    echo "bootstrap.py not found; skipping"
  fi
else
  echo "Skipping bootstrap step by user request"
fi

# Run run_immediate.py if present and not skipped
if [[ "$DO_RUN" -eq 1 ]]; then
  if [[ -f "run_immediate.py" ]]; then
    echo "--- Running run_immediate.py ---"
    run_cmd "$VENV_PYTHON" "run_immediate.py"
  else
    echo "run_immediate.py not found; skipping"
  fi
else
  echo "Skipping immediate run by user request"
fi

echo "--- Setup and run finished; logs: ${LOG_FILE} ---"
# write a small artifact status file
cat > "${ARTIFACT_DIR}/setup_summary_${TS}.json" <<EOF
{
  "timestamp": "${TS}",
  "venv": "${VENV_DIR}",
  "bootstrap_run": ${DO_BOOTSTRAP},
  "run_immediate": ${DO_RUN},
  "log": "${LOG_FILE}"
}
EOF
