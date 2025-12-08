from fastapi import APIRouter
from pydantic import BaseModel
from typing import Optional

router = APIRouter(prefix="/remote", tags=["remote"])

class PullRequest(BaseModel):
    session_id: str

class ListRequest(BaseModel):
    list_repos: Optional[bool] = False
    list_sessions: Optional[bool] = False

class NewRequest(BaseModel):
    repo: str
    session_description: str

@router.post("/pull")
async def pull_results(payload: PullRequest):
    return {"status": "success", "message": f"Pulling results for session {payload.session_id}"}

@router.post("/list")
async def list_items(payload: ListRequest):
    repos = []
    sessions = []
    if payload.list_repos:
        repos = ["torvalds/linux", "facebook/react"]
    if payload.list_sessions:
        sessions = ["session_12345", "session_abcde"]
    return {"status": "success", "repositories": repos, "sessions": sessions}

@router.post("/new")
async def new_session(payload: NewRequest):
    return {"status": "success", "message": f"New session created for repo {payload.repo}", "session_id": "new_session_xyz"}
