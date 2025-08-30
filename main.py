import os
import requests
import json
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler
from dotenv import dotenv_values

config = dotenv_values(".env")

# Initialize the app with your bot token and socket mode handler
app = App(token=config["SLACK_BOT_TOKEN"])

def ask_ollama(message):
    """Send message to your Ollama API"""
    response = requests.post('http://localhost:11434/api/chat', 
        json={
            "model": "emma-assistant:latest",
            "messages": [{"role": "user", "content": message}],
            "stream": False
        })
    return response.json()['message']['content']

@app.message("hello")
def message_hello(message, say):
    say(f"Hey there <@{message['user']}>!")

@app.event("app_mention")
def handle_app_mentions(body, say):
    """When someone @mentions the bot"""
    text = body["event"]["text"]
    # Remove the bot mention from the text
    clean_text = text.split('>', 1)[1].strip() if '>' in text else text
    
    # Get response from Ollama
    ai_response = ask_ollama(clean_text)
    say(ai_response)

if __name__ == "__main__":
    SocketModeHandler(app, config["SOCKET_MODEL_TOKEN"]).start()