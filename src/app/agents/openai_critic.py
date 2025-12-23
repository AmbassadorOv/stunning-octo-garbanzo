class OpenAICriticAgent:
    async def execute_task(self, task_policy: dict) -> dict:
        return {
            "task_id": task_policy.get("task_id"),
            "status": "SUCCESS",
            "result_data": "This is a mock response from the OpenAI Critic agent.",
            "agent_name": "OpenAICritic",
        }
