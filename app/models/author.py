from app import db

class Author(db.Model):
    __tablename__ = "author"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String)
    books = db.relationship("Book", back_populates="author", lazy=True)
    # lazy means when call author object, will not return books by author until
    # specifically queried

    def to_dict(self):
        return {
        "id": self.id,
        "name": self.name
    }

    @classmethod
    def from_dict(cls, author_data):
        new_author = Author(name=author_data["name"])
        return new_author