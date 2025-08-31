from emma import Emma
from dotenv import dotenv_values
from slack_bolt.adapter.socket_mode import SocketModeHandler

config = dotenv_values(".env")
emma_bot = Emma(token=config["SLACK_BOT_TOKEN"])

if __name__ == "__main__":
    SocketModeHandler(app=emma_bot, app_token=config["SOCKET_MODEL_TOKEN"]).start()