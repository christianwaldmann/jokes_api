from flask import render_template, request
from database import db, ma
from flask.blueprints import Blueprint
from sqlalchemy.sql.expression import func
import requests
from markupsafe import escape
from string_manipulation import reverse_words


app_bp = Blueprint("application", __name__)


class Author(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String(100))
    lastname = db.Column(db.String(100))
    jokes = db.relationship("InternalJoke", backref="author", lazy=True)

    def __init__(self, firstname, lastname):
        self.firstname = firstname
        self.lastname = lastname


class AuthorSchema(ma.Schema):
    class Meta:
        fields = ('id', 'firstname', 'lastname', 'author.jokes')


class InternalJoke(db.Model):
    id = db.Column(db.String(22), primary_key=True)
    author_id = db.Column(db.Integer, db.ForeignKey("author.id"), nullable=False)

    def __init__(self, id_, author_id):
        self.id = id_
        self.author_id = author_id


class InternalJokeSchema(ma.Schema):
    class Meta:
        fields = ('id', 'author_id')


def create_joke(id_, value):
    internaljoke = get_or_create_internal_joke(id_)
    author = Author.query.get(internaljoke.author_id)
    return {"id": id_, "value": value, "author": f"{author.firstname} {author.lastname}"}


def get_or_create_internal_joke(id_):
    internaljoke = InternalJoke.query.get(id_)
    if not internaljoke:
        random_author = Author.query.order_by(func.random()).first()
        internaljoke = InternalJoke(id_, random_author.id)
        db.session.add(internaljoke)
        db.session.commit()
    return internaljoke


@app_bp.route("/")
def index():
    return render_template("index.html")


@app_bp.route("/joke")
def joke_random():
    res = requests.get("https://api.chucknorris.io/jokes/random")
    res_json = res.json()
    return create_joke(res_json["id"], res_json["value"])


@app_bp.route("/joke/reverse")
def joke_random_reverse():
    res = requests.get("https://api.chucknorris.io/jokes/random")
    res_json = res.json()
    joke = create_joke(res_json["id"], res_json["value"])
    joke["value"] = reverse_words(joke["value"])
    return joke


@app_bp.route("/joke/<id>", methods=['GET'])
def joke_id(id):
    res = requests.get(f"https://api.chucknorris.io/jokes/{escape(id)}")
    res_json = res.json()
    return create_joke(id, res_json["value"])


@app_bp.route("/joke/<id>/reverse")
def joke_id_reverse(id):
    res = requests.get(f"https://api.chucknorris.io/jokes/{escape(id)}")
    res_json = res.json()
    joke = create_joke(id, res_json["value"])
    joke["value"] = reverse_words(joke["value"])
    return joke


author_schema = AuthorSchema()
authors_schema = AuthorSchema(many=True)
internaljoke_schema = InternalJokeSchema()


@app_bp.route('/author', methods=['POST'])
def add_author():
    firstname = request.json['firstname']
    lastname = request.json['lastname']
    new_author = Author(firstname, lastname)
    db.session.add(new_author)
    db.session.commit()
    return author_schema.jsonify(new_author)


@app_bp.route('/author/<id>', methods=['GET'])
def get_author(id):
    author = Author.query.get(id)
    return author_schema.jsonify(author)


@app_bp.route('/author', methods=['GET'])
def get_all_authors():
    all_authors = Author.query.all()
    return authors_schema.jsonify(all_authors)


@app_bp.route('/author/<id>', methods=['PUT'])
def update_author(id):
    author = Author.query.get(id)
    author.firstname = request.json['firstname']
    author.lastname = request.json['lastname']
    db.session.commit()
    return author_schema.jsonify(author)


@app_bp.route('/author/<id>', methods=['DELETE'])
def delete_author(id):
    author = Author.query.get(id)
    db.session.delete(author)
    db.session.commit()
    return author_schema.jsonify(author)


@app_bp.route("/joke/<jid>/<aid>", methods=['PUT'])
def assign_author_to_joke(jid, aid):
    internaljoke = InternalJoke.query.get(jid)
    internaljoke.author_id = aid
    db.session.commit()
    author = Author.query.get(internaljoke.author_id)
    res = requests.get(f"https://api.chucknorris.io/jokes/{escape(jid)}")
    res_json = res.json()
    return {"id": internaljoke.id, "value": res_json["value"], "author": f"{author.firstname} {author.lastname}"}
