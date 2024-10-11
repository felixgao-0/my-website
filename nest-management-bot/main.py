import os
import logging

from slack_bolt import App

from dotenv import load_dotenv

# Local environment BUGFIX: I can't figure out why but ig im missing some cert files lol
# might be unneeded for others
# TODO: REMOVE IN PROD, prob
import certifi

import database
import views.home as home

os.environ['SSL_CERT_FILE'] = certifi.where()

load_dotenv()
logging.basicConfig(level=logging.INFO)

# Initialize your app with your bot token and signing secret
app = App(
    token=os.environ["SLACK_MANAGEMENT_BOT_TOKEN"],
    signing_secret=os.environ["SLACK_MANAGEMENT_SIGNING_SECRET"]
)

me = os.environ['MY_SLACK_ID']

@app.event("app_home_opened")
def update_home_tab(client, event):
    if event['user'] != me:
        home.generate_unauthorized(client, event)

    #if event['user']
    #home.generate_unauthorized(client, event)


if __name__ == "__main__":
    app.start(port=8000)
