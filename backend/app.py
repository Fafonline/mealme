from flask import Flask
from flask_cors import CORS

app = Flask(__name__)


def add_cors_headers(response):
    # Replace "http://localhost:80" with the actual URL of your Angular application
    # response.headers['Access-Control-Allow-Origin'] = 'http://localhost'
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Headers'] = '*'
    response.headers['Access-Control-Allow-Methods'] = 'GET, POST, PUT, DELETE, OPTIONS'
    return response


@app.after_request
def after_request(response):
    response = add_cors_headers(response)
    return response


@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"

# Route function to get all meals


@app.route("/meals", methods=["GET"])
def get_meals():
    return "[{\"name\":\"Tartiflette\"},{\"name\":\"Couscous\"}]"
