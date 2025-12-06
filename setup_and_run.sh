#!/bin/bash
set -e

echo "--- Starting Automated Julius Deployer Setup ---"

# 1. Run bootstrap to create venv and install dependencies
python3 bootstrap.py --project-path "$(pwd)"

# 2. Run an immediate deployment cycle
echo "\n--- Running an immediate deployment cycle ---"
python3 run_immediate.py

echo "\n--- Setup and immediate run complete. ---"
