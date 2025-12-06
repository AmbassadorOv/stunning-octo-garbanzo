# Automated Julius Deployer - Bundle & Quick Installer

This bundle contains an automated Julius deployment script plus a small Python bootstrapper to prepare an environment and run a single deployment immediately.

Included files:
- python/requirements.txt
- .env.example
- automated_julius_deployer.py
- run_immediate.py
- bootstrap.py
- systemd/deployer.service
- systemd/deployer.timer

Quick usage:
- To run the automated setup and an immediate deployment cycle, simply run the following command:

  ./setup_and_run.sh

- For manual setup:
  1. Inspect and copy `.env.example` to `.env` and fill values (or let the installer create one for you).
  2. Prepare environment and install dependencies (creates a `venv` by default):

     python3 bootstrap.py --project-path "$(pwd)"

  3. To run a single chunk immediately for testing:

     python3 run_immediate.py

4. To start the daily scheduler manually:

   python3 automated_julius_deployer.py run_scheduler

5. (Optional) Follow printed instructions to enable the systemd unit/timer if you want system-level scheduling.

Notes:
- The installer will not enable systemd units without confirmation and will not automatically run privileged commands unless you pass --install-systemd (it will still prompt).
- If you prefer cron, the README earlier contains an example cron line.
