from emma import Emma
from ollama import OllamaClient
from dotenv import dotenv_values
from slack_bolt.adapter.socket_mode import SocketModeHandler

config = dotenv_values(".env")

user_memories = {}
ai_client = OllamaClient()
emma_bot = Emma(
    token=config["SLACK_BOT_TOKEN"], user_memories=user_memories, ai_client=ai_client
)


if __name__ == "__main__":
    SocketModeHandler(app=emma_bot, app_token=config["SOCKET_MODEL_TOKEN"]).start()
