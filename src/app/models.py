from pydantic import BaseModel
from typing import List, Dict, Any
import datetime

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

# --- Huddle AI Bridge Models ---

class DataPacket(BaseModel):
    """
    Layer I (Ingress): Standardized data packet from Huddle sensors.
    """
    timestamp: datetime.datetime
    authentication: str
    sensor_data: Dict[str, Any]

class PureStateVector(BaseModel):
    """
    Layer II (Core): The processed state vector ready for egress.
    """
    psv_data: Dict[str, float]
    symbolic_trace: List[str]
    profile_provenance: str
