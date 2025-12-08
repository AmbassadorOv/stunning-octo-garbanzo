import os
import json
from ..julius_api import Julius

# Pydantic models (assumed to be defined elsewhere, e.g., TaskPolicy, StepResult)
# from ..models import TaskPolicy, StepResult

class JuliusAgent:
    """
    A dedicated agent for executing data analysis tasks using Julius AI.
    Julius specializes in analysis, visualization, and reporting.
    """
    def __init__(self):
        # Initialize Julius client using the environment variable
        julius_api_token = os.getenv('JULIUS_API_TOKEN')
        if not julius_api_token:
            raise ValueError("JULIUS_API_TOKEN environment variable not set.")

        # Initialize the client (assuming standard API key method)
        self.client = Julius(api_key=julius_api_token)

    async def execute_task(self, task_policy: dict) -> dict:
        """
        Executes a data analysis task by interacting with the Julius AI API.

        :param task_policy: The TaskPolicy dict containing instructions and context.
        :return: A StepResult dict containing the Julius AI output.
        """
        # --- 1. Extract necessary task parameters ---
        task_id = task_policy.get('task_id', 'unknown')
        prompt = task_policy.get('prompt', 'Analyze the provided data.')
        file_paths = task_policy.get('file_paths', [])

        print(f"Julius Agent received Task {task_id}. Prompt: {prompt[:40]}...")

        # --- 2. Handle File Uploads (Crucial for Julius AI) ---
        uploaded_files = []
        if file_paths:
            print(f"Uploading {len(file_paths)} files to Julius...")
            try:
                # The Julius API client supports file upload
                uploaded_files = await self.client.files.upload(file_paths)
                print(f"Uploaded files: {uploaded_files}")
            except Exception as e:
                return {
                    "task_id": task_id,
                    "status": "FAILURE",
                    "result_data": {"error": f"Julius File Upload Error: {e}"},
                    "agent_name": "Julius"
                }

        # --- 3. Run Chat Completion (The analysis step) ---
        try:
            # Create a chat completion with the analysis prompt
            response = await self.client.chat.completions.create(
                model="default",
                messages=[
                    {"role": "user", "content": prompt}
                ],
                file_paths=uploaded_files, # Link the uploaded files to the chat
                advanced_reasoning=True
            )

            # --- 4. Format Result ---
            result_content = response.choices[0].message.content

            # Assuming Julius generates code, visualizations, and reports
            # You might need to add logic here to download generated visualizations.

            return {
                "task_id": task_id,
                "status": "SUCCESS",
                "result_data": {"result": result_content},
                "agent_name": "Julius"
            }

        except Exception as e:
            return {
                "task_id": task_id,
                "status": "FAILURE",
                "result_data": {"error": f"Julius Execution Error: {e}"},
                "agent_name": "Julius"
            }
        finally:
            # --- 5. Clean up uploaded files (optional but recommended) ---
            for file in uploaded_files:
                await self.client.files.delete(file['name'])
