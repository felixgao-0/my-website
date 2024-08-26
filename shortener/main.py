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
    return "hi"


@app.route('/api/create_url', methods=["POST"])
def url_creator(url_path):
    return flask.render_template("index.html")


app.run(host='0.0.0.0', port=8080)
