import re
from slack_bolt import App
from collections import deque


class Emma(App):
    def __init__(self, token, user_memories, ai_client):
        super().__init__(token=token)
        self.user_memories = user_memories
        self.ai_client = ai_client
        self.init_events()
        self.init_message()

    def init_events(self):
        @self.event("app_mention")
        def handle_app_mentions(body, say):
            """When someone @mentions the bot"""
            raw_text = body["event"]["text"]
            text = re.sub(r"<@\w+>", "", raw_text).strip()
            user_id = body["event"]["user"]
            user_memory = self.user_memories.setdefault(user_id, deque(maxlen=10))
            user_memory.append({"role": "user", "content": text})
            ai_response = self.ask_ollama(user_memory)
            user_memory.append({"role": "assistant", "content": ai_response})
            say(f"{ai_response}")

    def init_message(self):
        @self.message("hello")
        def message_hello(message, say):
            say(f"Hey there <@{message['user']}>!")

    def ask_ollama(self, user_memory):
        return self.ai_client.chat(user_memory)
