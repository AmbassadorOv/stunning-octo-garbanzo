# Mock Julius API
class Julius:
    def __init__(self, api_key: str):
        pass

    class files:
        @staticmethod
        async def upload(file_paths: list):
            return [{"name": "mock_file.csv"}]

        @staticmethod
        async def delete(file_name: str):
            pass

    class chat:
        class completions:
            @staticmethod
            async def create(model: str, messages: list, file_paths: list, advanced_reasoning: bool):
                class Choice:
                    class Message:
                        content = "This is a mock response from the Julius agent."
                    message = Message()
                return type("Response", (), {"choices": [Choice()]})()
