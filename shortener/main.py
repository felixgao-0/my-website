import atexit
import random
import string
import re

import validators
from flask import Flask, request
import flask

import database

app = Flask(
    'app', 
    template_folder="template/",
    static_folder='static/'
)

db = database.Database()


@app.route('/')
def landing_page():
    return flask.render_template("index.html")


@app.route('/analytics/<analytics_path>')
def analytics(analytics_path):
    #result = db.get_analytics(url_path)
    return "analytics test"


@app.route('/test')
def test_page_lol():
    return str(db.check_url_exists("analytics_url", "pnYnM5YXp6"))


@app.route('/u/<url_path>')
def url_shortener(url_path):
    result = db.get_url(url_path)
    if not result:
        return "Not found", 404
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


@app.route('/api/create_url', methods=["POST"])
def _api_url_creator():
    new_url = request.form.get("shortened-link-field")
    old_url = request.form.get("original-link-field")

    # Checks go burr
    if new_url is None or old_url is None:
        return "Form data missing", 400

    forbidden_url_paths = ["api", "analytics", "admin", "login", "dashboard", "settings", "manage"]
    if new_url.lower() in forbidden_url_paths:
        return "Reserved URL path", 400

    if not re.compile(r'^[a-zA-Z0-9]+$').match(new_url):
        return "Shortened URL can only contain alphanumeric characters", 400

    if len(new_url) > 15:
        return "Shortened URL is too long", 413 # HTTP 413 = too large

    if isinstance(validators.url(old_url), validators.utils.ValidationError):
        return "Invalid URL to shorten", 400

    if db.check_url_exists("shortened_url", new_url):
        return "URL already exists", 409 # HTTP 409 = conflict

    analytics_url = "".join(
        # Generate a 10 character string of alphanumeric characters
        random.choice(string.ascii_letters + string.digits) for _ in range(10)
    )
    db.add_url(old_url, new_url, analytics_url) # Add DB entry
    return flask.render_template(
        "url_created.html",
        shortened_url=new_url,
        analytics_url=analytics_url
    ), 201


# Close the database on code end
atexit.register(lambda: db.close())

app.run(host='0.0.0.0', port=8080, debug=True)
