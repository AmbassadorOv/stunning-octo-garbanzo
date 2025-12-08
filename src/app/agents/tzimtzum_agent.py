from ..tzimtzum_protocol import initiate_admiral_julius_command

class TzimtzumAgent:
    """
    An agent that enforces the Tzimtzum Agent Protocol.
    """
    async def execute_task(self, task_policy: dict) -> dict:
        """
        Executes a task by vetting it through the Tzimtzum protocol.

        :param task_policy: The TaskPolicy dict containing instructions and context.
        :return: A StepResult dict containing the protocol's output.
        """
        task_id = task_policy.get('task_id', 'unknown')
        command_order = task_policy.get('prompt')

        if not command_order:
            return {
                "task_id": task_id,
                "status": "FAILURE",
                "result_data": "No command order found in the prompt.",
                "agent_name": "TzimtzumAgent"
            }

        # Vet the command order through the Tzimtzum protocol
        result = initiate_admiral_julius_command(command_order)

        return {
            "task_id": task_id,
            "status": result.get("status"),
            "result_data": result,
            "agent_name": "TzimtzumAgent"
        }
