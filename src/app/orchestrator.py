# --- IMPORTS ---
from fastapi import APIRouter
from .models import TaskPolicy, StepResult
from .agents.openai_critic import OpenAICriticAgent
from .agents.julius_agent import JuliusAgent



router = APIRouter()

# Initialize Agents
openai_agent = OpenAICriticAgent()
julius_agent = JuliusAgent()

# Agent mapping
agents = {
    "critic": openai_agent,
    "julius": julius_agent,
}

@router.post("/execute_step", response_model=StepResult)
async def execute_step(task_policy: TaskPolicy):
    """
    Executes a task step by routing it to the appropriate agent.
    """
    agent_type = task_policy.agent_type.lower()
    agent = agents.get(agent_type)

    if agent:
        result = await agent.execute_task(task_policy.dict())
        return StepResult(**result)
    else:
        # Handle unknown agent types
        return StepResult(
            task_id=task_policy.task_id,
            status="ERROR",
            result_data=f"Unknown agent type: {agent_type}",
            agent_name="Orchestrator"
        )
