from flask import Flask, render_template
from markupsafe import escape
import requests
import os
from string_manipulation import reverse_words


app = Flask("JokesAPI")


def create_joke_from_response(res):
    res_json = res.json()
    return {"id": res_json["id"], "value": res_json["value"]}


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/joke")
def joke_random():
    res = requests.get("https://api.chucknorris.io/jokes/random")
    return create_joke_from_response(res)


@app.route("/joke/reverse")
def joke_random_reverse():
    res = requests.get("https://api.chucknorris.io/jokes/random")
    joke = create_joke_from_response(res)
    joke["value"] = reverse_words(joke["value"])
    return joke


@app.route("/joke/<id>")
def joke_id(id):
    res = requests.get(f"https://api.chucknorris.io/jokes/{escape(id)}")
    return create_joke_from_response(res)


@app.route("/joke/<id>/reverse")
def joke_id_reverse(id):
    res = requests.get(f"https://api.chucknorris.io/jokes/{escape(id)}")
    joke = create_joke_from_response(res)
    joke["value"] = reverse_words(joke["value"])
    return joke


if __name__ == "__main__":
    port = int(os.getenv('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
