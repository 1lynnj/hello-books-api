from os import abort
from flask import Blueprint, jsonify, abort, make_response, request
from app import db
from app.models.book import Book

books_bp = Blueprint("books", __name__, url_prefix="/books")

@books_bp.route("", methods=["POST"])
def create_book():
    request_body = request.get_json()
    new_book = Book(title=request_body['title'],
            description=request_body['description'])

    db.session.add(new_book)
    db.session.commit()

    return make_response(jsonify(f"Book {new_book.title} successfully created"), 201)

# get all books, or query by title
@books_bp.route("", methods=["GET"])
def get_all_books():
    title_query = request.args.get("title")
    if title_query:
        books = Book.query.filter_by(title=title_query) # books = Book.query.filter_by(title="The Secret History")
    else:
        books = Book.query.all()
    
    books_response = []
    for book in books:
        books_response.append({
            "id": book.id,
            "title": book.title,
            "description": book.description
    })
    return jsonify(books_response)


def validate_book(book_id):
    try:
        book_id = int(book_id)
    except:
        abort(make_response({"message": f"book {book_id} is not valid"}, 400)) #400 is BAD REQUEST HTTP response code

    book = Book.query.get(book_id)
    
    if not book:
        abort(make_response({"message": f"book {book_id} not found"}, 404))
    
    return book

# Get id, title and description of one book by id
@books_bp.route("/<book_id>", methods=["GET"])
def read_one_book(book_id):
    book = validate_book(book_id)
    return {
        "id": book.id,
        "title": book.title,
        "description": book.description
    }


# updating a book
@books_bp.route("/<book_id>", methods=["PUT"])
def update_book(book_id):
    book = validate_book(book_id)

    request_body = request.get_json()

    book.title = request_body["title"]
    book.description = request_body["description"]

    db.session.commit()

    return make_response(jsonify(f"Book #{book.id} successfully updated."))

@books_bp.route("/<book_id>", methods=["DELETE"])
def delete_book(book_id):
    book = validate_book(book_id)

    db.session.delete(book)
    db.session.commit()

    return make_response(jsonify(f"Book #{book.id} successfully deleted."))




####Hardcoded resource before creating database methods
# class Book:
#     def __init__(self, id, title, description):
#         self.id = id
#         self.title = title
#         self.description = description

# book_1 = Book(1, "Secret History", "A thrilling college campus story.")
# book_2 = Book(2, "Winter's Tale", "An adventurous love story.")
# book_3 = Book(3, "To Kill A Mockingbird", "A thrilling coming of age story.")

# books = [book_1, book_2, book_3]

