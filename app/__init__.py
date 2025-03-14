# startup logic and app configurations

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from dotenv import load_dotenv
import os

db = SQLAlchemy()
migrate = Migrate()
load_dotenv()

def create_app(test_config=None):
    app = Flask(__name__)

    if not test_config:
        app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
        app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get("SQLALCHEMY_DATABASE_URI")

    else:
        app.config["TESTING"] = True
        app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
        app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("SQLALCHEMY_TEST_DATABASE_URI")

    # app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    # app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql+psycopg2://postgres:postgres@localhost:5432/hello_books_development'

    from app.models.book import Book
    from app.models.author import Author
    
    db.init_app(app)
    migrate.init_app(app, db)

    from .routes import books_bp
    app.register_blueprint(books_bp)

    from .routes import authors_bp
    app.register_blueprint(authors_bp)

    return app






# from flask import Flask

# def create_app(test_config=None):
#     app = Flask(__name__)

#     from .routes import hello_world_bp
#     app.register_blueprint(hello_world_bp)

#     from .routes import books_bp
#     app.register_blueprint(books_bp)

#     return app