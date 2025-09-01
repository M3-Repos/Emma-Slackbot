import os
import requests
import json
from slack_bolt import App

class Emma(App):

    user_memories = {}

    def __init__(self,token):
        super().__init__(token=token)
        self.init_events()
        self.init_message()

    def init_events(self):
        @self.event("app_mention")
        def handle_app_mentions(body, say):
            """When someone @mentions the bot"""
            text = body["event"]["text"]
            user_id = body["event"]["user"]  # Gets the user ID like "U1234567890"
            user_memory = Emma.user_memories.setdefault(user_id,[])
            user_memory.append(text)
            ai_response = self.ask_ollama(*user_memory)
            user_memory.append(ai_response)
            #say(f"{ai_response}\nUser ID: {user_id}")
            say(f"{ai_response}")

    def init_message(self):
        @self.message("hello")
        def message_hello(message, say):
            say(f"Hey there <@{message['user']}>!")

    def ask_ollama(self,*message):
        """Send message to your Ollama API"""
        try:
            response = requests.post('http://localhost:11434/api/chat', 
                json={
                    "model": "emma-assistant:latest",
                    "messages": [{"role": "user", "content": "".join(message)}],
                    "stream": False
                },timeout=30)
            response.raise_for_status()
            return response.json()['message']['content']
        except Exception as e:
            return f"Sorry, I'm having trouble processing that request.\n{str(e)}"
