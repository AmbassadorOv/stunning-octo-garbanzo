#!/bin/bash

# run_agent.sh

# Edit PROJECT_DIR and PYTHON_BIN before use
PROJECT_DIR="/app"
PYTHON_BIN="/app/.venv/bin/python"   # or /usr/bin/python3

cd "$PROJECT_DIR" || { echo "Cannot cd to $PROJECT_DIR"; exit 1; }

# Optional: activate virtualenv if you prefer activation over direct python path
# source .venv/bin/activate

# Ensure reports and logs directories exist
mkdir -p reports logs

# Run the agent script (agent.py must be in PROJECT_DIR)
exec "$PYTHON_BIN" agent.py run --csv data/phenons.csv --json data/experiments.json --out reports/report.html --out-csv reports/merged.csv --interval-minutes 60
