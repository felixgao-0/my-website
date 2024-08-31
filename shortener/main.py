import atexit
import os
import random
import string
import re
from calendar import error

import validators
from flask import Flask, request
import flask

import database

app = Flask(
    'app', 
    template_folder="template/",
    static_folder='static/'
)

app.secret_key = os.environ['FLASK_SECRET_KEY']

db = database.Database()


@app.route('/')
def landing_page():
    return flask.render_template("index.html")


@app.route('/test')
def test_page_lol():
    return str(db.get_analytics("test5"))


@app.route('/analytics/<analytics_path>')
def analytics(analytics_path):
    result = db.get_analytics(analytics_path)
    if not result:
        return flask.abort(404)
    else:
        return flask.render_template("analytics.html", analytics=result)


@app.route('/u/<url_path>')
def url_shortener(url_path):
    result = db.get_url(url_path)
    if not result:
        return flask.abort(404)
    new_url = result[0][1]

    db.add_analytics(
        int(result[0][0]),
        request.referrer,
        request.headers.get('User-Agent')
    )

    # Note to self: HTTP 302 = temp redirect, don't use HTTP 301 it breaks everything D:
    if new_url.startswith("https://") or new_url.startswith("http://"):
        return flask.redirect(new_url, code=302) # Temp redirect
    else:
        return flask.redirect("https://" + new_url, code=302) # Temp redirect


@app.route('/create_url', methods=["POST"])
def _api_url_creator():
    error_state = False
    new_url = request.form.get("shortened-link-field")
    old_url = request.form.get("original-link-field")

    # Checks go burr
    if new_url is None or old_url is None:
        return {
            "status": "Ahh, mission control we're missing data somehow. Make a github issue abt this and Felix will fix this (maybe).",
            "type": "shortened-link-error"
        }, 400

    forbidden_url_paths = ["api", "analytics", "analytic", "admin", "login", "dashboard", "settings", "manage"]
    if new_url.lower() in forbidden_url_paths:
        return {
            "status": "Woah area 51 documents! That shortened URL path is reserved!",
            "type": "shortened-link-error"
        }, 400

    elif not re.compile(r'^[a-zA-Z0-9-_]+$').match(new_url):
        return {
            "status": "Whoops! The URL can only contain alphanumeric characters, dashes, and underscores.",
            "type": "shortened-link-error"
        }, 400

    elif len(new_url) > 15:
        return {
            "status": "Woah wheres the end? The shortened URL path is too long.",
            "type": "shortened-link-error"
        }, 400

    elif db.check_url_exists("shortened_url", new_url):
        return {
            "status": "Sorry, that shortened URL has already been taken! Our database hates twins.",
            "type": "shortened-link-error"
        }, 400

    if not (old_url.startswith("https://") or old_url.startswith("http://")):
        return {
            "status": "The shortened URL should start with http:// or https://, or else our db explodes /hj.",
            "type": "shortened-link-error"
        }, 400


    elif isinstance(validators.url(old_url), validators.utils.ValidationError):
        return {
            "status": "That's an invalid URL. Pls check again",
            "type": "original-link-error"
        }, 400

    while True:
        analytics_url = "".join(
            # Generate a 10 character string of alphanumeric characters
            random.choice(string.ascii_letters + string.digits) for _ in range(10)
        )
        if not db.check_url_exists("analytics_url", analytics_url):
            break

    db.add_url(old_url, new_url, analytics_url) # Add DB entry
    return flask.render_template(
        "url_created.html",
        shortened_url=f"https://url.felixgao.dev/u/{new_url}",
        analytics_url=f"https://url.felixgao.dev/analytics/{analytics_url}"
    ), 201


# Close the database on code end
atexit.register(lambda: db.close())

app.run(host='0.0.0.0', port=8080, debug=True)
