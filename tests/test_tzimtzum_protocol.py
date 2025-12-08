import pytest
from src.app.tzimtzum_protocol import initiate_admiral_julius_command
from src.app.agents.tzimtzum_agent import TzimtzumAgent

def test_initiate_admiral_julius_command_success():
    """
    Tests that the initiate_admiral_julius_command function returns a SUCCESS status
    when the U_METRIC is above the ADAPTATION THRESHOLD.
    """
    command_order = {"test": "test"}
    result = initiate_admiral_julius_command(command_order)
    assert result["status"] == "SUCCESS"
    assert result["execution_path"] == "Extrapolate Nonlinear Discovery (Ring 5)"

@pytest.mark.asyncio
async def test_tzimtzum_agent_success():
    """
    Tests that the TzimtzumAgent returns a SUCCESS status when a valid
    command order is provided.
    """
    agent = TzimtzumAgent()
    task_policy = {
        "task_id": "test",
        "prompt": {"test": "test"}
    }
    result = await agent.execute_task(task_policy)
    assert result["status"] == "SUCCESS"
    assert result["agent_name"] == "TzimtzumAgent"

@pytest.mark.asyncio
async def test_tzimtzum_agent_no_command_order():
    """
    Tests that the TzimtzumAgent returns a FAILURE status when no command
    order is provided.
    """
    agent = TzimtzumAgent()
    task_policy = {
        "task_id": "test",
        "prompt": None
    }
    result = await agent.execute_task(task_policy)
    assert result["status"] == "FAILURE"
    assert result["agent_name"] == "TzimtzumAgent"
    assert result["result_data"] == "No command order found in the prompt."
