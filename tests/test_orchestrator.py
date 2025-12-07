
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import pytest
from unittest.mock import AsyncMock, patch
from fastapi.testclient import TestClient
from src.main import app
from src.app.models import TaskPolicy, StepResult

client = TestClient(app)

@pytest.fixture
def task_policy_factory():
    def _factory(agent_type: str):
        return {
            "task_id": "test-task",
            "agent_type": agent_type,
            "prompt": "Test prompt",
            "context": {},
            "file_paths": [],
            "steps": []
        }
    return _factory

@patch('src.app.orchestrator.julius_agent.execute_task', new_callable=AsyncMock)
def test_execute_step_julius_agent(mock_execute_task, task_policy_factory):
    mock_execute_task.return_value = {
        "task_id": "test-task",
        "status": "SUCCESS",
        "result_data": "Julius agent success",
        "agent_name": "Julius"
    }

    task_policy = task_policy_factory("julius")
    response = client.post("/execute_step", json=task_policy)

    assert response.status_code == 200
    response_data = response.json()
    assert response_data["status"] == "SUCCESS"
    assert response_data["agent_name"] == "Julius"
    mock_execute_task.assert_called_once_with(task_policy)

@patch('src.app.orchestrator.openai_agent.execute_task', new_callable=AsyncMock)
def test_execute_step_critic_agent(mock_execute_task, task_policy_factory):
    mock_execute_task.return_value = {
        "task_id": "test-task",
        "status": "SUCCESS",
        "result_data": "Critic agent success",
        "agent_name": "OpenAICritic"
    }

    task_policy = task_policy_factory("critic")
    response = client.post("/execute_step", json=task_policy)

    assert response.status_code == 200
    response_data = response.json()
    assert response_data["status"] == "SUCCESS"
    assert response_data["agent_name"] == "OpenAICritic"
    mock_execute_task.assert_called_once_with(task_policy)

def test_execute_step_unknown_agent(task_policy_factory):
    task_policy = task_policy_factory("unknown_agent")
    response = client.post("/execute_step", json=task_policy)

    assert response.status_code == 200
    response_data = response.json()
    assert response_data["status"] == "ERROR"
    assert "Unknown agent type" in response_data["result_data"]
    assert response_data["agent_name"] == "Orchestrator"
