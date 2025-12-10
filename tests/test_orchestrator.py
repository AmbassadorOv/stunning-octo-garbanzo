import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch
import os
import sys

# Add the project root to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.main import app

@pytest.fixture
def client():
    """Fixture to provide a test client for the FastAPI app."""
    return TestClient(app)

@patch('src.app.orchestrator.julius_agent.execute_task')
def test_route_to_julius_agent(mock_julius_execute, client):
    """Test routing to the JuliusAgent."""
    # Arrange
    expected_result = {
        "task_id": "123",
        "status": "COMPLETED",
        "result_data": "Julius executed",
        "agent_name": "Julius"
    }
    mock_julius_execute.return_value = expected_result

    task_payload = {
        "task_id": "123",
        "agent_type": "Julius",
        "prompt": "test prompt",
        "context": {},
        "file_paths": [],
        "steps": []
    }

    # Act
    response = client.post("/execute_step", json=task_payload)

    # Assert
    assert response.status_code == 200
    response_json = response.json()
    assert response_json["agent_name"] == "Julius"
    assert response_json["result_data"] == "Julius executed"
    mock_julius_execute.assert_called_once()

@patch('src.app.orchestrator.openai_agent.execute_task')
def test_route_to_critic_agent(mock_critic_execute, client):
    """Test routing to the OpenAICriticAgent."""
    # Arrange
    expected_result = {
        "task_id": "456",
        "status": "COMPLETED",
        "result_data": "Critic executed",
        "agent_name": "OpenAICritic"
    }
    mock_critic_execute.return_value = expected_result

    task_payload = {
        "task_id": "456",
        "agent_type": "Critic",
        "prompt": "test prompt",
        "context": {},
        "file_paths": [],
        "steps": []
    }

    # Act
    response = client.post("/execute_step", json=task_payload)

    # Assert
    assert response.status_code == 200
    response_json = response.json()
    assert response_json["agent_name"] == "OpenAICritic"
    assert response_json["result_data"] == "Critic executed"
    mock_critic_execute.assert_called_once()

def test_route_to_unknown_agent(client):
    """Test routing for an unknown agent type."""
    # Arrange
    task_payload = {
        "task_id": "789",
        "agent_type": "Unknown",
        "prompt": "test prompt",
        "context": {},
        "file_paths": [],
        "steps": []
    }

    # Act
    response = client.post("/execute_step", json=task_payload)

    # Assert
    assert response.status_code == 200
    response_json = response.json()
    assert response_json["status"] == "ERROR"
    assert "Unknown agent type: unknown" in response_json["result_data"]
