from os import abort
from flask import Blueprint, jsonify, abort, make_response, request
from app import db
from app.models.book import Book
from app.models.author import Author

books_bp = Blueprint("books", __name__, url_prefix="/books")
authors_bp = Blueprint("authors", __name__, url_prefix="/authors")

@books_bp.route("", methods=["POST"])
def create_book():
    request_body = request.get_json()
    new_book = Book.from_dict(request_body)

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
        books_response.append(book.to_dict())

    return jsonify(books_response)


# refactored validate book to include validating other ids like author
def validate_model(cls, model_id):
    try:
        model_id = int(model_id)
    except:
        abort(make_response({"message": f"{cls.__name__} {model_id} is not valid"}, 400)) #400 is BAD REQUEST HTTP response code

    model = cls.query.get(model_id)
    
    if not model:
        abort(make_response({"message": f"{cls.__name__} {model_id} not found"}, 404))
    
    return model

# Get id, title and description of one book by id
@books_bp.route("/<book_id>", methods=["GET"])
def read_one_book(model_id):
    book = validate_model(Book, model_id)
    return book.to_dict()


# updating a book
@books_bp.route("/<book_id>", methods=["PUT"])
def update_book(model_id):
    book = validate_model(model_id)

    request_body = request.get_json()

    book.title = request_body["title"]
    book.description = request_body["description"]

    db.session.commit()

    return make_response(jsonify(f"Book #{book.id} successfully updated."))

@books_bp.route("/<book_id>", methods=["DELETE"])
def delete_book(model_id):
    book = validate_model(model_id)

    db.session.delete(book)
    db.session.commit()

    return make_response(jsonify(f"Book #{book.id} successfully deleted."))


###################Author routes#################
@authors_bp.route("", methods=["GET"])
def get_all_authors():
    name_query = request.args.get("name")
    if name_query:
        authors = Author.query.filter_by(name=name_query) 
    else:
        authors = Author.query.all()
    
    authors_response = []
    for author in authors:
        authors_response.append(author.to_dict())

    return jsonify(authors_response)

@authors_bp.route("", methods=["POST"])
def create_author():
    request_body = request.get_json()
    new_author = Author.from_dict(request_body)

    db.session.add(new_author)
    db.session.commit()

    return make_response(jsonify(f"Author {new_author.name} successfully created"), 201)

@authors_bp.route("/<author_id>/books", methods=["POST"])
def create_book_with_author_id(author_id):

    request_body = request.get_json()
    new_book = Book(
        title=request_body["title"],
        description=request_body["description"],
        author_id=author_id
        )

    db.session.add(new_book)
    db.session.commit()

    return make_response(jsonify(f"Book {new_book.title} by {new_book.author.name} successfully created"), 201)

@authors_bp.route("/<author_id>/books", methods=["GET"])
def get_all_books_by_author_id(author_id):

    # getting the author 
    author = validate_model(Author, author_id)
    
    authors_response = []
    # author.books is like doing a query of books by author 
    # - this is set up in the Author model as a one-to-many relationship
    for book in author.books:
        authors_response.append(book.to_dict())

    return jsonify(authors_response)



##############Retired code################
# refactored following function to validate_model
# def validate_book(book_id):
#     try:
#         book_id = int(book_id)
#     except:
#         abort(make_response({"message": f"book {book_id} is not valid"}, 400)) #400 is BAD REQUEST HTTP response code

#     book = Book.query.get(book_id)
    
#     if not book:
#         abort(make_response({"message": f"book {book_id} not found"}, 404))
    
#     return book

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

