from flask import Blueprint, jsonify, abort, make_response

hello_world_bp = Blueprint("hello_world", __name__)


# example of an endpoint
@hello_world_bp.route("/hello-world", methods=["GET"])
def say_hello_world():
    my_beautiful_response_body = "Hello, World!"
    return my_beautiful_response_body

@hello_world_bp.route("/hello/JSON", methods=["GET"])
def say_hello_json():
    return {
        "name": "Ada Lovelace",
        "message": "Hello!",
        "hobbies": ["Fishing", "Swimming", "Watching Reality Shows"]
    }

@hello_world_bp.route("/broken-endpoint-with-broken-server-code")
def broken_endpoint():
    response_body = {
        "name": "Ada Lovelace",
        "message": "Hello!",
        "hobbies": ["Fishing", "Swimming", "Watching Reality Shows"]
    }
    new_hobby = "Surfing"
    response_body["hobbies"] += [new_hobby]

    return response_body

class Book:
    def __init__(self, id, title, description):
        self.id = id
        self.title = title
        self.description = description

book_1 = Book(1, "Secret History", "A thrilling college campus story.")
book_2 = Book(2, "Winter's Tale", "An adventurous love story.")
book_3 = Book(3, "To Kill A Mockingbird", "A thrilling coming of age story.")

books = [book_1, book_2, book_3]

books_bp = Blueprint("books", __name__, url_prefix="/books")

# Get list of all books
@books_bp.route("", methods=["GET"])
def handle_books():
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

    for book in books:
        if book.id == book_id:
            return book
    
    abort(make_response({"message": f"book {book_id} not found"}, 404))

# Get id, title and description of one book by id
@books_bp.route("/<book_id>", methods=["GET"])
def handle_book(book_id):
    book = validate_book(book_id)
    return {
        "id": book.id,
        "title": book.title,
        "description": book.description
    }

