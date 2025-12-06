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


from typing import Dict, Any, List, Optional
import time
import copy

class AgentState:
    """
    Represents the operational state of the LLM agent.
    This state is checkpointed to facilitate rollbacks (Pillar III).
    """
    def __init__(self, initial_plan: List[str]):
        self.plan = initial_plan  # Remaining steps in the task
        self.execution_trace: List[Dict[str, Any]] = [] # Structured log of actions and tool calls [3, 4]
        self.current_output: str = ""
        self.variable_state: Dict[str, Any] = {} # Critical variables (e.g., API keys, file handles)
        self.error_context: Optional[Exception] = None # Hard Python exception (if detected)
        self.rca_report: Optional[str] = None      # Root Cause Analysis output (Pillar II)

    def checkpoint(self) -> 'AgentState':
        """Saves the current state to allow for controlled rollback."""
        return copy.deepcopy(self)
