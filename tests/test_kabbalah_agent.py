import pytest
from src.app.agents.kabbalah_agent import KabbalahAgent

@pytest.fixture
def kabbalah_agent():
    return KabbalahAgent()

def test_analyze_closure(kabbalah_agent):
    result = kabbalah_agent.analyze_closure()
    assert isinstance(result, dict)
    assert "letters_with_999_closure" in result
    assert "letters_with_1000_closure" in result
    assert result["letters_with_999_closure"] == ['Gimel', 'Vav', 'Tet']
    assert result["letters_with_1000_closure"] == ['Aleph', 'Heh', 'Het']

@pytest.mark.asyncio
async def test_execute_task_closure(kabbalah_agent):
    task_policy = {"task_id": "123", "prompt": "analyze closure"}
    result = await kabbalah_agent.execute_task(task_policy)
    assert result["status"] == "SUCCESS"
    assert "letters_with_999_closure" in result["result_data"]
    assert "letters_with_1000_closure" in result["result_data"]
    assert result["result_data"]["letters_with_999_closure"] == ['Gimel', 'Vav', 'Tet']
    assert result["result_data"]["letters_with_1000_closure"] == ['Aleph', 'Heh', 'Het']


@pytest.mark.asyncio
async def test_execute_task_unknown(kabbalah_agent):
    task_policy = {"task_id": "123", "prompt": "unknown analysis"}
    result = await kabbalah_agent.execute_task(task_policy)
    assert result["status"] == "SUCCESS"
    assert "error" in result["result_data"]
    assert "Unknown analysis type" in result["result_data"]["error"]
