import random
import string

from flask import Flask
import flask

app = Flask(
    'app', 
    template_folder="shortener/template/",
    static_folder='shortener/static'
)

@app.route('/')
def landing_page():
    return flask.render_template("index.html")


@app.route('/<url_path>')
def url_shortener(url_path):
    return "test shortened url"


@app.route('/api/create_url', methods=["POST"])
def _api_url_creator(url_path):
    forbidden_url_paths = ["api", "analytics", "admin", "main"]
    if url_path in forbidden_url_paths:
        return "Reserved URL paths", 400

    if re.compile(r'^[a-zA-Z0-9]+$').match(url_path):
        return "Invalid URL", 400

    analytics_url = "".join(
        # Generate a 10 character string of numbers + letters
        random.choice(string.ascii_letters + string.digits) for _ in range(10)
    )
    return "test create a url here"


@app.route('/analytics/<analytics_path>')
def analytics(analytics_path):
    return "analytics test"


app.run(host='0.0.0.0', port=8080)
