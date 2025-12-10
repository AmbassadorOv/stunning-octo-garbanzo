# --- IMPORTS ---
from fastapi import APIRouter
from .models import TaskPolicy, StepResult
from .agents.openai_critic import OpenAICriticAgent
from .agents.julius_agent import JuliusAgent



router = APIRouter()

# Initialize Agents
openai_agent = OpenAICriticAgent()
julius_agent = JuliusAgent()

# Placeholder for your AgentType Enum
class AgentType:
    CRITIC = "critic"
    JULIUS = "julius"

@router.post("/execute_step", response_model=StepResult)
async def execute_step(task_policy: TaskPolicy):
    # Determine which agent to use based on the task policy
    agent_type = task_policy.agent_type.lower()

    if agent_type == AgentType.JULIUS:
        # Route to the new Julius Agent for data-specific tasks
        result = await julius_agent.execute_task(task_policy.model_dump())
        return StepResult(**result)

    elif agent_type == AgentType.CRITIC:
        # Route to the existing OpenAI Critic
        result = await openai_agent.execute_task(task_policy.model_dump())
        return StepResult(**result)

    else:
        # Handle unknown agent types
        return StepResult(
            task_id=task_policy.task_id,
            status="ERROR",
            result_data=f"Unknown agent type: {agent_type}",
            agent_name="Orchestrator"
        )
