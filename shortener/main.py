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
        return flask.abort(400) # HTTP 400 = no data D:

    forbidden_url_paths = ["api", "analytics", "analytic", "admin", "login", "dashboard", "settings", "manage"]
    if new_url.lower() in forbidden_url_paths:
        flask.flash("That shortened URL path is reserved!", "shortened-link-error")
        error_state = True

    if not re.compile(r'^[a-zA-Z0-9-_]+$').match(new_url):
        flask.flash("Whoops! The URL can only contain alphanumeric characters, dashes, and underscores.", "shortened-link-error")
        error_state = True

    if len(new_url) > 15:
        flask.flash("Woah wheres the end? The shortened URL path is too long.", "shortened-link-error")
        error_state = True

    if db.check_url_exists("shortened_url", new_url):
        flask.flash("Sorry, that shortened URL has already been taken! Our database hates twins.", "shortened-link-error")
        error_state = True

    if isinstance(validators.url(old_url), validators.utils.ValidationError):
        flask.flash("That's an invalid URL. Does it start with https://?", "original-link-error")
        error_state = True

    if error_state:
        return flask.redirect(flask.url_for('landing_page'))

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
