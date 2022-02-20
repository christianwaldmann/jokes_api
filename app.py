from flask import Flask
import os
from dotenv import load_dotenv

from database import db, ma
from views import app_bp, Author


load_dotenv()


def create_app():
    app = Flask("JokesAPI")
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("DATABASE_URL")
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)
    ma.init_app(app)
    app.register_blueprint(app_bp)
    return app


def setup_database(app):
    with app.app_context():
        db.create_all()
        author = Author("Hans", "Jürgen")
        db.session.add(author)
        db.session.commit()


if __name__ == "__main__":
    port = int(os.getenv('PORT', 5000))
    app = create_app()
    if not os.path.isdir(os.getenv("DATABASE_LOCAL_PATH")):
        setup_database(app)
    app.run(host='0.0.0.0', port=port)
