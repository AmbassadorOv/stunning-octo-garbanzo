import os
import subprocess
import time
import sys
import json
import requests
import fire
from datetime import datetime
from dotenv import load_dotenv

# --- Configuration & Constants ---

# 7200 seconds = 2 hours. This is the time the script will sleep between chunks.
DEPLOYMENT_INTERVAL_SECONDS = 7200
DOCKER_COMPOSE_FILE = "docker-compose.yml"
STATE_FILE = "deployment_state.txt"
ORCHESTRATOR_URL = "http://localhost:8000"
# Ensure this task file exists in your project structure for validation
JULIUS_TASK_FILE = 'tests/julius_eagles_task.json'

STAGES = {
    "BUILD_IMAGES": "Stage 1: Building Docker Images",
    "DEPLOY_SERVICES": "Stage 2: Deploying Services (Docker Up)",
    "VALIDATE_SETUP": "Stage 3: Running Smoke Tests (Julius Agent Validation)",
    "CYCLE_COMPLETE": "Cycle Complete - Resetting"
}
INITIAL_STATE = "BUILD_IMAGES"

# --- Utility Functions ---

def load_environment():
    """Load environment variables from a .env file."""
    load_dotenv()
    if not os.getenv("JULIUS_API_TOKEN"):
        print("[WARNING] JULIUS_API_TOKEN not found. Deployment continues, but Julius Agent may fail.")

def read_state():
    """Reads the last completed stage from the state file."""
    if not os.path.exists(STATE_FILE):
        return INITIAL_STATE
    with open(STATE_FILE, 'r') as f:
        state = f.read().strip()
        return state if state in STAGES else INITIAL_STATE

def write_state(stage):
    """Writes the current stage to the state file."""
    with open(STATE_FILE, 'w') as f:
        f.write(stage)

# --- CLI and Deployment Orchestration Class ---

class DeploymentCLI:
    """
    Command-Line Interface for managing the Julius 'Big Eagles' automation deployment.

    Use 'python automated_julius_deployer.py [command]'
    e.g., 'python automated_julius_deployer.py run_scheduler'
    """

    def __init__(self):
        load_environment()

    def _run_subprocess_command(self, cmd, stage_name, success_state):
        """Helper to run Docker commands and manage state updates."""
        print(f"[{stage_name}] - Starting execution.")
        try:
            # Stop existing containers before build/up for fresh deployment
            if "build" in cmd:
                subprocess.run(["docker", "compose", "-f", DOCKER_COMPOSE_FILE, "stop"], check=False)

            result = subprocess.run(
                cmd,
                check=True,
                capture_output=True,
                text=True
            )
            print(f"[{stage_name}] - ✅ Success.")
            if success_state:
                write_state(success_state)
            return True
        except subprocess.CalledProcessError as e:
            print(f"[{stage_name}] - ❌ ERROR: Command failed. Stderr:\n{e.stderr}")
            return False
        except FileNotFoundError:
            print(f"[{stage_name}] - ❌ ERROR: Docker or docker-compose not found. Is Docker installed?")
            return False

    # --- CLI Callable Methods (Individual Chunks) ---

    def build_images(self):
        """Builds all Docker images for the project."""
        cmd = ["docker", "compose", "-f", DOCKER_COMPOSE_FILE, "build"]
        return self._run_subprocess_command(cmd, STAGES['BUILD_IMAGES'], None)

    def deploy_services(self):
        """Deploys/restarts all services locally using Docker Compose."""
        cmd = ["docker", "compose", "-f", DOCKER_COMPOSE_FILE, "up", "-d", "--remove-orphans"]
        return self._run_subprocess_command(cmd, STAGES['DEPLOY_SERVICES'], None)

    def validate_setup(self):
        """Runs the smoke test against the orchestrator for Julius Agent validation."""
        stage_name = STAGES['VALIDATE_SETUP']
        print(f"[{stage_name}] - Running Julius Agent validation test.")

        try:
            with open(JULIUS_TASK_FILE, 'r') as f:
                task_policy = json.load(f)

            # 1. Post the TaskPolicy
            response_task = requests.post(f"{ORCHESTRATOR_URL}/task", json=task_policy, timeout=30)
            response_task.raise_for_status()

            # 2. Call /execute_step
            response_exec = requests.post(f"{ORCHESTRATOR_URL}/execute_step", json=task_policy, timeout=120)
            response_exec.raise_for_status()
            result = response_exec.json()

            if result.get('status') == 'SUCCESS' and result.get('agent_type') == 'JULIUS':
                print(f"[{stage_name}] - ✅ Validation passed. Julius Agent is operational.")
                return True
            else:
                print(f"[{stage_name}] - ⚠️ WARNING: Task status was not SUCCESS. Result: {result.get('status')}")
                return False

        except requests.exceptions.RequestException as e:
            print(f"[{stage_name}] - ❌ ERROR: Validation failed (Orchestrator not reachable/Task failed): {e}")
            return False
        except FileNotFoundError:
            print(f"[{stage_name}] - ❌ ERROR: Task fixture file ({JULIUS_TASK_FILE}) not found.")
            return False

    # --- Main Scheduler Method ---

    def run_scheduler(self):
        """
        The main loop: Executes the chunked deployment cycle every 2 hours
        based on the last saved state.
        """
        print(f"--- Julius 'Big Eagles' Project Automated Scheduler Initialized ---")
        print(f"Recurrence: Every {DEPLOYMENT_INTERVAL_SECONDS / 3600} hours")
        print("Press Ctrl+C to stop the scheduler.")

        while True:
            now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            current_state = read_state()
            print(f"\n--- Starting Recurring Cycle at {now} (State: {STAGES.get(current_state, 'Unknown')}) ---")

            stage_mapping = {
                "BUILD_IMAGES": (self.build_images, "DEPLOY_SERVICES"),
                "DEPLOY_SERVICES": (self.deploy_services, "VALIDATE_SETUP"),
                "VALIDATE_SETUP": (self.validate_setup, "CYCLE_COMPLETE")
            }

            if current_state == "CYCLE_COMPLETE":
                print(f"[{STAGES['CYCLE_COMPLETE']}] - Full setup verified. Restarting full deployment cycle.")
                write_state(INITIAL_STATE)
                current_state = INITIAL_STATE

            if current_state in stage_mapping:
                func, next_state = stage_mapping[current_state]

                # Execute the stage
                success = func()

                # Update state only if execution was successful
                if success:
                    write_state(next_state)
                else:
                    # If failed, the current_state remains the same for retry on next run
                    print(f"Failure in {current_state}. Will retry this stage in 2 hours.")

            print(f"--- Cycle Chunk Complete. Next check scheduled in {DEPLOYMENT_INTERVAL_SECONDS / 3600} hours. ---")

            try:
                print(f"Scheduler sleeping for {DEPLOYMENT_INTERVAL_SECONDS} seconds...")
                time.sleep(DEPLOYMENT_INTERVAL_SECONDS)
            except KeyboardInterrupt:
                print("\nScheduler stopped by user (KeyboardInterrupt). Exiting.")
                break
            except Exception as e:
                print(f"\nAn unexpected error occurred during the sleep: {e}. Sleeping for 5 minutes and restarting.")
                time.sleep(300)


if __name__ == "__main__":
    try:
        # Use python-fire to expose all public methods of the class as CLI commands
        fire.Fire(DeploymentCLI)
    except Exception as e:
        print(f"A critical error occurred: {e}")
