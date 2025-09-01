import requests


class OllamaClient:
    def __init__(self, base_url="http://localhost:11434"):
        self.base_url = base_url

    def chat(self, user_memory):
        try:
            response = requests.post(
                f"{self.base_url}/api/chat",
                json={
                    "model": "emma-assistant:latest",
                    "messages": [*user_memory],
                    "stream": False,
                },
                timeout=60,
            )
            response.raise_for_status()
            return response.json()["message"]["content"]
        except Exception as e:
            return f"Sorry, I'm having trouble processing that request.\n{str(e)}"
