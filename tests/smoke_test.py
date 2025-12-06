import requests
import json
import os
import time

ORCHESTRATOR_URL = "http://app:8000"
JULIUS_TASK_FILE = 'tests/julius_eagles_task.json'

def wait_for_server():
    """Waits for the server to be available."""
    for _ in range(30):
        try:
            response = requests.get(f"{ORCHESTRATOR_URL}/docs")
            if response.status_code == 200:
                print("[INFO] Server is up.")
                return True
        except requests.exceptions.ConnectionError:
            pass
        time.sleep(1)
    print("[ERROR] Server did not start in time.")
    return False

def run_julius_test():
    """Tests the Julius Agent integration by posting a data analysis task."""
    try:
        with open(JULIUS_TASK_FILE, 'r') as f:
            task_policy = json.load(f)

        task_id = task_policy['task_id']

        response_exec = requests.post(f"{ORCHESTRATOR_URL}/execute_step", json=task_policy)
        response_exec.raise_for_status()

        result = response_exec.json()

        if result.get('status') == 'SUCCESS' and result.get('agent_name') == 'Julius':
            print(f"[SUCCESS] Julius Agent (Task {task_id}) passed. Result snippet: {result['result_data'][:60]}...")
            return True
        else:
            print(f"[FAILURE] Julius Agent (Task {task_id}) failed. Result: {result}")
            return False

    except requests.exceptions.RequestException as e:
        print(f"[ERROR] Julius Test failed due to network/API error: {e}")
        return False

def main():
    if not wait_for_server():
        return

    print("\n--- Running Julius 'Big Eagles' Agent Test ---")
    julius_success = run_julius_test()

    if julius_success:
        print("\n✅ All agent tests passed.")
    else:
        print("\n❌ One or more agent tests failed.")
        exit(1)

if __name__ == "__main__":
    main()
