from flask import Flask
from markupsafe import escape
import requests
from string_manipulation import reverse_words


app = Flask("JokesAPI")


@app.route("/joke")
def joke_random():
    res = requests.get("https://api.chucknorris.io/jokes/random")
    joke = res.json()
    return joke


@app.route("/joke/reverse")
def joke_random_reverse():
    res = requests.get("https://api.chucknorris.io/jokes/random")
    joke = res.json()
    joke["value"] = reverse_words(joke["value"])
    return joke


@app.route("/joke/<id>")
def joke_id(id):
    res = requests.get(f"https://api.chucknorris.io/jokes/{escape(id)}")
    joke = res.json()
    return joke


@app.route("/joke/<id>/reverse")
def joke_id_reverse(id):
    res = requests.get(f"https://api.chucknorris.io/jokes/{escape(id)}")
    joke = res.json()
    joke["value"] = reverse_words(joke["value"])
    return joke
