from app import db

class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String)
    description = db.Column(db.String)

    def to_dict(self):
        return {
        "id": self.id,
        "title": self.title,
        "description": self.description
    }

    @classmethod
    def from_dict(cls, book_data):
        new_book = Book(title=book_data["title"], description=book_data["description"])
        return new_book