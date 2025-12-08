import pytest
from src.app.agents.huddle_agent import HuddleAgent
from src.app.models import TaskPolicy
import json

@pytest.fixture
def huddle_agent():
    return HuddleAgent()

@pytest.mark.asyncio
async def test_execute_task_success(huddle_agent: HuddleAgent):
    # --- 1. Define a mock TaskPolicy ---
    mock_task_policy = {
        "task_id": "huddle-test-123",
        "agent_type": "huddle",
        "prompt": "Process Huddle sensor data.",
        "context": {
            "light": 75,
            "sound": 50,
            "presence": True,
            "activity": 5
        },
        "file_paths": [],
        "steps": []
    }

    # --- 2. Execute the task ---
    result = await huddle_agent.execute_task(mock_task_policy)

    # --- 3. Assertions ---
    assert result["status"] == "SUCCESS"
    assert result["agent_name"] == "HuddleAgent"
    assert "psv" in result["result_data"]

    # --- 4. Verify PSV data structure ---
    result_data = json.loads(result["result_data"])
    psv = result_data["psv"]

    assert "psv_data" in psv
    assert "symbolic_trace" in psv
    assert "profile_provenance" in psv

    assert psv["psv_data"]["light_level"] == 0.75
    assert psv["psv_data"]["sound_level"] == 0.50
    assert psv["psv_data"]["presence"] == 1.0
    assert psv["psv_data"]["activity"] == 0.5
