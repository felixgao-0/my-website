import os
import logging

from slack_bolt import App

from dotenv import load_dotenv

# Local environment BUGFIX: I can't figure out why but ig im missing some cert files lol
# might be unneeded for others
# TODO: REMOVE IN PROD
import certifi
os.environ['SSL_CERT_FILE'] = certifi.where()

load_dotenv()
logging.basicConfig(level=logging.INFO)

# Initialize your app with your bot token and signing secret
app = App(
    token=os.environ["SLACK_MANAGEMENT_BOT_TOKEN"],
    signing_secret=os.environ["SLACK_MANAGEMENT_SIGNING_SECRET"]
)

if __name__ == "__main__":
    app.start(port=int(os.environ.get("PORT", 8000)))
