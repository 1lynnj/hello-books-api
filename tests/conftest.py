import pytest
from app import create_app
from app import db
from flask.signals import request_finished
from app.models.book import Book


@pytest.fixture
def app():
    app = create_app({"TESTING": True})

    @request_finished.connect_via(app)
    def expire_session(sender, response, **extra):
        db.session.remove()

    with app.app_context():
        db.create_all()
        yield app

    with app.app_context():
        db.drop_all()


@pytest.fixture
def client(app):
    return app.test_client()

@pytest.fixture
def two_saved_books(app):
    history_book = Book(title="History Book", description="a book about history")
    comic_book = Book(title="Comic Book", description="a book with comics")

    db.session.add_all([history_book, comic_book])

    db.session.commit()