import random
import string
import re

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


@app.route('/<url_path>')
def url_shortener(url_path):
    new_url = database.get_url(url_path)
    return flask.redirect(new_url[0], code=301) # Temp redirect


@app.route('/api/create_url', methods=["POST"])
def _api_url_creator():
    new_url = request.form.get("shortened-link")
    old_url = request.form.get("original-link")

    if new_url is None or old_url is None:
        return "Form data missing", 400

    forbidden_url_paths = ["api", "analytics", "admin", "main"]
    if new_url in forbidden_url_paths:
        return "Reserved URL paths", 400

    if not re.compile(r'^[a-zA-Z0-9]+$').match(new_url):
        return "Invalid URL", 400

    analytics_url = "".join(
        # Generate a 10 character string of numbers + letters
        random.choice(string.ascii_letters + string.digits) for _ in range(10)
    )
    return "test create a url here"


@app.route('/analytics/<analytics_path>')
def analytics(analytics_path):
    return "analytics test"


app.run(host='0.0.0.0', port=8080, debug=True)
