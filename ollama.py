import requests
import logging

logger = logging.getLogger(__name__)


class OllamaClient:
    def __init__(self, base_url="http://localhost:11434"):
        self.base_url = base_url
        logger.info("Ollama Client initialized")

    def chat(self, user_memory):
        try:
            logger.info("Issuing request to Ollama")
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
            logger.info("Ollama response successfull")
            return response.json()["message"]["content"]
        except requests.exceptions.RequestException as e:
            logger.error(f"Ollama response unsuccessful: {e}")
            return f"Sorry, I'm having trouble reaching the AI service right now.\n{str(e)}"
        except Exception as e:
            logger.error(f"Ollama response unsuccessful: {e}")
            return f"Sorry, I'm having some trouble processing that request.\n{str(e)}"
