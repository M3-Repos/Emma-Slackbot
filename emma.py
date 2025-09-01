import re
import logging
from slack_bolt import App
from collections import deque

logger = logging.getLogger(__name__)

class Emma(App):
    def __init__(self, token, user_memories, ai_client):
        super().__init__(token=token)
        self.user_memories = user_memories
        self.ai_client = ai_client
        self.init_events()
        self.init_message()
        logger.info("Emma Application initialized")

    def init_events(self):
        @self.event("app_mention")
        def handle_app_mentions(body, say):
            """When someone @mentions the bot"""
            raw_text = body["event"]["text"]
            text = re.sub(r"<@\w+>", "", raw_text).strip()
            user_id = body["event"]["user"]
            logger.info(f"Received mention from user {user_id}: {text}")

            user_memory = self.user_memories.setdefault(user_id, deque(maxlen=10))
            user_memory.append({"role": "user", "content": text})
            ai_response = self.ask_ollama(user_memory)
            user_memory.append({"role": "assistant", "content": ai_response})

            logger.info(f"Responding to user {user_id}")
            say(f"{ai_response}")

    def init_message(self):
        @self.message("hello")
        def message_hello(message, say):
            user_id = message["user"]
            logger.info(f"Hello message from user {user_id}")
            say(f"Hey there <@{user_id}>!")

    def ask_ollama(self, user_memory):
        return self.ai_client.chat(user_memory)
