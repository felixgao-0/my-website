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


@app.route('/')
def landing_page():
    return flask.render_template("index.html")


@app.route('/u/<url_path>')
def url_shortener(url_path):
    result = database.get_url(url_path)
    if not result:
        return "Not found", 404
    new_url = result[0][1]

    # Note to self: HTTP 302 = temp redirect, don't use HTTP 301 it breaks everything D:
    if new_url.startswith("https://") or new_url.startswith("http://"):
        return flask.redirect(new_url, code=302) # Temp redirect
    else:
        return flask.redirect("https://" + new_url, code=302) # Temp redirect


@app.route('/api/create_url', methods=["POST"])
def _api_url_creator():
    new_url = request.form.get("shortened-link")
    old_url = request.form.get("original-link")

    # Checks go burr
    if new_url is None or old_url is None:
        return "Form data missing", 400

    forbidden_url_paths = ["api", "analytics", "admin", "main"]
    if new_url in forbidden_url_paths:
        return "Reserved URL paths", 400

    if not re.compile(r'^[a-zA-Z0-9]+$').match(new_url):
        return "Invalid URL to convert into", 400

    try: # Returns ValidationError when url is invalid
        validators.url.url(old_url)
    except validators.utils.ValidationError:
        return "Invalid URL", 400

    analytics_url = "".join(
        # Generate a 10 character string of numbers + letters
        random.choice(string.ascii_letters + string.digits) for _ in range(10)
    )
    database.add_url(old_url, new_url, analytics_url) # Add DB entry
    return "Url created", 201


@app.route('/analytics/<analytics_path>')
def analytics(analytics_path):
    #result = database.get_analytics(url_path)
    return "analytics test"


app.run(host='0.0.0.0', port=8080, debug=True)
