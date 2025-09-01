import logging
from contextlib import contextmanager
from emma import Emma
from ollama import OllamaClient
from dotenv import dotenv_values
from slack_bolt.adapter.socket_mode import SocketModeHandler

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@contextmanager
def emma_context():
    config = dotenv_values(".env")

    user_memories = {}
    ai_client = OllamaClient()
    emma_bot = Emma(
        token=config["SLACK_BOT_TOKEN"], user_memories=user_memories, ai_client=ai_client
    )

    try:
        logger.info("Starting Emma bot...")
        handler = SocketModeHandler(app=emma_bot, app_token=config["SOCKET_MODEL_TOKEN"])
        yield handler
    finally:
        logger.info("Stopping Emma bot...")

if __name__ == "__main__":
    try:
        with emma_context() as handler:
            handler.start()
    except KeyboardInterrupt:
        logger.info("Gracefully shutting down Emma bot...")
    except Exception as e:
        logger.error(f"An unexpected error occurred while running the Emma bot: {e}")
