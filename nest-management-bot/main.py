import atexit
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

import server_utils as utils

os.environ['SSL_CERT_FILE'] = certifi.where()

load_dotenv()
logging.basicConfig(level=logging.INFO)

# Initialize bot with token and signing secret
app = App(
    token=os.environ["SLACK_MANAGEMENT_BOT_TOKEN"],
    signing_secret=os.environ["SLACK_MANAGEMENT_SIGNING_SECRET"]
)

# Open database for account management
db = database.Database({
    "dbname": "felixgao_nest_management",
    "user": "felixgao",
    "password": os.environ['DB_PASSWORD'],
    "host": "hackclub.app",
    "port": "5432"
    })

me = os.environ['MY_SLACK_ID']


@app.event("app_home_opened")
def update_home_tab(client, event):
    user_id = event['user']
    if user_id != me: 
        # Testing check, blocks others from using D:
        home.generate_unauthorized(client, event)

    if not db.get_user(slack_id=user_id): 
        #User not registered, signup!
        home.generate_setup(client, event)


# TODO: Action btn to generate code
def setup_user(client):
    user_token = utils.generate_token()
    #db.add_user("U07BU2HS17Z", user_token)


# Close the database on code end
atexit.register(lambda: db.close())

if __name__ == "__main__":
    app.start(port=8000)
