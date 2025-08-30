# Import required libraries for Slack bot functionality
import os
import requests
import json
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler
from dotenv import dotenv_values

class Emma(App):
    """
    Emma - A Slack bot that integrates with Ollama for AI responses.
    Inherits from slack_bolt.App to handle Slack events and interactions.
    """

    def __init__(self, token):
        """
        Initialize the Emma bot with the provided Slack bot token.
        
        Args:
            token (str): Slack bot token for authentication
        """
        super().__init__(token=token)
        self.init_events()  # Set up event handlers
        self.init_message()  # Set up message handlers

    def init_events(self):
        """Initialize event handlers for Slack events like app mentions."""
        
        @self.event("app_mention")
        def handle_app_mentions(body, say):
            """
            Handle when someone @mentions the bot in a channel.
            
            Args:
                body (dict): Event data from Slack containing message details
                say (function): Function to send a response back to the channel
            """
            text = body["event"]["text"]  # Extract the message text
            user_id = body["event"]["user"]  # Gets the user ID like "U1234567890"
            
            # Get AI response from Ollama API
            ai_response = self.ask_ollama(text)
            
            # Send the AI response along with the user ID back to the channel
            say(f"{ai_response}\nUser ID: {user_id}")
            # Alternative format (commented out):
            # say(ai_response, f"User ID: {user_id}")

    def init_message(self):
        """Initialize message handlers for specific message patterns."""
        
        @self.message("hello")
        def message_hello(message, say):
            """
            Respond to messages containing "hello".
            
            Args:
                message (dict): Message data from Slack
                say (function): Function to send a response back to the channel
            """
            say(f"Hey there <@{message['user']}>!")

    def ask_ollama(self, message):
        """
        Send a message to the Ollama API and get an AI response.
        
        Args:
            message (str): The user's message to send to Ollama
            
        Returns:
            str: The AI-generated response from Ollama
        """
        # Make POST request to Ollama API
        response = requests.post('http://localhost:11434/api/chat', 
            json={
                "model": "emma-assistant:latest",  # Specify the Ollama model to use
                "messages": [{"role": "user", "content": message}],  # Format message for chat API
                "stream": False  # Disable streaming for simpler response handling
            })
        
        # Extract and return the AI response content
        return response.json()['message']['content']


if __name__ == "__main__":
    """
    Main execution block - starts the Slack bot when the script is run directly.
    """
    # Load configuration from .env file
    config = dotenv_values(".env")
    
    # Create and start the bot using Socket Mode for real-time communication
    # Socket Mode allows the bot to receive events without exposing a public HTTP endpoint
    SocketModeHandler(
        app=Emma(token=config["SLACK_BOT_TOKEN"]),  # Initialize Emma bot with bot token
        app_token=config["SOCKET_MODEL_TOKEN"]      # Use socket mode token for connection
    ).start()