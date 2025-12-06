from pydantic import BaseModel
from typing import List, Dict, Any

class TaskPolicy(BaseModel):
    task_id: str
    agent_type: str
    prompt: str
    context: Dict[str, Any]
    file_paths: List[str]
    steps: List[Dict[str, Any]]

class StepResult(BaseModel):
    task_id: str
    status: str
    result_data: str
    agent_name: str
