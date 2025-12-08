from fastapi.testclient import TestClient
from src.main import app

client = TestClient(app)

def test_pull():
    response = client.post("/remote/pull", json={"session_id": "12345"})
    assert response.status_code == 200
    assert response.json() == {"status": "success", "message": "Pulling results for session 12345"}

def test_list_repos():
    response = client.post("/remote/list", json={"list_repos": True})
    assert response.status_code == 200
    assert response.json() == {"status": "success", "repositories": ["torvalds/linux", "facebook/react"], "sessions": []}

def test_list_sessions():
    response = client.post("/remote/list", json={"list_sessions": True})
    assert response.status_code == 200
    assert response.json() == {"status": "success", "repositories": [], "sessions": ["session_12345", "session_abcde"]}

def test_new_session():
    response = client.post("/remote/new", json={"repo": "torvalds/linux", "session_description": "write unit tests"})
    assert response.status_code == 200
    assert response.json() == {"status": "success", "message": "New session created for repo torvalds/linux", "session_id": "new_session_xyz"}
