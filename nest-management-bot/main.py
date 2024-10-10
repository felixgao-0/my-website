import os
import logging

from slack_bolt import App

from dotenv import load_dotenv

load_dotenv()
logging.basicConfig(level=logging.DEBUG)

# Initialize your app with your bot token and signing secret
app = App(
    token=os.environ["SLACK_BOT_TOKEN"],
    signing_secret=os.environ["SLACK_SIGNING_SECRET"]
)

if __name__ == "__main__":
    app.start(port=int(os.environ.get("PORT", 3000)))
