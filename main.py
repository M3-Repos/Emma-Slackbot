from emma import Emma
from dotenv import dotenv_values
from slack_bolt.adapter.socket_mode import SocketModeHandler

if __name__ == "__main__":
    config = dotenv_values(".env")
    SocketModeHandler(app=Emma(token=config["SLACK_BOT_TOKEN"]), app_token=config["SOCKET_MODEL_TOKEN"]).start()