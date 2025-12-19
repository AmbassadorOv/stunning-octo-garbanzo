import requests
import time
import json
import os

BASE_URL = "http://localhost:8080"

def wait_for_server():
    """Waits for the server to be available."""
    print("--- Waiting for server to start ---")
    # Using /audit as the health check endpoint
    for _ in range(30):
        try:
            response = requests.get(f"{BASE_URL}/audit")
            if response.status_code == 200:
                print("--- Server is up ---")
                return True
        except requests.exceptions.ConnectionError:
            pass
        time.sleep(1)
    print("--- Server did not start in time ---")
    return False

def test_audit_endpoint():
    print("--- Testing /audit endpoint ---")
    response = requests.get(f"{BASE_URL}/audit")
    assert response.status_code == 200
    data = response.json()
    assert data["audit"] == "Success"
    assert data["mode"] == "Bottom-to-Top"
    print("--- GET /audit: OK ---")

def test_orchestrate_endpoint():
    print("--- Testing /orchestrate endpoint ---")
    if not os.getenv("OPENAI_API_KEY") or not os.getenv("GEMINI_API_KEY"):
        print("--- SKIPPING /orchestrate test: API keys not set in environment ---")
        return

    payload = {
        "context_id": "test-001",
        "prompt": "Database write errors on service payments since 03:00 UTC. Show root-cause hypotheses and minimal remediation steps.",
        "goal": "restore payment writes within 15 minutes",
        "max_tokens": 400,
        "temperature": 0.1,
        "hex_step": "A",
        "reverse_sequence": True
    }

    response = requests.post(f"{BASE_URL}/orchestrate", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert "estimate" in data
    assert "consensus" in data
    assert "active_nodes" in data
    # Depending on API key validity, active_nodes could be > 0 or 0
    print(f"--- POST /orchestrate response: {data} ---")
    print("--- POST /orchestrate: OK ---")


def main():
    if not wait_for_server():
        exit(1)

    try:
        test_audit_endpoint()
        test_orchestrate_endpoint()
        print("\n✅ All smoke tests passed.")
    except AssertionError as e:
        print(f"\n❌ Smoke test failed: {e}")
        exit(1)
    except Exception as e:
        print(f"\n❌ An unexpected error occurred: {e}")
        exit(1)

if __name__ == "__main__":
    main()
