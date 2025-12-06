from fastapi import APIRouter, HTTPException
from .models import TaskPolicy, StepResult, AgentState
from .parer import CriticAgent, DiagnosisModule, HealerAgent, RePlanningModule, ASPLEngine
from .agents.julius_agent import JuliusAgent
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = APIRouter()

# Initialize PARER components
critic_agent = CriticAgent()
diagnosis_module = DiagnosisModule()
healer_agent = HealerAgent()
re_planning_module = RePlanningModule()
aspl_engine = ASPLEngine()
julius_agent = JuliusAgent()  # Primary actor agent

# In-memory store for agent states, keyed by task_id
agent_states: dict[str, AgentState] = {}

@router.post("/execute_step", response_model=StepResult)
async def execute_step(task_policy: TaskPolicy):
    """
    Executes a single step of a task, incorporating the PARER framework for error recovery.
    """
    task_id = task_policy.task_id

    # 1. Initialize or retrieve AgentState
    if task_id not in agent_states:
        initial_plan = [step['step_name'] for step in task_policy.steps]
        agent_states[task_id] = AgentState(initial_plan=initial_plan)

    state = agent_states[task_id]

    # Checkpoint the state before execution
    last_stable_state = state.checkpoint()

    try:
        # 2. Execute the primary task (Actor)
        # The primary actor (e.g., JuliusAgent) executes its step.
        # This is where a hard exception might occur.
        logger.info(f"Executing task {task_id} with agent {task_policy.agent_type}")
        actor_result = await julius_agent.execute_task(task_policy.dict())
        state.current_output = actor_result.get("result_data", "")
        state.execution_trace.append({"action": "execute_julius_agent", "output": state.current_output})

    except Exception as e:
        logger.error(f"Hard exception caught during task execution: {e}")
        state.error_context = e
        actor_result = {}

    # 3. Pillar I: Detection (Critic)
    critic_decision = critic_agent.route(state)

    # 4. State Graph Orchestration
    if critic_decision == "SUCCESS":
        logger.info("Critic reports success. Finalizing step.")
        aspl_engine.process_recovery_outcome(state, "SUCCESS")
        return StepResult(
            task_id=task_id,
            status="SUCCESS",
            result_data=state.current_output,
            agent_name=actor_result.get("agent_name", task_policy.agent_type)
        )

    elif critic_decision == "DIAGNOSE":
        # 5. Pillar II: Diagnosis
        diagnosis_result = diagnosis_module.diagnose_and_classify(state)

        # 6. Pillar III: Recovery (Heal or Re-plan)
        if diagnosis_result == "HEAL":
            recovery_outcome = healer_agent.apply_patch(state, last_stable_state)
        elif diagnosis_result == "RE_PLAN":
            recovery_outcome = re_planning_module.re_plan(state)
        else:
            recovery_outcome = "FALLBACK_HUMAN" # Default fallback

        # 7. Process Recovery Outcome
        # NOTE: The blueprint describes this as an async process, but it's called synchronously here for simplicity.
        aspl_engine.process_recovery_outcome(state, recovery_outcome)

        if recovery_outcome == "RESUME":
            logger.info("Recovery successful. Resuming execution.")
            # For this example, we return a "RECOVERED" status.
            # A more complex orchestrator might re-run the step.
            return StepResult(
                task_id=task_id,
                status="RECOVERED",
                result_data="The step was successfully recovered after a failure.",
                agent_name="Orchestrator"
            )
        else: # FALLBACK_HUMAN
            logger.warning("Recovery failed. Rolling back to last stable state.")
            agent_states[task_id] = last_stable_state # Rollback
            raise HTTPException(
                status_code=500,
                detail="The agent failed to recover from an error and has been rolled back."
            )

    return StepResult(
        task_id=task_id,
        status="ERROR",
        result_data="An unknown error occurred in the orchestrator.",
        agent_name="Orchestrator"
    )
